"""
Financial Research Agent Implementation

Creates a standard agent for context poisoning evaluation in financial research.
"""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

from context_poisoning.tools import all_tools
from context_poisoning.instructions import FINANCIAL_RESEARCH_INSTRUCTIONS

load_dotenv()

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)

agent = create_agent(
    model=llm,
    tools=all_tools,
    system_prompt=FINANCIAL_RESEARCH_INSTRUCTIONS
)
