"""
Research Assistant Agent Implementation

Creates standard and deep agents for context distraction evaluation.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import MemorySaver

from context_distraction.tools import all_research_tools, custom_agent_tools
from context_distraction.instructions import (
    STANDARD_RESEARCH_INSTRUCTIONS,
    CUSTOM_AGENT_RESEARCH_INSTRUCTIONS,
)
from context_distraction.middleware import AnswerStorageMiddleware, CustomAgentState


def create_standard_agent(llm, tools=None, system_prompt=None):
    """
    Create a standard agent using create_agent.
    
    This agent accumulates all tool call results in context,
    leading to context distraction as tasks get larger.
    """
    if tools is None:
        tools = all_research_tools
    if system_prompt is None:
        system_prompt = STANDARD_RESEARCH_INSTRUCTIONS
    
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )


def create_custom_agent(llm, tools=None, system_prompt=None, summarize_threshold: int = 20):
    """
    Create a custom agent with reflection capabilities, enhanced instructions, and summarization middleware.
    
    This agent:
    - Uses reflection tool to plan approach
    - Uses enhanced instructions for better planning and tool usage
    - Has summarization middleware that compresses tool results while preserving statistics
    - Does NOT use deep agents filesystem approach
    """
    if tools is None:
        tools = custom_agent_tools
    if system_prompt is None:
        system_prompt = CUSTOM_AGENT_RESEARCH_INSTRUCTIONS
    
    # Create answer storage middleware that cleans up calculation history when answers are stored
    answer_storage_middleware = AnswerStorageMiddleware()
    
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        middleware=[answer_storage_middleware],
        state_schema=CustomAgentState,  # Ensures entire graph uses custom schema with all_tool_calls
    )
