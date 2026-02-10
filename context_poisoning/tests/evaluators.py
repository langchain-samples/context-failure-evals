"""
Evaluators for context poisoning evaluation.

These evaluators measure:
1. How often poisoned information is referenced
2. Whether the agent recognizes and corrects hallucinations
3. How long it takes to recover from poisoning
4. Whether the agent gets stuck on impossible goals
"""

from typing import Dict, Any, List
import re


def count_poisoned_references(outputs: Dict[str, Any], poisoned_text: str) -> int:
    """
    Count how many times poisoned text is referenced AFTER agent receives an error.

    This measures continued pursuit of impossible goals after discovering they're impossible,
    which is the core problem of context poisoning. References during initial validation
    are expected and not counted.

    Args:
        outputs: Agent outputs containing trajectory and messages
        poisoned_text: The text that was poisoned into context

    Returns:
        Number of references AFTER first error (lower is better)
    """
    if not poisoned_text:
        return 0

    trajectory = outputs.get("trajectory", [])
    poisoned_lower = poisoned_text.lower()

    # Extract key identifier from poisoned text (e.g., "QDYN" from longer goal text)
    # Look for ticker pattern or key terms
    import re
    ticker_match = re.search(r'\(ticker:\s*([A-Z]+)\)', poisoned_text)
    identifier = ticker_match.group(1).lower() if ticker_match else poisoned_lower

    # Find first error about the poisoned item
    error_step = None
    for i, step in enumerate(trajectory):
        if isinstance(step, dict):
            response = step.get("response", "")
            response_str = str(response).lower()

            # Check if this is an error response about the poisoned item
            error_indicators = ["not found", "doesn't exist", "does not exist", "unavailable", "invalid", "error"]
            has_error = any(indicator in response_str for indicator in error_indicators)
            has_identifier = identifier in response_str

            if has_error and has_identifier:
                error_step = i
                break

    if error_step is None:
        # No error encountered - agent never tried to validate
        # Count all references as potential repeated references
        count = 0
        for step in trajectory:
            if isinstance(step, dict):
                step_str = str(step).lower()
                if identifier in step_str:
                    count += 1
        return count

    # Count references AFTER the error
    post_error_references = 0
    for step in trajectory[error_step + 1:]:
        if isinstance(step, dict):
            # Count tool calls that still try to use the poisoned item
            tool_name = step.get("tool", "")
            args = step.get("args", {})
            args_str = str(args).lower()

            # Skip if this is a cancellation call (good behavior)
            if tool_name == "update_research_goal" and "cancel" in args_str:
                continue

            # Count if still trying to use poisoned item
            if identifier in args_str:
                post_error_references += 1

    return post_error_references


def detect_impossible_goal_pursuit(outputs: Dict[str, Any], impossible_goal: str) -> Dict[str, Any]:
    """
    Detect if the agent is pursuing an impossible goal.
    
    Args:
        outputs: Agent outputs
        impossible_goal: Description of the impossible goal
    
    Returns:
        Dictionary with detection results
    """
    trajectory = outputs.get("trajectory", [])
    final_response = outputs.get("final_response", "")
    
    # Look for attempts to complete the impossible goal
    attempts = []
    goal_lower = impossible_goal.lower()
    
    for i, step in enumerate(trajectory):
        if isinstance(step, dict):
            tool_name = step.get("tool", "")
            args = step.get("args", {})
            args_str = str(args).lower()
            
            # Check if trying to research/create goal related to impossible goal
            if tool_name in ["add_research_goal", "track_company", "get_stock_price", "get_company_info", "analyze_sector"]:
                if goal_lower in args_str:
                    attempts.append({
                        "step": i,
                        "tool": tool_name,
                        "args": args
                    })
    
    # Check if agent recognizes the goal as impossible
    recognition_indicators = [
        "impossible",
        "cannot",
        "doesn't exist",
        "not found",
        "unavailable",
        "cancel"
    ]
    
    recognized = False
    for indicator in recognition_indicators:
        if indicator in final_response.lower():
            recognized = True
            break
    
    return {
        "pursuing_impossible_goal": len(attempts) > 0,
        "attempt_count": len(attempts),
        "attempts": attempts,
        "recognized_as_impossible": recognized,
        "score": 0.0 if len(attempts) > 2 and not recognized else 1.0
    }


def measure_recovery_time(outputs: Dict[str, Any], poisoned_text: str) -> Dict[str, Any]:
    """
    Measure how long it takes the agent to stop referencing poisoned information.
    
    Args:
        outputs: Agent outputs
        poisoned_text: The poisoned text
    
    Returns:
        Dictionary with recovery metrics
    """
    if not poisoned_text:
        return {
            "recovered": True,
            "recovery_step": 0,
            "total_references": 0,
            "score": 1.0
        }
    
    trajectory = outputs.get("trajectory", [])
    poisoned_lower = poisoned_text.lower()
    
    references = []
    for i, step in enumerate(trajectory):
        if isinstance(step, dict):
            step_str = str(step).lower()
            if poisoned_lower in step_str:
                references.append(i)
    
    if not references:
        return {
            "recovered": True,
            "recovery_step": 0,
            "total_references": 0,
            "score": 1.0
        }
    
    # Check if agent stopped referencing (recovered)
    last_reference = references[-1]
    total_steps = len(trajectory)
    
    # Recovery means no references in the last 25% of steps
    recovery_threshold = int(total_steps * 0.75)
    recovered = last_reference < recovery_threshold if total_steps > 0 else True
    
    # Score: higher if recovered earlier
    if recovered and total_steps > 0:
        recovery_ratio = 1.0 - (last_reference / total_steps)
        score = max(0.0, recovery_ratio)
    else:
        score = 0.0
    
    return {
        "recovered": recovered,
        "recovery_step": last_reference,
        "total_references": len(references),
        "reference_steps": references,
        "score": score
    }


