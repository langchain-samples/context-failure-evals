"""
Setup datasets for context poisoning evaluation.
"""

from typing import List, Dict, Any
from langsmith import Client
from context_poisoning.resources.test_cases import TEST_CASES
from context_poisoning.tools import reset_state, inject_poisoned_goal


def create_poisoning_dataset(dataset_name: str, test_cases: List[Dict[str, Any]], client: Client):
    """
    Create or recreate a LangSmith dataset from test cases.
    
    Args:
        dataset_name: Name for the dataset
        test_cases: List of test case dictionaries
        client: LangSmith client
    
    Returns:
        Created dataset
    """
    # Force recreate to ensure correct structure
    try:
        existing = client.read_dataset(dataset_name=dataset_name)
        if existing:
            client.delete_dataset(dataset_id=existing.id)
            print(f"  Deleted existing dataset: {dataset_name}")
            # Small delay to ensure deletion completes
            import time
            time.sleep(0.5)
    except Exception as e:
        # Dataset doesn't exist or couldn't be deleted - try to create anyway
        pass
    
    examples = []
    
    for i, test_case in enumerate(test_cases):
        # Reset state for each test case
        reset_state()
        
        # Inject poisoned goal if specified
        poisoned_goal = test_case.get("poisoned_goal")
        if poisoned_goal:
            inject_poisoned_goal(poisoned_goal)
        
        # Create some initial research state to make the scenario more realistic
        from context_poisoning.tools import track_company_helper, add_research_note_helper
        track_company_helper("AAPL")
        track_company_helper("GOOGL")
        add_research_note_helper("AAPL", "Initial research note on Apple Inc.")
        
        # Get current state for reference
        from context_poisoning.tools import get_current_research_state_helper
        state_result = get_current_research_state_helper()
        
        # Create example
        example = {
            "inputs": {
                "query": test_case["query"]
            },
            "outputs": {
                "poisoned_text": poisoned_goal or "",
                "test_case_name": test_case["name"],
                "expected_behavior": test_case["expected_behavior"],
                "initial_state": state_result.get("state", {})
            },
            "metadata": {
                "test_case": test_case["name"],
                "description": test_case["description"],
                "poisoning_indicators": test_case.get("poisoning_indicators", [])
            }
        }
        
        examples.append(example)
    
    # Create dataset (with retry if conflict occurs)
    try:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description="Context poisoning evaluation test cases for financial research"
        )
    except Exception as e:
        if "already exists" in str(e) or "Conflict" in str(e):
            # If still exists, try to read it instead
            print(f"  Dataset already exists, using existing dataset: {dataset_name}")
            dataset = client.read_dataset(dataset_name=dataset_name)
            # Clear existing examples and recreate
            existing_examples = list(client.list_examples(dataset_id=dataset.id))
            for ex in existing_examples:
                try:
                    client.delete_example(example_id=ex.id)
                except:
                    pass
        else:
            raise
    
    # Add examples
    for example in examples:
        client.create_example(
            inputs=example["inputs"],
            outputs=example["outputs"],
            dataset_id=dataset.id,
            metadata=example["metadata"]
        )
    
    return dataset
