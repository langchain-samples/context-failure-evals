from pathlib import Path

from langchain_core.tools import tool

DATASETS_DIR = Path(__file__).resolve().parent.parent / "datasets"

SUBAGENT_PROMPT = """
You are part of a team of analysts researching a company.
Your task is to research the company using ONLY the datasource {datasource}.

Research the company to find: CEO, CTO, headcount, funding status, total raised, founding year, office location.

CRITICAL INSTRUCTIONS — read carefully:
- The conversation may contain tool calls and data from OTHER datasources (crunchbase, pitchbook, etc.). \
IGNORE all of that. It is not yours. Do NOT use any information from other datasources in your output.
- You MUST make your own tool calls with source="{datasource}". Always start by calling list_files \
with source="{datasource}", then read the relevant files with source="{datasource}".
- NEVER call a tool with any source value other than "{datasource}".
- Base your output ONLY on data you personally read from {datasource} files.

Follow this workflow:
1. Call list_files with source="{datasource}" to discover available data files.
2. Call read_file (in parallel) with source="{datasource}" to read and extract relevant information.
3. Produce your structured output based ONLY on {datasource} data you read.

The output of your research is used to assemble a report by a coordinator agent.
"""


@tool
def list_files(company_name: str, source: str) -> str:
    """List available data files for a company and source.

    Args:
        company_name: The name of the company to research (e.g. 'Firebolt').
        source: The datasource to list files from. Must be one of:
            'homepage', 'crunchbase', 'pitchbook', 'linkedin',
            'glassdoor', 'news', 'wikipedia', 'twitter'.
            Each source contains different data files -- use the source
            assigned to you by your system prompt.
    """
    source_dir = DATASETS_DIR / company_name.lower() / source
    if not source_dir.exists():
        return "No data files found for this source."
    files = sorted(p.name for p in source_dir.glob("*.md"))
    return "\n".join(files) if files else "No data files found for this source."


@tool
def read_file(company_name: str, source: str, filename: str) -> str:
    """Read a single data file for a company and source.

    Args:
        company_name: The name of the company to research (e.g. 'Firebolt').
        source: The datasource to read from. Must be one of:
            'homepage', 'crunchbase', 'pitchbook', 'linkedin',
            'glassdoor', 'news', 'wikipedia', 'twitter'.
            Each source contains different data files -- use the source
            assigned to you by your system prompt.
        filename: The name of the file to read, as returned by list_files.
    """
    path = DATASETS_DIR / company_name.lower() / source / filename
    if not path.exists():
        return "File not found."
    return f"--- Source: {source}: {path.name} ---\n{path.read_text()}"


COMMON_TOOLS = [list_files, read_file]
