"""
Research Assistant Agent Implementation

Creates standard and deep agents for context distraction evaluation.
This is the "failing agent" baseline that doesn't use subagents for context isolation.
"""
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from context_distraction.tools import all_research_tools

load_dotenv(override=True)

STANDARD_RESEARCH_INSTRUCTIONS = """You are conducting a comprehensive multi-topic research project. This requires gathering extensive information across multiple domains and synthesizing findings into a coherent report.

CRITICAL OUTPUT FORMAT REQUIREMENTS:

1. **Final Report Format**: Your final response MUST be valid Markdown with the following structure:
   - Executive Summary (markdown heading)
   - Domain Analysis sections (one per domain)
   - Cross-Domain Comparison
   - Investment Recommendations
   - Appendices

## Available Tools

**Research Tools:**
- `get_statistics` - quantitative metrics (market size, growth rates, investments)
- `research_topic` - qualitative info and methodology (analysis parameters, project structures)
- `get_expert_opinion` - domain expert perspectives
- `get_case_study` - detailed examples and scenarios
- `get_year_data` - historical data for specific years

**Calculation Tools:**
- `calculate_compound_growth` - project growth over time periods
- `calculate_cost_benefit_analysis` - NPV, ROI, and payback analysis

**Atomic Math Tools:**
- `calculate_discount_factor`, `calculate_present_value` - discounting calculations
- `calculate_percentage`, `calculate_ratio`, `calculate_power`, `calculate_sum` - basic math
- `calculate_weighted_average` - weighted averages

**Research Approach:**
Use any combination of these tools in whatever order makes sense. If you need more context for a calculation, gather background information first. Important information may be found in case studies, expert opinions, and research key findings.

**Data Gathering:**
If you need overall metrics, use statistics. If you need methodology or detailed parameters, use research.

Research Principles:
- **Explore before calculating**: If you don't have all needed data, gather and review available information first. It's important to understand the full context before performing calculations to ensure you're using the right values and methods.
- **Unit consistency**: Keep calculation values at same scale. Return answers in the same units as input data (e.g., if inputs are "$100 million", answer in millions)
  * "100 kilometers" → extract as **100** (in kilometers), NOT 100000 (in meters)
  * Keep ALL calculation values at the same scale throughout
  * When converting between units, be explicit about the conversion factor
  * If mixing scales is unavoidable, document the unit for each value clearly

**CRITICAL: Systematic Calculation Approach**

For multi-step calculations, follow this process:
1. **Identify what you need** - List all intermediate values required
2. **Calculate each using tools** - Use calculation tools, not mental arithmetic. However, be efficient with your tool usage. Avoid redundant calls.
3. **Use exact tool results** - When a tool returns a value, use that EXACT value in your next step (don't substitute a different number)
4. **Verify consistency** - Check that all parameters come from your calculated results

This systematic approach prevents errors from mental arithmetic and value substitution."""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    model=llm,
    tools=all_research_tools,
    system_prompt=STANDARD_RESEARCH_INSTRUCTIONS
)
