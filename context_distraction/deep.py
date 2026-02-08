"""DeepAgents-based agent with planning and synthesis middleware.

Uses middleware to enforce structured workflow:
- PlanningMiddleware: Creates execution plan before agent starts
- SynthesisMiddleware: Synthesizes final response after agent finishes
"""

from datetime import datetime
from typing import Annotated, Any, Dict, List, TypedDict
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.agents.middleware.types import AgentMiddleware
from deepagents.middleware import FilesystemMiddleware
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage, get_buffer_string
from langchain_core.tools import InjectedToolCallId, tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langgraph.types import Command

from context_distraction.tools import (
    deepagent_research_tools
)

load_dotenv(override=True)

# =============================================================================
# STATE
# =============================================================================

class ResearchState(MessagesState):
    """Custom state for research tasks."""
    research_brief: str  # High-level breakdown of objectives


# =============================================================================
# PROMPTS
# =============================================================================

RESEARCH_BRIEF_PROMPT = """Create a research brief that breaks down this request.

List:
1. The key objectives (WHAT we need to find/answer)
2. What specific data points are needed (metrics, values to look up)
3. Any calculations needed to combine the data
4. Dependencies between tasks

IMPORTANT: Workers have access to databases with pre-computed metrics (correlations, market sizes, growth rates, NPVs, ROIs, etc). The brief should focus on WHAT data to retrieve, not HOW to calculate it from scratch.

Be thorough but concise."""


SUPERVISOR_PROMPT = f"""You coordinate complex tasks by delegating to specialized workers.

A research brief has been prepared outlining the objectives and requirements.

## Approach

Delegate coherent tasks to workers:
1. Identify distinct objectives
2. Delegate each objective as a complete task - workers can handle multi-step analysis
3. Track results systematically

## Delegation Rules

Use the `delegate` tool to assign tasks. Each worker handles ONE specific task independently.

**Give objectives, not methods**: Tell workers WHAT to find, not HOW to find it. Workers have access to data sources and will determine the best approach. You may include helpful formulas that may be relevant.

**Never invent figures**: Only include numbers in your delegation if they:
- Appear verbatim in the original request, OR
- Were returned by a previous worker

If you don't have a value, don't guess - delegate a task to find it first.

**One delegation per objective**: If you need data for 5 domains, delegate ONE task that covers all 5.

**Sequential for Dependencies**: Wait for results before delegating dependent tasks.

## Execution

1. Delegate complete objectives to workers - they have data sources and calculation tools
2. Each worker handles the full task independently (research + compute)
3. Verify results make sense (check units, magnitude) - re-delegate with clarification if needed
4. Report the computed results - never calculate yourself

Current date: {datetime.now().strftime('%B %d, %Y')}
"""


WORKER_PROMPT = f"""You are a specialist completing a specific task.

## Your Job
Complete EXACTLY what you're asked - no more, no less.

## Process
1. **Plan first** - Write your approach to a scratchpad file before taking action
2. **Gather data** - Use research tools to find needed values
3. **Calculate** - Use calculation tools (never mental math)
4. **Return result** - Call `done(answer="...")` with your final answer

## Using the Filesystem
You have access to read/write files. Use this to track your work:
- Write your plan to `scratchpad.md` before starting
- Record intermediate values as you gather them
- This prevents losing track of what you've already done

## Available Tools
- `get_statistics` - quantitative metrics (market size, growth rates, investments)
- `research_topic` - qualitative info and methodology (analysis parameters, project structures)
- `calculate_compound_growth`, `calculate_cost_benefit_analysis` - for financial projections
- `calculate_ratio`, `calculate_percentage`, `calculate_sum`, `calculate_weighted_average` - for math
- `calculate_present_value`, `calculate_power` - for discounting and exponents
- `done` - Call this with your final answer

## Data Gathering
If you need overall metrics, use statistics. If you need methodology or detailed parameters, use research.

Current date: {datetime.now().strftime('%B %d, %Y')}
"""


SYNTHESIS_PROMPT = """Create a final response based on the work completed.

Review the conversation and synthesize all findings into a comprehensive response that:
1. Addresses everything the user originally asked for
2. Provides final COMPUTED numerical values (not formulas)
3. Follows any format the user requested
4. Is well-organized and complete"""


# =============================================================================
# MIDDLEWARE
# =============================================================================

class ResearchBriefMiddleware(AgentMiddleware):
    """Middleware that creates a research brief before the agent starts."""

    def __init__(self, model: ChatOpenAI):
        self.model = model

    async def abefore_agent(self, state, runtime) -> dict[str, Any] | None:
        """Create a research brief and inject it into messages."""
        messages = state.get("messages", [])
        if not messages:
            return None

        # Get the user's original request (first message)
        original_request = messages[0]

        # Create research brief
        prompt = [
            SystemMessage(content=RESEARCH_BRIEF_PROMPT),
            original_request,
        ]

        brief = self.model.invoke(prompt)

        # Inject brief as an AI message after the user request
        brief_message = AIMessage(content=f"## Research Brief\n{brief.content}")
        new_messages = [messages[0], brief_message] + messages[1:]

        return {"messages": new_messages, "research_brief": brief.content}


