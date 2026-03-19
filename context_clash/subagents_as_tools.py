"""
Subagents-as-tools agent for company research from pre-generated datasets.

Each source is a subagent wrapped as a tool. The coordinator only sees the
subagent's final summary, keeping the context lean and reducing "context clash"
from conflicting raw data.
"""

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain_core.tools import tool

from .model import SUBAGENTS_AS_TOOLS_AGGREGATOR_PROMPT, model
from .subagents.crunchbase import agent as crunchbase_agent
from .subagents.glassdoor import agent as glassdoor_agent
from .subagents.homepage import agent as homepage_agent
from .subagents.linkedin import agent as linkedin_agent
from .subagents.models import CompanyInfo
from .subagents.news import agent as news_agent
from .subagents.pitchbook import agent as pitchbook_agent
from .subagents.twitter import agent as twitter_agent
from .subagents.wikipedia import agent as wikipedia_agent


@tool
def call_homepage_agent(query: str) -> str:
    """Call the homepage research subagent to find information from the company's homepage."""
    result = homepage_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_crunchbase_agent(query: str) -> str:
    """Call the Crunchbase research subagent to find funding, investors, and company data."""
    result = crunchbase_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_pitchbook_agent(query: str) -> str:
    """Call the PitchBook research subagent to find funding, deal history, and financial data."""
    result = pitchbook_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_linkedin_agent(query: str) -> str:
    """Call the LinkedIn research subagent to find employee count, team structure, and headcount."""
    result = linkedin_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_glassdoor_agent(query: str) -> str:
    """Call the Glassdoor research subagent to find employee reviews and company insights."""
    result = glassdoor_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_news_agent(query: str) -> str:
    """Call the news research subagent to find information from news articles and third party sources."""
    result = news_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_wikipedia_agent(query: str) -> str:
    """Call the Wikipedia research subagent to find encyclopedic information about the company."""
    result = wikipedia_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool
def call_twitter_agent(query: str) -> str:
    """Call the Twitter/X research subagent to find social media discussions about the company."""
    result = twitter_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


agent = create_agent(
    name="subagents-as-tools",
    model=model,
    tools=[
        call_homepage_agent,
        call_crunchbase_agent,
        call_pitchbook_agent,
        call_linkedin_agent,
        call_glassdoor_agent,
        call_news_agent,
        call_wikipedia_agent,
        call_twitter_agent,
    ],
    system_prompt=SUBAGENTS_AS_TOOLS_AGGREGATOR_PROMPT,
    response_format=ProviderStrategy(schema=CompanyInfo, strict=True),
)

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Research the company Firebolt."}]}
    )
    print(result["structured_response"].model_dump_json(indent=2))
