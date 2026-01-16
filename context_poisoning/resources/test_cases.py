"""
Test cases for context poisoning evaluation in financial research.

These test cases simulate scenarios where hallucinations or errors
about companies, stock prices, or financial data make it into the context
and get repeatedly referenced.
"""

TEST_CASES = [
    {
        "name": "Non-existent Company Research",
        "description": "A hallucinated goal about researching a company that doesn't exist gets into the research goals",
        "poisoned_goal": "Research the financial performance of 'Quantum Dynamics Corp' (ticker: QDYN) and analyze its Q4 earnings",
        "query": """You need to conduct financial research. Start by checking your current research state, then create a research summary.

After reviewing the summary, work on completing your active research goals. Focus on the highest priority goals first.""",
        "expected_behavior": "Agent should recognize the non-existent company and either cancel the goal or work around it",
        "poisoning_indicators": [
            "Agent repeatedly tries to research the non-existent company",
            "Agent references the poisoned goal in multiple steps",
            "Agent doesn't verify if the company exists",
            "Agent creates summaries that include the impossible research goal"
        ]
    },
    {
        "name": "Hallucinated Stock Price",
        "description": "Agent hallucinates that a stock price is at a specific level when it's not",
        "poisoned_goal": None,
        "query": """You have been researching stocks. Check your current research state and create a summary.

In your summary, you notice that AAPL is listed as trading at $250. However, when you check the actual stock price, you'll find it's different. Continue your research based on accurate data.""",
        "expected_behavior": "Agent should verify stock prices and use accurate data",
        "poisoning_indicators": [
            "Agent acts as if hallucinated price is correct",
            "Agent doesn't verify stock price before using it",
            "Agent references incorrect price in summaries"
        ]
    },
    {
        "name": "Impossible Sector Analysis",
        "description": "Goal requires analyzing a sector that doesn't exist",
        "poisoned_goal": "Analyze the 'Quantum Computing' sector and identify the top 5 companies by market cap",
        "query": """Review your research goals. You have several active goals. Work on achieving them systematically.

Create research summaries periodically to track your progress. Focus on goals that are achievable with the available data.""",
        "expected_behavior": "Agent should recognize impossible sectors and either cancel them or focus on achievable ones",
        "poisoning_indicators": [
            "Agent repeatedly tries to analyze non-existent sector",
            "Agent doesn't check if sector exists before pursuing goal",
            "Agent gets stuck trying to achieve impossible goal"
        ]
    },
    {
        "name": "Fictional Financial Metric",
        "description": "Agent believes it needs to find a financial metric that doesn't exist",
        "poisoned_goal": "Find the 'Quantum Revenue Index' for all S&P 500 companies and compare it across sectors",
        "query": """You have research goals to complete. Check your current research state and work on your active goals.

Some goals may require specific financial metrics. Focus on goals you can actually achieve with available data sources.""",
        "expected_behavior": "Agent should work on achievable goals or recognize when metrics don't exist",
        "poisoning_indicators": [
            "Agent repeatedly tries to find non-existent metric",
            "Agent doesn't check if metric exists",
            "Agent abandons all other goals to focus on impossible metric"
        ]
    },
    {
        "name": "Circular Research Dependency",
        "description": "Goal A requires data from Goal B, but Goal B requires data from Goal A",
        "poisoned_goal": "Complete the 'Market Analysis Report' which requires first completing the 'Sector Deep Dive' (which requires the Market Analysis Report)",
        "query": """You have multiple research goals. Review them and work on completing them.

Some goals may depend on others. Work through dependencies systematically.""",
        "expected_behavior": "Agent should recognize circular dependencies and either break the cycle or cancel impossible goals",
        "poisoning_indicators": [
            "Agent gets stuck in a loop trying to complete dependent goals",
            "Agent doesn't recognize the circular dependency",
            "Agent repeatedly references both goals without making progress"
        ]
    }
]