class SynthesisMiddleware(AgentMiddleware):
    """Middleware that synthesizes final response after the agent finishes."""

    def __init__(self, model: ChatOpenAI):
        self.model = model

    async def aafter_agent(self, state, runtime) -> dict[str, Any] | None:
        """Synthesize all findings into a final response."""
        messages = state.get("messages", [])
        if not messages:
            return None

        # Get original request
        original_request = messages[0].content if messages else ""

        # Get work done (everything after the first message)
        work_done = get_buffer_string(messages[1:]) if len(messages) > 1 else ""

        # Create synthesis prompt
        prompt = [
            SystemMessage(content=SYNTHESIS_PROMPT),
            HumanMessage(
                content=f"## Original Request\n{original_request}\n\n## Work Completed\n{work_done}"
            )
        ]

        # Generate final response
        response = self.model.invoke(prompt)

        # Return state update - append synthesis to messages
        return {"messages": messages + [response]}


# =============================================================================
# CUSTOM DELEGATE TOOL
# =============================================================================

def create_delegate_tool(worker_runnable):
    """Create a delegate tool that passes raw context to workers."""

    @tool
    async def delegate(
        task: str,
        breakdown: List[str],
        raw_context: List[str],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        """Delegate a task to a worker.

        Args:
            task: Clear description of what the worker should do
            breakdown: Step-by-step instructions including formulas and expected units
            raw_context: VERBATIM snippets from the original request
        """
        breakdown_section = "\n".join(f"{i+1}. {step}" for i, step in enumerate(breakdown))
        context_section = "\n".join(f"- {snippet}" for snippet in raw_context)
        task_id = tool_call_id[-8:]  # Use last 8 chars as unique ID
        full_prompt = f"""## Task
{task}

## Task ID: {task_id}
Use `scratchpad-{task_id}.md` to track your work.

## Steps to Complete
{breakdown_section}

## Original Context (verbatim)
{context_section}

## Guidance
- Write your plan to scratchpad-{task_id}.md before starting
- Look up exact values rather than estimating
- Use calculation tools rather than mental math
- Pay attention to units - match the units in your answer to what was asked
- Before returning, verify your answer addresses exactly what was asked

Complete the task following the steps above."""

        try:
            result = await worker_runnable.ainvoke({"messages": [HumanMessage(content=full_prompt)]})
            final_content = result["messages"][-1].content if result.get("messages") else "No result"
        except Exception as e:
            final_content = f"Worker failed: {str(e)[:200]}"

        return Command(
            goto=END,
            update={"messages": [ToolMessage(content=final_content, tool_call_id=tool_call_id)]}
        )

    return delegate


# =============================================================================
# AGENT CREATION
# =============================================================================

def create_research_agent(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0,
    subagent_recursion_limit: int = 50,
    main_recursion_limit: int = 200,
):
    """Create an agent with planning and synthesis middleware.

    Args:
        model_name: The model to use
        temperature: Temperature setting
        subagent_recursion_limit: Max recursion for worker subagents
        main_recursion_limit: Max recursion for main agent

    Returns:
        A compiled deep agent with middleware
    """
    model = ChatOpenAI(model=model_name, temperature=temperature)

    # Create worker runnable for our custom delegate tool
    worker_runnable = create_agent(
        model=model,
        system_prompt=WORKER_PROMPT,
        tools=deepagent_research_tools,
    ).with_config({"recursion_limit": subagent_recursion_limit})

    # Create custom delegate tool with structured parameters
    delegate_tool = create_delegate_tool(worker_runnable)

    # Create agent using langchain's create_agent with deepagents middleware
    # This gives us file/todo tools without the conflicting task tool
    agent = create_agent(
        model=model,
        tools=[delegate_tool],  # Our custom delegation with breakdown/context
        system_prompt=SUPERVISOR_PROMPT,
        middleware=[
            TodoListMiddleware(),
            FilesystemMiddleware(),
            ResearchBriefMiddleware(model),
            SynthesisMiddleware(model),
        ],
        context_schema=ResearchState,
    )

    return agent.with_config({"recursion_limit": main_recursion_limit})


# Default agent instance
deep_agent = create_research_agent()


# =============================================================================
# RUNNER
# =============================================================================

async def run_deep_agent(query: str) -> Dict[str, Any]:
    """Run the agent on a query and extract outputs."""
    from context_distraction.resources.validation_utils import extract_tool_calls_from_message

    try:
        trajectory = []
        final_response = ""
        all_messages = []

        async for chunk in deep_agent.astream(
            {"messages": [HumanMessage(content=query)]},
            stream_mode="updates",
        ):
            if isinstance(chunk, dict):
                for key, value in chunk.items():
                    if isinstance(value, dict) and "messages" in value:
                        msgs = value["messages"]
                        if isinstance(msgs, list):
                            all_messages.extend(msgs)
                            for msg in msgs:
                                tool_calls = extract_tool_calls_from_message(msg)
                                trajectory.extend(tool_calls)

        # Get final response from last AIMessage
        for msg in reversed(all_messages):
            if hasattr(msg, 'content') and msg.content and isinstance(msg, AIMessage):
                final_response = msg.content
                break

        return {
            "final_response": final_response,
            "trajectory": trajectory,
            "error": None
        }
    except Exception as e:
        return {
            "final_response": "",
            "trajectory": [],
            "error": str(e)
        }
