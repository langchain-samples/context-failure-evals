"""
Answer storage middleware that cleans up calculation history when answers are stored.

This middleware watches for `store_answer` tool calls and removes previous
calculation-related tool calls from message history, keeping only the stored answer.
"""

from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage, RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from typing import Dict, Any, List, Tuple

# Tool names that are considered "calculation" tools and should be cleaned up
CALCULATION_TOOL_NAMES = {
    "calculate_discount_factor",
    "calculate_present_value",
    "calculate_percentage",
    "calculate_weighted_average",
    "calculate_ratio",
    "calculate_power",
    "calculate_sum",
    "calculate_compound_growth",
    "calculate_cost_benefit_analysis",
    "analyze_correlation",
    "get_historical_trends",
}


def _get_tool_name(tc: Any) -> str:
    """Extract tool name from a tool call."""
    return tc.get("name", "") if isinstance(tc, dict) else getattr(tc, "name", "")


def _get_tool_id(tc: Any) -> str:
    """Extract tool ID from a tool call."""
    return tc.get("id", "") if isinstance(tc, dict) else getattr(tc, "id", "")


def _get_tool_args(tc: Any) -> Dict[str, Any]:
    """Extract tool args from a tool call."""
    return tc.get("args", {}) if isinstance(tc, dict) else getattr(tc, "args", {})


def _extract_tool_calls(msg: Any) -> List[Any]:
    """Extract tool calls from an AI message."""
    if isinstance(msg, dict):
        return msg.get("tool_calls", [])
    elif isinstance(msg, AIMessage) and hasattr(msg, 'tool_calls'):
        return msg.tool_calls or []
    return []


def _is_store_answer_call(msg: Any) -> bool:
    """Check if a message contains a store_answer tool call."""
    tool_calls = _extract_tool_calls(msg)
    return any(_get_tool_name(tc) == "store_answer" for tc in tool_calls)


def _filter_calculation_tool_calls(tool_calls: List[Any]) -> Tuple[List[Any], set]:
    """Filter out calculation tool calls. Returns (filtered_calls, calculation_ids)."""
    filtered = []
    calculation_ids = set()
    
    for tc in tool_calls:
        tool_name = _get_tool_name(tc)
        tool_id = _get_tool_id(tc)
        
        if tool_name in CALCULATION_TOOL_NAMES:
            calculation_ids.add(tool_id)
        else:
            filtered.append(tc)
    
    return filtered, calculation_ids


def _create_filtered_ai_message(msg: Any, filtered_tool_calls: List[Any]) -> Any:
    """Create a new AI message with only the filtered tool calls."""
    if isinstance(msg, dict):
        new_msg = msg.copy()
        new_msg["tool_calls"] = filtered_tool_calls
        return new_msg
    elif isinstance(msg, AIMessage):
        return AIMessage(
            content=msg.content,
            tool_calls=filtered_tool_calls,
            id=getattr(msg, 'id', None),
            additional_kwargs=getattr(msg, 'additional_kwargs', {})
        )
    return msg


def _get_tool_call_id_from_message(msg: Any) -> str:
    """Extract tool_call_id from a ToolMessage."""
    if isinstance(msg, dict):
        return msg.get("tool_call_id", "")
    elif isinstance(msg, ToolMessage):
        return getattr(msg, "tool_call_id", "")
    return ""


def _is_system_or_user(msg: Any) -> bool:
    """Check if message is a system or user message."""
    return isinstance(msg, (SystemMessage, HumanMessage)) or (
        isinstance(msg, dict) and msg.get("type") in ("system", "human")
    )


def _is_ai_message(msg: Any) -> bool:
    """Check if message is an AI message."""
    return isinstance(msg, AIMessage) or (isinstance(msg, dict) and msg.get("type") == "ai")


def _is_tool_message(msg: Any) -> bool:
    """Check if message is a ToolMessage."""
    return isinstance(msg, ToolMessage) or (isinstance(msg, dict) and msg.get("type") == "tool")


