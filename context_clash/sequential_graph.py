"""
Sequential graph for company research from pre-generated datasets.

Each subagent is invoked sequentially with the full accumulated message history.
Raw data from all sources accumulates in the messages, creating maximum "context
clash" from conflicting information for the final aggregator.

Graph: START -> crunchbase -> pitchbook -> linkedin -> glassdoor -> news -> wikipedia -> homepage -> twitter -> aggregator -> END
"""

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain_core.messages import AnyMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from .model import SEQUENTIAL_GRAPH_AGGREGATOR_PROMPT, model
from .subagents import CompanyInfo
from .subagents.crunchbase import agent as crunchbase_agent
from .subagents.glassdoor import agent as glassdoor_agent
from .subagents.homepage import agent as homepage_agent
from .subagents.linkedin import agent as linkedin_agent
from .subagents.news import agent as news_agent
from .subagents.pitchbook import agent as pitchbook_agent
from .subagents.twitter import agent as twitter_agent
from .subagents.wikipedia import agent as wikipedia_agent

# --- Graph State ---


class ResearchState(MessagesState):
    structured_response: CompanyInfo | None = None


# --- Helpers ---


def strip_structured_responses(messages: list[AnyMessage]) -> list[AnyMessage]:
    """Remove CompanyInfo tool calls and their tool responses from messages.

    Each subagent produces a CompanyInfo structured output after reading raw data.
    We strip these so only the raw data tool calls flow through the graph,
    keeping maximum "context clash" for the aggregator.
    """
    # Collect tool_call IDs for CompanyInfo calls
    company_info_call_ids: set[str] = set()
    for msg in messages:
        if msg.type == "ai" and getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                if tc["name"] == "CompanyInfo":
                    company_info_call_ids.add(tc["id"])

    filtered: list[AnyMessage] = []
    for msg in messages:
        # Skip AI messages whose only tool calls are CompanyInfo
        if msg.type == "ai" and getattr(msg, "tool_calls", None):
            if all(tc["name"] == "CompanyInfo" for tc in msg.tool_calls):
                continue
        # Skip tool responses for CompanyInfo calls
        if (
            msg.type == "tool"
            and getattr(msg, "tool_call_id", None) in company_info_call_ids
        ):
            continue
        filtered.append(msg)
    return filtered


# --- Graph Nodes ---


def homepage_node(state: ResearchState) -> dict:
    result = homepage_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def crunchbase_node(state: ResearchState) -> dict:
    result = crunchbase_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def pitchbook_node(state: ResearchState) -> dict:
    result = pitchbook_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def linkedin_node(state: ResearchState) -> dict:
    result = linkedin_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def glassdoor_node(state: ResearchState) -> dict:
    result = glassdoor_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def news_node(state: ResearchState) -> dict:
    result = news_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def wikipedia_node(state: ResearchState) -> dict:
    result = wikipedia_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


def twitter_node(state: ResearchState) -> dict:
    result = twitter_agent.invoke(state)
    return {"messages": strip_structured_responses(result["messages"])}


aggregator_agent = create_agent(
    name="aggregator",
    model=model,
    tools=[],
    system_prompt=SEQUENTIAL_GRAPH_AGGREGATOR_PROMPT,
    response_format=ProviderStrategy(schema=CompanyInfo, strict=True),
)


def aggregator_node(state: ResearchState) -> dict:
    result = aggregator_agent.invoke(state)
    return result


# --- Build the Graph ---

builder = StateGraph(ResearchState)

builder.add_node("homepage", homepage_node)
builder.add_node("crunchbase", crunchbase_node)
builder.add_node("pitchbook", pitchbook_node)
builder.add_node("linkedin", linkedin_node)
builder.add_node("glassdoor", glassdoor_node)
builder.add_node("news", news_node)
builder.add_node("wikipedia", wikipedia_node)
builder.add_node("twitter", twitter_node)
builder.add_node("aggregator", aggregator_node)

builder.add_edge(START, "crunchbase")
builder.add_edge("crunchbase", "pitchbook")
builder.add_edge("pitchbook", "linkedin")
builder.add_edge("linkedin", "glassdoor")
builder.add_edge("glassdoor", "news")
builder.add_edge("news", "wikipedia")
builder.add_edge("wikipedia", "homepage")
builder.add_edge("homepage", "twitter")
builder.add_edge("twitter", "aggregator")
builder.add_edge("aggregator", END)

graph = builder.compile()
graph.name = "sequential_graph"

agent = graph

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Research the company Firebolt."}]}
    )
    print(result["structured_response"].model_dump_json(indent=2))
