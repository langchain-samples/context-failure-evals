"""Test script for context distraction evaluation using LangSmith experiments."""

from langsmith import aevaluate
from context_distraction.agent import agent
from context_distraction.resources.test_tasks import TEST_TASKS, build_partial_task
from context_distraction.resources.validation_utils import extract_tool_calls_from_message
from context_distraction.tests.setup_datasets import setup_datasets, build_reference_outputs
from context_distraction.tests.evaluators import (
    recall_accuracy_evaluator,
    tool_call_completeness_evaluator,
    tool_call_efficiency_evaluator,
)

async def run_agent(inputs: dict) -> dict:
    """Run standard agent and extract trajectory using streaming."""
    query = inputs["query"]
    trajectory = []
    final_response = ""
    
    
    # Stream to capture tool calls and final state
    final_state = {}
    all_messages = []
    
    # Stream and extract tool calls from each chunk
    async for chunk in agent.astream(
        {"messages": [("user", query)]},
        stream_mode="updates",
    ):
        # chunk is a tuple: (namespace, data) or just data dict
        if isinstance(chunk, tuple) and len(chunk) >= 2:
            namespace, data = chunk
        elif isinstance(chunk, dict):
            data = chunk
        else:
            continue
        
        # Extract messages from tools and model keys
        if isinstance(data, dict):
            for key in ['tools', 'model']:
                if key in data:
                    msgs = data[key].get('messages', [])
                    all_messages.extend(msgs)
                    
                    # Extract tool calls from messages
                    for msg in msgs:
                        tool_calls = extract_tool_calls_from_message(msg)
                        for tc in tool_calls:
                            trajectory.append(tc)
            
            # Update final state
            final_state.update(data)
    
    # Extract final response from last message
    for msg in reversed(all_messages):
        if isinstance(msg, dict) and msg.get("content"):
            final_response = msg["content"]
            break
        elif hasattr(msg, 'content') and msg.content:
            final_response = msg.content
            break
    
    return {"final_response": final_response, "trajectory": trajectory}


async def run_experiment(agent_type: str, dataset_name: str):
    """
    Run evaluation experiment for specified agent type using LangSmith.
    
    Args:
        agent_type: "standard" (custom agent support removed)
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
        experiment_prefix=f"context-distraction-{agent_type}-agent",
        metadata={"agent_type": agent_type, "model": "gpt-4o-mini"},
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
    # Run agent with streaming
    inputs = {"query": task["query"]}
    outputs = await run_agent(inputs)
    
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
    print(f"Tool Call Efficiency: {efficiency_result['score']:.2%}", flush=True)
    print(f"{efficiency_result['comment']}\n", flush=True)
    
    print(f"\n{'='*80}", flush=True)
    print("FINAL RESPONSE", flush=True)
    print(f"{'='*80}\n", flush=True)
    print(outputs["final_response"][:500] + "..." if len(outputs["final_response"]) > 500 else outputs["final_response"], flush=True)
    
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

    parser = argparse.ArgumentParser(description="Test standard research agent")
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

        standard_experiment = asyncio.run(run_experiment("standard", args.dataset))
        print(f"\nStandard agent experiment completed: {standard_experiment}")
    else:
        # Run local test with streaming
        task_index = args.task - 1  # Convert 1-based to 0-based index
        if task_index < 0 or task_index >= len(TEST_TASKS):
            print(f"Error: Task {args.task} out of range. Valid tasks: 1-{len(TEST_TASKS)}")
            exit(1)

        questions = parse_questions(args.questions) if args.questions else None
        asyncio.run(run_local_test(task_index, questions))