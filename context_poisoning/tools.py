"""
Financial research tools that simulate a research environment.

These tools allow an agent to conduct financial research, track research goals, and maintain state.
The tools are designed to demonstrate context poisoning when hallucinations
about company data, stock prices, or financial metrics make it into the context.
"""

from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
import json
from datetime import datetime, timedelta

# Simulated financial data (in a real system, this would be a database)
_RESEARCH_STATE = {
    "research_goals": [],
    "completed_research": [],
    "companies_tracked": [],
    "sectors_analyzed": [],
    "research_notes": {},
    "current_focus": None,
}

# Available companies for research
_AVAILABLE_COMPANIES = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "market_cap": 3000000000000},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "market_cap": 1800000000000},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "market_cap": 3200000000000},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "market_cap": 1500000000000},
    "TSLA": {"name": "Tesla Inc.", "sector": "Consumer Discretionary", "market_cap": 800000000000},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financial Services", "market_cap": 500000000000},
    "V": {"name": "Visa Inc.", "sector": "Financial Services", "market_cap": 500000000000},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "market_cap": 400000000000},
}

# Available sectors
_AVAILABLE_SECTORS = ["Technology", "Financial Services", "Healthcare", "Consumer Discretionary", "Energy", "Industrials"]


@tool
def get_current_research_state() -> Dict[str, Any]:
    """
    Get the current state of all research goals, completed research, and tracked companies.
    
    Returns:
        Dictionary containing research goals, completed research, companies tracked, sectors analyzed, and notes.
    """
    return {
        "ok": True,
        "state": {
            "research_goals": _RESEARCH_STATE["research_goals"],
            "completed_research": _RESEARCH_STATE["completed_research"],
            "companies_tracked": _RESEARCH_STATE["companies_tracked"],
            "sectors_analyzed": _RESEARCH_STATE["sectors_analyzed"],
            "research_notes": _RESEARCH_STATE["research_notes"],
            "current_focus": _RESEARCH_STATE["current_focus"],
        }
    }


@tool
def get_stock_price(ticker: str) -> Dict[str, Any]:
    """
    Get current stock price for a company ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL")
    
    Returns:
        Current stock price and basic information.
    """
    if ticker not in _AVAILABLE_COMPANIES:
        return {
            "ok": False,
            "error": f"Ticker '{ticker}' not found. Available tickers: {', '.join(_AVAILABLE_COMPANIES.keys())}"
        }
    
    company = _AVAILABLE_COMPANIES[ticker]
    # Simulate price (in real system, would fetch from API)
    base_price = 150.0 if ticker == "AAPL" else 100.0
    price = base_price + (hash(ticker) % 50)
    
    return {
        "ok": True,
        "ticker": ticker,
        "company_name": company["name"],
        "current_price": round(price, 2),
        "sector": company["sector"],
        "market_cap": company["market_cap"],
        "timestamp": datetime.now().isoformat()
    }


@tool
def get_company_info(ticker: str) -> Dict[str, Any]:
    """
    Get detailed company information.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Detailed company information including financials, business description, and key metrics.
    """
    if ticker not in _AVAILABLE_COMPANIES:
        return {
            "ok": False,
            "error": f"Ticker '{ticker}' not found. Available tickers: {', '.join(_AVAILABLE_COMPANIES.keys())}"
        }
    
    company = _AVAILABLE_COMPANIES[ticker]
    
    return {
        "ok": True,
        "ticker": ticker,
        "company_name": company["name"],
        "sector": company["sector"],
        "market_cap": company["market_cap"],
        "description": f"{company['name']} is a leading company in the {company['sector']} sector.",
        "key_metrics": {
            "pe_ratio": 25.5,
            "dividend_yield": 0.5,
            "revenue_growth": 8.5,
        }
    }