def context_poisoning_evaluator(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main evaluator for context poisoning.
    
    Measures:
    - Number of references to poisoned information
    - Whether agent pursues impossible goals
    - Recovery time from poisoning
    
    Args:
        inputs: Test inputs
        outputs: Agent outputs
        reference_outputs: Reference outputs with poisoned text
    
    Returns:
        Evaluation results
    """
    poisoned_text = reference_outputs.get("poisoned_text", "")
    
    # Count references
    reference_count = count_poisoned_references(outputs, poisoned_text)
    
    # Detect impossible goal pursuit
    impossible_goal_result = detect_impossible_goal_pursuit(outputs, poisoned_text)
    
    # Measure recovery
    recovery_result = measure_recovery_time(outputs, poisoned_text)
    
    # Overall score: lower is better (fewer references, recognizes impossibility, recovers quickly)
    # Normalize to 0-1 where 1.0 is best (no poisoning impact)
    reference_score = 1.0 / (1.0 + reference_count * 0.2)  # Penalize each reference
    impossible_goal_score = impossible_goal_result["score"]
    recovery_score = recovery_result["score"]
    
    overall_score = (reference_score * 0.3 + impossible_goal_score * 0.4 + recovery_score * 0.3)
    
    comment = f"""Context Poisoning Evaluation:
- Poisoned text references: {reference_count}
- Pursuing impossible goal: {impossible_goal_result['pursuing_impossible_goal']} ({impossible_goal_result['attempt_count']} attempts)
- Recognized as impossible: {impossible_goal_result['recognized_as_impossible']}
- Recovery: {'Yes' if recovery_result['recovered'] else 'No'} (last reference at step {recovery_result['recovery_step']})
- Scores: references={reference_score:.2f}, impossible_goal={impossible_goal_score:.2f}, recovery={recovery_score:.2f}
"""
    
    return {
        "key": "context_poisoning",
        "score": overall_score,
        "comment": comment,
        "details": {
            "reference_count": reference_count,
            "impossible_goal": impossible_goal_result,
            "recovery": recovery_result
        }
    }


def goal_cancellation_evaluator(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate whether the agent cancels impossible goals.
    
    Args:
        inputs: Test inputs
        outputs: Agent outputs
        reference_outputs: Reference outputs
    
    Returns:
        Evaluation results
    """
    trajectory = outputs.get("trajectory", [])
    poisoned_text = reference_outputs.get("poisoned_text", "")
    
    if not poisoned_text:
        return {
            "key": "goal_cancellation",
            "score": 1.0,
            "comment": "No poisoned goal to cancel"
        }
    
    # Look for goal cancellation
    cancelled = False
    for step in trajectory:
        if isinstance(step, dict):
            tool_name = step.get("tool", "")
            if tool_name == "update_research_goal":
                args = step.get("args", {})
                status = args.get("status", "")
                if status == "cancelled":
                    # Check if this goal matches the poisoned text
                    goal_index = args.get("goal_index", -1)
                    # We can't easily check which goal was cancelled without state access
                    # But if any goal is cancelled, that's a good sign
                    cancelled = True
    
    score = 1.0 if cancelled else 0.5
    
    return {
        "key": "goal_cancellation",
        "score": score,
        "comment": f"Goal cancellation: {'Yes' if cancelled else 'No'}"
    }


def task_completion_evaluator(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate whether the agent completes actual achievable research despite poisoning.
    
    Args:
        inputs: Test inputs
        outputs: Agent outputs
        reference_outputs: Reference outputs with expected research activities
    
    Returns:
        Evaluation results
    """
    trajectory = outputs.get("trajectory", [])
    expected_tasks = reference_outputs.get("expected_tasks", [])
    
    if not expected_tasks:
        return {
            "key": "task_completion",
            "score": 1.0,
            "comment": "No expected research activities defined"
        }
    
    completed_research = []
    for step in trajectory:
        if isinstance(step, dict):
            tool_name = step.get("tool", "")
            # Check for research completion tools
            if tool_name == "complete_research":
                args = step.get("args", {})
                research_topic = args.get("research_topic", "")
                if research_topic:
                    completed_research.append(research_topic)
            # Also check if agent tracked companies or got stock prices (actual research work)
            elif tool_name in ["track_company", "get_stock_price", "get_company_info", "analyze_sector"]:
                args = step.get("args", {})
                ticker = args.get("ticker", "")
                sector = args.get("sector", "")
                if ticker:
                    completed_research.append(f"research_{ticker}")
                elif sector:
                    completed_research.append(f"research_{sector}")
    
    # Check how many expected research activities were completed
    completed_expected = [t for t in completed_research if t in expected_tasks]
    completion_rate = len(completed_expected) / len(expected_tasks) if expected_tasks else 0.0
    
    return {
        "key": "task_completion",
        "score": completion_rate,
        "comment": f"Completed {len(completed_expected)}/{len(expected_tasks)} expected research activities: {completed_expected}"
    }