def _track_tool_calls(messages: List[Any], existing_tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Track all tool calls from messages for evaluation."""
    all_tool_calls = existing_tool_calls.copy()
    existing_ids = {tc.get("id") for tc in all_tool_calls}
    
    for msg in messages:
        tool_calls = _extract_tool_calls(msg)
        for tc in tool_calls:
            tool_id = _get_tool_id(tc)
            if tool_id and tool_id not in existing_ids:
                all_tool_calls.append({
                    "name": _get_tool_name(tc),
                    "args": _get_tool_args(tc),
                    "id": tool_id
                })
                existing_ids.add(tool_id)
    
    return all_tool_calls


def _filter_messages(messages: List[Any], calculation_tool_call_ids: set, up_to_index: int) -> List[Any]:
    """Filter messages up to index, removing calculation tool calls and their ToolMessages."""
    cleaned = []
    i = 0
    
    while i <= up_to_index:
        msg = messages[i]
        
        # Always keep system/user messages
        if _is_system_or_user(msg):
            cleaned.append(msg)
            i += 1
            continue
        
        # Process AI messages
        if _is_ai_message(msg):
            tool_calls = _extract_tool_calls(msg)
            
            if tool_calls:
                filtered_calls, calc_ids = _filter_calculation_tool_calls(tool_calls)
                
                if not filtered_calls:
                    # All calculation tools - skip message and its ToolMessages
                    i += 1
                    while i <= up_to_index and _is_tool_message(messages[i]):
                        if _get_tool_call_id_from_message(messages[i]) in calc_ids:
                            i += 1
                        else:
                            break
                    continue
                elif len(filtered_calls) < len(tool_calls):
                    # Mixed - keep filtered message
                    cleaned.append(_create_filtered_ai_message(msg, filtered_calls))
                    kept_ids = {_get_tool_id(tc) for tc in filtered_calls}
                    
                    # Keep matching ToolMessages
                    i += 1
                    while i <= up_to_index and _is_tool_message(messages[i]):
                        tool_id = _get_tool_call_id_from_message(messages[i])
                        if tool_id in kept_ids:
                            cleaned.append(messages[i])
                        i += 1
                    continue
            
            # No tool calls or no calculation tools - keep as is
            cleaned.append(msg)
        
        # Process ToolMessages
        elif _is_tool_message(msg):
            tool_id = _get_tool_call_id_from_message(msg)
            if tool_id not in calculation_tool_call_ids:
                cleaned.append(msg)
        
        i += 1
    return cleaned


class CustomAgentState(AgentState, total=False):
    """Custom state schema that extends AgentState with all_tool_calls for evaluation."""
    all_tool_calls: List[Dict[str, Any]]  # Track all tool calls for evaluation


class AnswerStorageMiddleware(AgentMiddleware):
    """
    Middleware that cleans up calculation tool calls when store_answer is called.
    
    Uses RemoveMessage with REMOVE_ALL_MESSAGES for persistent removal from checkpointer.
    Tracks all tool calls (including filtered ones) for evaluation purposes.
    """
    
    def before_model(self, state: CustomAgentState, runtime: Any) -> Dict[str, Any] | None:
        """Filter calculation tool calls before store_answer calls."""
        messages = state.get("messages", [])
        
        # Track ALL tool calls from ALL messages for evaluation (before any filtering)
        # This ensures we capture everything including calculation tools that get filtered
        all_tool_calls = _track_tool_calls(messages, state.get("all_tool_calls", []))
        
        # Find latest store_answer call
        store_answer_indices = [i for i, msg in enumerate(messages) if _is_store_answer_call(msg)]
        if not store_answer_indices:
            return {"all_tool_calls": all_tool_calls}
        
        latest_store_idx = store_answer_indices[-1]
        
        # Collect calculation tool call IDs to remove (only up to store_answer)
        calculation_ids = set()
        for i in range(latest_store_idx + 1):
            tool_calls = _extract_tool_calls(messages[i])
            if tool_calls:
                _, calc_ids = _filter_calculation_tool_calls(tool_calls)
                calculation_ids.update(calc_ids)
        
        if not calculation_ids:
            return {"all_tool_calls": all_tool_calls}
        
        # Filter messages up to store_answer
        cleaned_messages = _filter_messages(messages, calculation_ids, latest_store_idx)
        
        # Use RemoveMessage for persistent removal, then rebuild with cleaned messages
        # IMPORTANT: all_tool_calls includes ALL tool calls (even filtered ones) for evaluation
        return {
            "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *cleaned_messages,
                *messages[latest_store_idx + 1:]  # Keep everything after store_answer
            ],
            "all_tool_calls": all_tool_calls  # This contains ALL tool calls for trajectory evaluation
        }
