from pathlib import Path

from langchain_core.tools import tool

DATASETS_DIR = Path(__file__).resolve().parent.parent / "datasets"

SUBAGENT_PROMPT = """
You are part of a team of analysts researching a company.
Your task is to research the company using the datasource {datasource}.

Research the company to find: CEO, CTO, headcount, funding status, total raised, founding year, office location.

Follow this workflow:
1. Only consider data files from the datasource {datasource}. Tool calls must include a source parameter with the value {datasource}.
2. Use your list tool to discover what data files are available for the company from the datasource {datasource},
3. Read files in parallel using your read tool and extract the relevant information from the source.

The output of your research is used to assemble a report by a coordinator agent.

IMPORTANT: If you don't call a tool, explain why you didn't call it.
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
    return f"--- {path.name} ---\n{path.read_text()}"


COMMON_TOOLS = [list_files, read_file]
