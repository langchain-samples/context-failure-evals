from typing import Any

from langsmith import Client

client = Client()


def result_match_ratio(outputs: dict[str, Any], reference_outputs: dict[str, Any]) -> float:
    """Compare agent output to ground truth on 4 key fields. Returns 0-1 score."""
    compare_keys = ["ceo_name", "cto_name", "funding_status", "office_locations"]

    score = 0
    for key in compare_keys:
        if key not in reference_outputs and (key not in outputs or outputs[key] is None):
            score += 1
        elif (
            key in reference_outputs
            and key in outputs
            and outputs[key] == reference_outputs[key]
        ):
            score += 1
    return float(score) / len(compare_keys)


def get_metrics_from_experiment(experiment) -> dict[str, float]:
    """Extract average metrics from a LangSmith experiment."""
    results = list(experiment)

    scores = []
    for result in results:
        for eval_result in result["evaluation_results"]["results"]:
            if eval_result.key == "result_match_ratio" and eval_result.score is not None:
                scores.append(eval_result.score)

    avg_metrics = {}
    avg_metrics["result_match_ratio"] = sum(scores) / len(scores) if scores else 0.0

    # Get aggregated stats from the LangSmith session
    session = client.read_project(
        project_name=experiment.experiment_name, include_stats=True
    )
    avg_metrics["latency_p99"] = session.latency_p99.total_seconds()
    avg_metrics["avg_tokens"] = session.total_tokens / len(results) if results else 0
    avg_metrics["avg_cost"] = float(session.total_cost / len(results)) if results else 0.0

    return avg_metrics


def display_metrics(metrics: dict[str, float], title: str) -> None:
    """Print a formatted metrics table."""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")
    print(f"  {'Metric':<25} {'Value':>15}")
    print(f"  {'-' * 40}")
    print(f"  {'Match Ratio':<25} {metrics['result_match_ratio']:>14.1%}")
    print(f"  {'Latency (p99)':<25} {metrics['latency_p99']:>13.1f}s")
    print(f"  {'Avg Tokens':<25} {metrics['avg_tokens']:>15,.0f}")
    cost = f"${metrics['avg_cost']:.4f}"
    print(f"  {'Avg Cost':<25} {cost:>14}")
    print(f"{'=' * 50}\n")


def display_comparison(metrics_a: dict, name_a: str, metrics_b: dict, name_b: str) -> None:
    """Print a side-by-side comparison table."""
    print(f"\n{'=' * 65}")
    print(f"  {'Metric':<25} {name_a:>18} {name_b:>18}")
    print(f"  {'-' * 60}")
    print(f"  {'Match Ratio':<25} {metrics_a['result_match_ratio']:>17.1%} {metrics_b['result_match_ratio']:>17.1%}")
    print(f"  {'Latency (p99)':<25} {metrics_a['latency_p99']:>16.1f}s {metrics_b['latency_p99']:>16.1f}s")
    print(f"  {'Avg Tokens':<25} {metrics_a['avg_tokens']:>17,.0f} {metrics_b['avg_tokens']:>17,.0f}")
    cost_a = f"${metrics_a['avg_cost']:.4f}"
    cost_b = f"${metrics_b['avg_cost']:.4f}"
    print(f"  {'Avg Cost':<25} {cost_a:>17} {cost_b:>17}")
    print(f"{'=' * 65}\n")
