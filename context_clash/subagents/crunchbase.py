from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy

from ..model import research_model as model
from .common import COMMON_TOOLS, SUBAGENT_PROMPT
from .models import CompanyInfo

TOOLS = COMMON_TOOLS
PROMPT = SUBAGENT_PROMPT.format(datasource="Crunchbase")

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=PROMPT,
    response_format=ProviderStrategy(schema=CompanyInfo, strict=True),
)