@tool
def analyze_sector(sector: str) -> Dict[str, Any]:
    """
    Analyze a specific sector with market trends and key companies.
    
    Args:
        sector: Sector name (e.g., "Technology", "Financial Services")
    
    Returns:
        Sector analysis including trends, key companies, and market outlook.
    """
    if sector not in _AVAILABLE_SECTORS:
        return {
            "ok": False,
            "error": f"Sector '{sector}' not found. Available sectors: {', '.join(_AVAILABLE_SECTORS)}"
        }
    
    # Find companies in this sector
    companies_in_sector = [ticker for ticker, info in _AVAILABLE_COMPANIES.items() if info["sector"] == sector]
    
    if sector not in _RESEARCH_STATE["sectors_analyzed"]:
        _RESEARCH_STATE["sectors_analyzed"].append(sector)
    
    return {
        "ok": True,
        "sector": sector,
        "companies": companies_in_sector,
        "market_trend": "Growing",
        "key_insights": [
            f"The {sector} sector shows strong growth potential",
            f"Key companies include: {', '.join(companies_in_sector[:3])}",
            "Market conditions are favorable for investment"
        ],
        "outlook": "Positive"
    }


@tool
def add_research_goal(goal_description: str, priority: int = 1) -> Dict[str, Any]:
    """
    Add a research goal to the goals list.
    
    Args:
        goal_description: Description of the research goal
        priority: Priority level (1-5, where 5 is highest)
    
    Returns:
        Confirmation and updated goals list.
    """
    goal = {
        "description": goal_description,
        "priority": priority,
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    _RESEARCH_STATE["research_goals"].append(goal)
    
    return {
        "ok": True,
        "message": f"Research goal added: {goal_description}",
        "goals": _RESEARCH_STATE["research_goals"]
    }


@tool
def update_research_goal(goal_index: int, new_description: Optional[str] = None, new_priority: Optional[int] = None, status: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing research goal.
    
    Args:
        goal_index: Index of the goal to update (0-based)
        new_description: New description (optional)
        new_priority: New priority (optional)
        status: New status - "active", "completed", or "cancelled" (optional)
    
    Returns:
        Confirmation and updated goal.
    """
    if goal_index < 0 or goal_index >= len(_RESEARCH_STATE["research_goals"]):
        return {
            "ok": False,
            "error": f"Goal index {goal_index} out of range. Current goals count: {len(_RESEARCH_STATE['research_goals'])}"
        }
    
    goal = _RESEARCH_STATE["research_goals"][goal_index]
    if new_description:
        goal["description"] = new_description
    if new_priority:
        goal["priority"] = new_priority
    if status:
        goal["status"] = status
    
    return {
        "ok": True,
        "message": f"Research goal {goal_index} updated",
        "goal": goal
    }


@tool
def track_company(ticker: str) -> Dict[str, Any]:
    """
    Add a company to the tracking list.
    
    Args:
        ticker: Stock ticker symbol to track
    
    Returns:
        Confirmation and updated tracking list.
    """
    if ticker not in _AVAILABLE_COMPANIES:
        return {
            "ok": False,
            "error": f"Ticker '{ticker}' not found. Available tickers: {', '.join(_AVAILABLE_COMPANIES.keys())}"
        }
    
    if ticker not in _RESEARCH_STATE["companies_tracked"]:
        _RESEARCH_STATE["companies_tracked"].append(ticker)
    
    return {
        "ok": True,
        "message": f"Now tracking {ticker} ({_AVAILABLE_COMPANIES[ticker]['name']})",
        "tracked_companies": _RESEARCH_STATE["companies_tracked"]
    }


@tool
def add_research_note(topic: str, note: str) -> Dict[str, Any]:
    """
    Add a research note about a specific topic.
    
    Args:
        topic: Topic or company ticker the note is about
        note: The research note content
    
    Returns:
        Confirmation and updated notes.
    """
    if topic not in _RESEARCH_STATE["research_notes"]:
        _RESEARCH_STATE["research_notes"][topic] = []
    
    _RESEARCH_STATE["research_notes"][topic].append({
        "note": note,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "ok": True,
        "message": f"Note added for {topic}",
        "notes_count": len(_RESEARCH_STATE["research_notes"][topic])
    }


@tool
def complete_research(research_topic: str) -> Dict[str, Any]:
    """
    Mark a research topic as completed.
    
    Args:
        research_topic: The research topic that was completed
    
    Returns:
        Confirmation and updated completed research list.
    """
    if research_topic not in _RESEARCH_STATE["completed_research"]:
        _RESEARCH_STATE["completed_research"].append(research_topic)
    
    return {
        "ok": True,
        "message": f"Research on '{research_topic}' marked as completed",
        "completed_research": _RESEARCH_STATE["completed_research"]
    }


@tool
def create_research_summary() -> Dict[str, Any]:
    """
    Create a summary of current research progress, goals, and findings.
    This tool is designed to demonstrate context poisoning - if the summary
    contains hallucinations, they can poison the context.
    
    Returns:
        Summary of current research state, goals, and progress.
    """
    active_goals = [g for g in _RESEARCH_STATE["research_goals"] if g["status"] == "active"]
    completed = _RESEARCH_STATE["completed_research"]
    tracked = _RESEARCH_STATE["companies_tracked"]
    sectors = _RESEARCH_STATE["sectors_analyzed"]
    
    summary = {
        "active_research_goals": [g["description"] for g in active_goals],
        "completed_research": completed,
        "companies_tracked": tracked,
        "sectors_analyzed": sectors,
        "current_focus": _RESEARCH_STATE["current_focus"],
        "next_steps": []
    }
    
    # Generate next steps based on goals
    for goal in active_goals:
        summary["next_steps"].append(f"Work towards: {goal['description']}")
    
    return {
        "ok": True,
        "summary": summary,
        "summary_text": json.dumps(summary, indent=2)
    }


def reset_state():
    """Reset the research state (for testing)."""
    global _RESEARCH_STATE
    _RESEARCH_STATE = {
        "research_goals": [],
        "completed_research": [],
        "companies_tracked": [],
        "sectors_analyzed": [],
        "research_notes": {},
        "current_focus": None,
    }


def inject_poisoned_goal(poisoned_description: str):
    """
    Inject a poisoned goal into the state to simulate context poisoning.
    This simulates what happens when a hallucination makes it into the research goals.
    
    Args:
        poisoned_description: The hallucinated/impossible research goal description
    """
    goal = {
        "description": poisoned_description,
        "priority": 5,  # High priority to make it more likely to be referenced
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    _RESEARCH_STATE["research_goals"].append(goal)


# Helper functions for direct state manipulation (for testing/setup)
def _track_company_helper(ticker: str):
    """Helper function to track companies directly (bypasses tool decorator)."""
    if ticker in _AVAILABLE_COMPANIES and ticker not in _RESEARCH_STATE["companies_tracked"]:
        _RESEARCH_STATE["companies_tracked"].append(ticker)


def _add_research_note_helper(topic: str, note: str):
    """Helper function to add research notes directly (bypasses tool decorator)."""
    if topic not in _RESEARCH_STATE["research_notes"]:
        _RESEARCH_STATE["research_notes"][topic] = []
    _RESEARCH_STATE["research_notes"][topic].append({
        "note": note,
        "timestamp": datetime.now().isoformat()
    })


def _get_current_research_state_helper() -> Dict[str, Any]:
    """Helper function to get current research state directly (bypasses tool decorator)."""
    return {
        "ok": True,
        "state": {
            "research_goals": _RESEARCH_STATE["research_goals"],
            "completed_research": _RESEARCH_STATE["completed_research"],
            "companies_tracked": _RESEARCH_STATE["companies_tracked"],
            "sectors_analyzed": _RESEARCH_STATE["sectors_analyzed"],
            "research_notes": _RESEARCH_STATE["research_notes"],
            "current_focus": _RESEARCH_STATE["current_focus"],
        }
    }


# Export all tools
all_tools = [
    get_current_research_state,
    get_stock_price,
    get_company_info,
    analyze_sector,
    add_research_goal,
    update_research_goal,
    track_company,
    add_research_note,
    complete_research,
    create_research_summary,
]

# Export helper functions for direct state manipulation (for testing/setup)
track_company_helper = _track_company_helper
add_research_note_helper = _add_research_note_helper
get_current_research_state_helper = _get_current_research_state_helper
