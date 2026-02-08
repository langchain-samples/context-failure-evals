"""Test script for deep agent evaluation."""

from langsmith import aevaluate

from context_distraction.deep import run_deep_agent
from context_distraction.resources.test_tasks import TEST_TASKS, build_partial_task
from context_distraction.tests.setup_datasets import setup_datasets, build_reference_outputs
from context_distraction.tests.evaluators import (
    recall_accuracy_evaluator,
    tool_call_completeness_evaluator,
    tool_call_efficiency_evaluator,
)


async def run_agent(inputs: dict) -> dict:
    """Run deep agent and extract outputs."""
    query = inputs["query"]
    return await run_deep_agent(query)


async def run_experiment(dataset_name: str):
    """
    Run evaluation experiment for deep agent using LangSmith.

    Args:
        dataset_name: Name of the LangSmith dataset to evaluate against

    Returns:
        The experiment result from LangSmith aevaluate
    """
    return await aevaluate(
        run_agent,
        data=dataset_name,
        evaluators=[
            recall_accuracy_evaluator,
            tool_call_completeness_evaluator,
            tool_call_efficiency_evaluator,
        ],
        experiment_prefix="context-distraction-deep-agent",
        metadata={"agent_type": "deep", "model": "gpt-4o-mini"},
        max_concurrency=1,
    )


async def run_local_test(task_index=0, questions=None):
    """
    Run a local test with streaming output for debugging.

    Args:
        task_index: Index of test task to run (0-2 for tasks 1-3)
        questions: Optional list of question numbers to include (e.g., [5, 7, 8])
    """
    task = TEST_TASKS[task_index]

    # Build partial task if specific questions requested
    if questions:
        task = build_partial_task(task, questions)

    reference_outputs = build_reference_outputs(task)

    print(f"LOCAL TEST - {task['name']}", flush=True)

    # Run agent
    inputs = {"query": task["query"]}
    outputs = await run_agent(inputs)

    if outputs.get("error"):
        print(f"\nERROR: {outputs['error']}", flush=True)
        return outputs

    # Run evaluators locally
    print(f"\n{'='*80}", flush=True)
    print("EVALUATION RESULTS", flush=True)
    print(f"{'='*80}\n", flush=True)

    recall_result = recall_accuracy_evaluator(inputs, outputs, reference_outputs)
    print(f"Recall Accuracy: {recall_result['score']:.2%}", flush=True)
    print(f"{recall_result['comment']}\n", flush=True)

    completeness_result = tool_call_completeness_evaluator(inputs, outputs, reference_outputs)
    print(f"Tool Call Completeness: {completeness_result['score']:.2%}", flush=True)
    print(f"{completeness_result['comment']}\n", flush=True)

    efficiency_result = tool_call_efficiency_evaluator(inputs, outputs, reference_outputs)
    print(f"Tool Call Efficiency: {efficiency_result['score']:.2%}")
    print(f"{efficiency_result['comment']}\n", flush=True)

    print(f"\n{'='*80}", flush=True)
    print("FINAL RESPONSE", flush=True)
    print(f"{'='*80}\n", flush=True)
    print(outputs["final_response"][:500] + "..." if len(outputs["final_response"]) > 500 else outputs["final_response"])

    return outputs


def parse_questions(questions_str: str) -> list[int]:
    """Parse questions string like '5,7,8' or '5-8' into list of ints."""
    questions = []
    for part in questions_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            questions.extend(range(int(start), int(end) + 1))
        else:
            questions.append(int(part))
    return questions


if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="Test deep agent")
    parser.add_argument("--langsmith", action="store_true", help="Run evaluation on LangSmith")
    parser.add_argument("--dataset", default="context-distraction-research-slim", help="LangSmith dataset name")
    parser.add_argument("--task", type=int, default=1, help="Test task number (1-3) for local testing")
    parser.add_argument("--questions", "-q", type=str, default=None,
                        help="Specific questions to test, e.g. '5,7,8' or '5-8' or '5'. Default: all questions")

    args = parser.parse_args()

    if args.langsmith:
        # Run LangSmith evaluation
        full_dataset_name = "context-distraction-research"
        slim_dataset_name = "context-distraction-research-slim"
        setup_datasets(full_dataset_name, slim_dataset_name, TEST_TASKS)

        experiment = asyncio.run(run_experiment(args.dataset))
        print(f"\nDeep agent experiment completed: {experiment}")
    else:
        # Run local test
        task_index = args.task - 1  # Convert 1-based to 0-based index
        if task_index < 0 or task_index >= len(TEST_TASKS):
            print(f"Error: Task {args.task} out of range. Valid tasks: 1-{len(TEST_TASKS)}")
            exit(1)

        questions = parse_questions(args.questions) if args.questions else None
        asyncio.run(run_local_test(task_index, questions))
