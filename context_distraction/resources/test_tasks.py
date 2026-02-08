"""
Test tasks for context distraction evaluation.

Each task is designed to require many operations and test the agent's ability
to maintain accuracy across long context histories. Each task focuses on
different domains to ensure variety.
"""

from context_distraction.resources.expected_calculations import (
    get_domain_base_fact,
    get_compound_growth_10yr,
    get_cba_npv_10pct,
    get_correlation_market_size_vs_growth,
    calculate_correlation_ratio_to_avg,
    get_investment_priority_rank,
    get_risk_adjusted_npv,
    get_weighted_investment_score,
    get_strategic_priority_rank,
    calculate_npv_ratio,
    calculate_weighted_avg_growth,
    calculate_present_value_year5,
    calculate_market_share_percentage,
    calculate_total_investment_sum,
    calculate_growth_multiple_power,
    calculate_discount_factor_year7,
    calculate_npv_difference,
    calculate_weighted_avg_npv,
    calculate_roi_ratio,
)

# All topics used across test tasks
topics_all = ["renewable_energy", "artificial_intelligence", "electric_vehicles", "quantum_computing", "biotechnology"]


def build_partial_task(task: dict, questions: list[int]) -> dict:
    """
    Build a partial task with only specified questions.

    Args:
        task: Original task dict from TEST_TASKS
        questions: List of question numbers (1-indexed) to include, e.g. [5, 7, 8]

    Returns:
        Modified task dict with only the specified questions
    """
    # Get raw questions from the task
    raw_questions = task["raw_questions"]

    # Filter to only requested questions (convert to 0-indexed)
    selected_questions = [(q, raw_questions[q - 1]) for q in questions if 1 <= q <= len(raw_questions)]

    # Build the recall_questions string with renumbered questions
    recall_questions_str = "\n".join([
        f"{i+1}. {q_text}" for i, (_, q_text) in enumerate(selected_questions)
    ])

    # Build JSON template
    json_answers = ",\n    ".join([f'"{i+1}": <answer to question {i+1}>' for i in range(len(selected_questions))])

    # Build modified query - simplified to focus on questions
    query = f"""You are analyzing investment opportunities across {task['num_domains']} technology sectors: {task['domains_str']}.

## Background
You have access to research tools that can provide:
- Market statistics (market size, growth rates, investment levels, correlations)
- Cost-benefit analysis data (NPV, ROI, yearly benefits with discount rates)
- Domain-specific metrics

## Questions to Answer
{recall_questions_str}

## Output Format
Return your analysis with a JSON section containing answers:
```json
{{
  "answers": {{
    {json_answers}
  }}
}}
```

Use the research and calculation tools to find accurate values. Do not estimate - look up or calculate the exact values."""

    # Build expected answers mapping (renumbered)
    expected_answers = {
        i + 1: task["expected_answers"][orig_q]
        for i, (orig_q, _) in enumerate(selected_questions)
    }

    # Build recall_questions list (renumbered)
    recall_questions = [
        task["recall_questions"][orig_q - 1]
        for orig_q, _ in selected_questions
    ]

    return {
        **task,
        "name": f"{task['name']} (Q{','.join(map(str, questions))})",
        "query": query,
        "expected_answers": expected_answers,
        "recall_questions": recall_questions,
        "original_questions": questions,  # Track which original questions were included
    }


# Base task template
BASE_TASK_QUERY = """You are leading a multi-billion dollar investment analysis across {num_domains} technology sectors.

Research domains: {domains}.

For each domain, conduct comprehensive research including:
- Gathering key statistics and market data
- Consulting multiple expert opinions
- Analyzing relevant case studies
- Reviewing historical trends across key years
- Calculating compound growth projections (10-year forecast)
- Running correlation analyses between market size and growth rates
- Conducting cost-benefit analysis with 10% discount rate
- Aggregating statistics by region
- Comparing domains against each other
- Synthesizing comprehensive research findings

After completing research for all domains, create a final synthesis that:
- Compares all domains across multiple dimensions
- Performs investment portfolio optimization using NPV rankings
- Provides geographic market aggregation showing regional patterns
- Creates financial projections using compound growth calculations
- Calculates risk-adjusted return metrics

IMPORTANT: Your analysis must answer these specific questions:
{recall_questions}

CRITICAL OUTPUT FORMAT:
Your final response MUST be valid Markdown with a JSON section at the end containing the answers to all questions in this exact structure:
```json
{{
  "answers": {{
    "1": <answer to question 1>,
    "2": <answer to question 2>,
    "3": <answer to question 3>,
    "4": <answer to question 4>,
    "5": <answer to question 5>,
    "6": <answer to question 6>,
    "7": <answer to question 7>,
    "8": <answer to question 8>,
    "9": <answer to question 9>
  }}
}}
```

Be thorough and ensure all answers are accurate and complete."""

