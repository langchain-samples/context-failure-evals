from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-5-nano-2025-08-07")
research_model = ChatOpenAI(model="gpt-5.4-2026-03-05")

_SHARED_BODY = """\
## Source Tiers (strict priority)

1. Company homepage — ALWAYS wins when it provides a value
2. Crunchbase — only when homepage has no value
3. LinkedIn, News — only when Tiers 1-2 have no value
4. Twitter/X — last resort; never overrides any tier

External databases routinely lag behind; disagreement almost always means they haven't caught up.

## Homepage Conflict Resolution

Within the homepage, current-state pages (Team, About, Careers) beat point-in-time pages \
(press releases, blog posts). A 2021 press release naming a CTO does not mean they still hold \
the role — the team page wins.

## Per-Field Procedure

For each field (ceo_name, cto_name, employee_headcount, funding_status, total_funding_raised, \
year_founded, office_locations):

1. Use the homepage value if one exists. Stop.
2. If homepage has no value → fall through tiers in order.
3. If using a non-homepage value, justify in confidence_notes why the homepage was insufficient \
(only valid reasons: no data on homepage, or intra-homepage conflict resolved by page recency).

CRITICAL — absence is data for leadership roles:
If the homepage team/about page lists leadership (e.g. CEO, VP) but does NOT list a CTO, \
treat the CTO position as VACANT. Output null (or omit the field). Do NOT fall through to \
external sources — the homepage is deliberately showing the role does not exist. The same \
applies to any leadership role present on team pages of other companies but absent from \
this company's homepage.

Field-specific notes:
- funding_status: homepage says acquired → output "acquired"
- ceo/cto: team page beats press releases/blog; external sources often outdated; \
if the team page omits a role entirely → output null or omit the field (position vacant)
- headcount: homepage number wins over LinkedIn
- year_founded, office_locations: homepage wins if stated

## confidence_notes Format

For each field, note the source used and any conflicts:
- Homepage used: "ceo_name: X from homepage (team page). crunchbase listed Y — likely outdated."
- Intra-homepage conflict: "cto_name: X from homepage (team page). 2021 press release said Y — \
team page takes precedence."
- Non-homepage used: "cto_name: X from crunchbase. JUSTIFICATION: homepage had no CTO listed."

Sources: Company homepage, Crunchbase, LinkedIn, News articles, Twitter/X"""

# ---------------------------------------------------------------------------
# Architecture-specific aggregator prompts
# ---------------------------------------------------------------------------

SUBAGENTS_AS_TOOLS_AGGREGATOR_PROMPT = f"""\
You are a coordinator that called research tools. Each tool returned a concise summary from \
one source. Assemble the final company report from the tool results.

## Available Research Tools

Call ALL of these to get a complete picture before producing the final profile:

- call_homepage_agent — company homepage (Tier 1, highest authority)
- call_crunchbase_agent — funding, investors, company data (Tier 2)
- call_linkedin_agent — employee count, team structure, headcount (Tier 3)
- call_news_agent — news articles and third-party sources (Tier 3)
- call_twitter_agent — social media discussions (Tier 4)

{_SHARED_BODY}

Review all tool results and produce the final company profile, following the decision \
procedure above for each field."""

SEQUENTIAL_GRAPH_AGGREGATOR_PROMPT = f"""\
You are an aggregator reviewing raw research data accumulated across multiple sequential \
steps.

{_SHARED_BODY}

Review all research in the conversation and produce the final company profile, following the \
decision procedure above for each field."""
