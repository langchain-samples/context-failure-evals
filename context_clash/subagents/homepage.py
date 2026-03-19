from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy

from ..model import research_model as model
from .common import COMMON_TOOLS, SUBAGENT_PROMPT
from .models import CompanyInfo

HOMEPAGE_CONFLICT_PROMPT = """
## Resolving Conflicts WITHIN the Homepage

Not all homepage pages are equally current. The homepage may contain both current-state pages \
and historical snapshots. Apply this sub-priority:

CURRENT-STATE pages (most authoritative within homepage):
  → Team/leadership page, About page, Careers page
  These reflect the company's present reality.

POINT-IN-TIME pages (may be outdated within homepage):
  → Press releases, Blog posts
  These describe the company at a specific past date. A press release announcing a CTO hire \
in 2021 does NOT mean that person is still CTO today.

When homepage pages conflict with each other: prefer current-state pages over point-in-time \
pages. If a press release names a different CTO than the team page, the team page wins.
"""

EXTENDED_SUBAGENT_PROMPT = (
    SUBAGENT_PROMPT.format(datasource="homepage") + HOMEPAGE_CONFLICT_PROMPT
)

TOOLS = COMMON_TOOLS
PROMPT = EXTENDED_SUBAGENT_PROMPT

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=PROMPT,
    response_format=ProviderStrategy(schema=CompanyInfo, strict=True),
)