# Test task variations - each focuses on different primary domains with diverse Q5-Q9
TEST_TASKS = [
    {
        "name": "Task 1: 5 Domains - Focus on Renewable Energy",
        "primary_domain": "renewable_energy",
        "secondary_domain": "artificial_intelligence",
        "num_domains": 5,
        "domains_str": "renewable energy, artificial intelligence, electric vehicles, quantum computing, and biotechnology",
        "raw_questions": [
            "What was the global installed capacity in gigawatts for renewable energy?",
            "What is the global AI market size in billions of USD?",
            "What is the 10-year compound growth final value for the renewable energy market?",
            "What was the NPV calculated for the renewable energy cost-benefit analysis project with 10% discount rate?",
            "What is the ratio of renewable energy's correlation (between market size and growth rate) to the average correlation across all 5 domains?",
            "What is the ratio of renewable energy cost-benefit analysis NPV to artificial intelligence cost-benefit analysis NPV (both at 10% discount rate)?",
            "What is the present value of year 5 benefits for the renewable energy cost-benefit analysis project at 10% discount rate?",
            "What percentage of total market size across all domains does renewable energy represent?",
            "What is the weighted average of cost-benefit analysis NPVs across all domains, weighted by investment amounts?",
        ],
        "query": BASE_TASK_QUERY.format(
            num_domains=5,
            domains="renewable energy, artificial intelligence, electric vehicles, quantum computing, and biotechnology",
            recall_questions="\n".join([
                "1. What was the global installed capacity in gigawatts for renewable energy?",
                "2. What is the global AI market size in billions of USD?",
                "3. What is the 10-year compound growth final value for the renewable energy market?",
                "4. What was the NPV calculated for the renewable energy cost-benefit analysis project with 10% discount rate?",
                "5. What is the ratio of renewable energy's correlation (between market size and growth rate) to the average correlation across all 5 domains?",
                "6. What is the ratio of renewable energy cost-benefit analysis NPV to artificial intelligence cost-benefit analysis NPV (both at 10% discount rate)?",
                "7. What is the present value of year 5 benefits for the renewable energy cost-benefit analysis project at 10% discount rate?",
                "8. What percentage of total market size across all domains does renewable energy represent?",
                "9. What is the weighted average of cost-benefit analysis NPVs across all domains, weighted by investment amounts?",
            ]),
        ),
        "topics": topics_all,
        "recall_questions": [
            f"What was the global installed capacity in gigawatts for renewable energy? (Expected: {get_domain_base_fact('renewable_energy')} GW)",
            f"What is the global AI market size in billions of USD? (Expected: {get_domain_base_fact('artificial_intelligence')} billion)",
            f"What was the calculated 10-year compound growth final value for renewable energy? (Expected: {get_compound_growth_10yr('renewable_energy')})",
            f"What was the NPV calculated for renewable energy CBA with 10% discount rate? (Expected: {get_cba_npv_10pct('renewable_energy')})",
            f"What is the ratio of renewable energy's correlation to average correlation across all domains? (Expected: {calculate_correlation_ratio_to_avg('renewable_energy', topics_all)})",
            f"What is the ratio of renewable energy NPV to artificial intelligence NPV (both at 10% discount)? (Expected: {calculate_npv_ratio('renewable_energy', 'artificial_intelligence')})",
            f"What is the present value of year 5 benefits for renewable energy at 10% discount rate? (Expected: {calculate_present_value_year5('renewable_energy')})",
            f"What percentage of total market size across all domains does renewable energy represent? (Expected: {calculate_market_share_percentage('renewable_energy', topics_all)}%)",
            f"What is the weighted average of NPVs across all domains, weighted by investment amounts? (Expected: {calculate_weighted_avg_npv(topics_all)})",
        ],
        "expected_answers": {
            1: str(get_domain_base_fact('renewable_energy')),
            2: str(get_domain_base_fact('artificial_intelligence')),
            3: str(get_compound_growth_10yr('renewable_energy')),
            4: str(get_cba_npv_10pct('renewable_energy')),
            5: str(calculate_correlation_ratio_to_avg('renewable_energy', topics_all)),
            6: str(calculate_npv_ratio('renewable_energy', 'artificial_intelligence')),
            7: str(calculate_present_value_year5('renewable_energy')),
            8: str(calculate_market_share_percentage('renewable_energy', topics_all)),
            9: str(calculate_weighted_avg_npv(topics_all)),
        },
        "stats_count": 5,
        "expert_count": 3,
        "case_count": 2,
        "year_count": 3,
        "compare_count": 2,
    },
    {
        "name": "Task 2: 5 Domains - Focus on Electric Vehicles",
        "primary_domain": "electric_vehicles",
        "secondary_domain": "biotechnology",
        "num_domains": 5,
        "domains_str": "renewable energy, artificial intelligence, electric vehicles, quantum computing, and biotechnology",
        "raw_questions": [
            "What was the battery cost per kWh for electric vehicles?",
            "What is the global biotechnology market size in billions of USD?",
            "What was the calculated 10-year compound growth final value for electric vehicles?",
            "What was the NPV calculated for the electric vehicles cost-benefit analysis project with 10% discount rate?",
            "What was the investment priority ranking for electric vehicles among all domains based on weighted scores?",
            "What is the difference between electric vehicles cost-benefit analysis NPV and biotechnology cost-benefit analysis NPV (both at 10% discount rate)?",
            "What is the ratio of electric vehicles cost-benefit analysis ROI to biotechnology cost-benefit analysis ROI (both at 10% discount rate)?",
            "What is the sum of all domain investments in billions USD?",
            "What is the growth multiple (compound_growth_10yr / market_size) for electric vehicles raised to the power of 2?",
        ],
        "query": BASE_TASK_QUERY.format(
            num_domains=5,
            domains="renewable energy, artificial intelligence, electric vehicles, quantum computing, and biotechnology",
            recall_questions="\n".join([
                "1. What was the battery cost per kWh for electric vehicles?",
                "2. What is the global biotechnology market size in billions of USD?",
                "3. What was the calculated 10-year compound growth final value for electric vehicles?",
                "4. What was the NPV calculated for the electric vehicles cost-benefit analysis project with 10% discount rate?",
                "5. What was the investment priority ranking for electric vehicles among all domains based on weighted scores?",
                "6. What is the difference between electric vehicles cost-benefit analysis NPV and biotechnology cost-benefit analysis NPV (both at 10% discount rate)?",
                "7. What is the ratio of electric vehicles cost-benefit analysis ROI to biotechnology cost-benefit analysis ROI (both at 10% discount rate)?",
                "8. What is the sum of all domain investments in billions USD?",
                "9. What is the growth multiple (compound_growth_10yr / market_size) for electric vehicles raised to the power of 2?",
            ]),
        ),
        "topics": topics_all,
        "recall_questions": [
            f"What was the battery cost per kWh for electric vehicles? (Expected: {get_domain_base_fact('electric_vehicles')} $/kWh)",
            f"What is the global biotechnology market size in billions of USD? (Expected: {get_domain_base_fact('biotechnology')} billion)",
            f"What was the calculated 10-year compound growth final value for electric vehicles? (Expected: {get_compound_growth_10yr('electric_vehicles')})",
            f"What was the NPV calculated for electric vehicles CBA with 10% discount rate? (Expected: {get_cba_npv_10pct('electric_vehicles')})",
            f"What was the investment priority ranking for electric vehicles among all domains based on weighted scores? (Expected: Rank {get_investment_priority_rank('electric_vehicles')})",
            f"What is the difference between electric vehicles NPV and biotechnology NPV (both at 10% discount)? (Expected: {calculate_npv_difference('electric_vehicles', 'biotechnology')})",
            f"What is the ratio of electric vehicles ROI to biotechnology ROI (both at 10% discount)? (Expected: {calculate_roi_ratio('electric_vehicles', 'biotechnology')})",
            f"What is the sum of all domain investments in billions USD? (Expected: {calculate_total_investment_sum(topics_all)})",
            f"What is the growth multiple (compound_growth_10yr / market_size) for electric vehicles raised to the power of 2? (Expected: {calculate_growth_multiple_power('electric_vehicles')})",
        ],
        "expected_answers": {
            1: str(get_domain_base_fact('electric_vehicles')),
            2: str(get_domain_base_fact('biotechnology')),
            3: str(get_compound_growth_10yr('electric_vehicles')),
            4: str(get_cba_npv_10pct('electric_vehicles')),
            5: str(get_investment_priority_rank('electric_vehicles')),
            6: str(calculate_npv_difference('electric_vehicles', 'biotechnology')),
            7: str(calculate_roi_ratio('electric_vehicles', 'biotechnology')),
            8: str(calculate_total_investment_sum(topics_all)),
            9: str(calculate_growth_multiple_power('electric_vehicles')),
        },
        "stats_count": 6,
        "expert_count": 4,
        "case_count": 3,
        "year_count": 4,
        "compare_count": 2,
    },
    {
        "name": "Task 3: 5 Domains - Focus on Biotechnology",
        "primary_domain": "biotechnology",
        "secondary_domain": "renewable_energy",
        "num_domains": 5,
        "domains_str": "renewable energy, artificial intelligence, electric vehicles, quantum computing, and biotechnology",
        "raw_questions": [
            "What is the global biotechnology market size in billions of USD?",
            "What was the global installed capacity in gigawatts for renewable energy?",
            "What was the calculated 10-year compound growth final value for biotechnology?",
            "What was the NPV calculated for the biotechnology cost-benefit analysis project with 10% discount rate?",
            "What was the weighted investment score calculated for biotechnology based on comparison across all domains?",
            "What is the present value of year 5 benefits for the biotechnology cost-benefit analysis project at 10% discount rate?",
            "What percentage of total market size across all domains does biotechnology represent?",
            "What is the weighted average of cost-benefit analysis NPVs across all domains, weighted by investment amounts?",
            "What is the growth multiple (compound_growth_10yr / market_size) for biotechnology raised to the power of 2?",
        ],
        "query": BASE_TASK_QUERY.format(
            num_domains=5,
            domains="renewable energy, artificial intelligence, electric vehicles, quantum computing, and biotechnology",
            recall_questions="\n".join([
                "1. What is the global biotechnology market size in billions of USD?",
                "2. What was the global installed capacity in gigawatts for renewable energy?",
                "3. What was the calculated 10-year compound growth final value for biotechnology?",
                "4. What was the NPV calculated for the biotechnology cost-benefit analysis project with 10% discount rate?",
                "5. What was the weighted investment score calculated for biotechnology based on comparison across all domains?",
                "6. What is the present value of year 5 benefits for the biotechnology cost-benefit analysis project at 10% discount rate?",
                "7. What percentage of total market size across all domains does biotechnology represent?",
                "8. What is the weighted average of cost-benefit analysis NPVs across all domains, weighted by investment amounts?",
                "9. What is the growth multiple (compound_growth_10yr / market_size) for biotechnology raised to the power of 2?",
            ]),
        ),
        "topics": topics_all,
        "recall_questions": [
            f"What is the global biotechnology market size in billions of USD? (Expected: {get_domain_base_fact('biotechnology')} billion)",
            f"What was the global installed capacity in gigawatts for renewable energy? (Expected: {get_domain_base_fact('renewable_energy')} GW)",
            f"What was the calculated 10-year compound growth final value for biotechnology? (Expected: {get_compound_growth_10yr('biotechnology')})",
            f"What was the NPV calculated for biotechnology CBA with 10% discount rate? (Expected: {get_cba_npv_10pct('biotechnology')})",
            f"What was the weighted investment score calculated for biotechnology based on comparison across all domains? (Expected: {get_weighted_investment_score('biotechnology')})",
            f"What is the present value of year 5 benefits for biotechnology at 10% discount rate? (Expected: {calculate_present_value_year5('biotechnology')})",
            f"What percentage of total market size across all domains does biotechnology represent? (Expected: {calculate_market_share_percentage('biotechnology', topics_all)}%)",
            f"What is the weighted average of NPVs across all domains, weighted by investment amounts? (Expected: {calculate_weighted_avg_npv(topics_all)})",
            f"What is the growth multiple (compound_growth_10yr / market_size) for biotechnology raised to the power of 2? (Expected: {calculate_growth_multiple_power('biotechnology')})",
        ],
        "expected_answers": {
            1: str(get_domain_base_fact('biotechnology')),
            2: str(get_domain_base_fact('renewable_energy')),
            3: str(get_compound_growth_10yr('biotechnology')),
            4: str(get_cba_npv_10pct('biotechnology')),
            5: str(get_weighted_investment_score('biotechnology')),
            6: str(calculate_present_value_year5('biotechnology')),
            7: str(calculate_market_share_percentage('biotechnology', topics_all)),
            8: str(calculate_weighted_avg_npv(topics_all)),
            9: str(calculate_growth_multiple_power('biotechnology')),
        },
        "stats_count": 7,
        "expert_count": 5,
        "case_count": 4,
        "year_count": 5,
        "compare_count": 3,
    },
]
