"""
Helper functions for running agents and extracting trajectories.
"""

from typing import Dict, Any, List
from langchain_core.messages import ToolMessage
import json


def extract_tool_calls_from_message(msg) -> List[Dict[str, Any]]:
    """
    Extract tool calls from a message object.
    
    Args:
        msg: Message object (can be dict or LangChain message)
    
    Returns:
        List of tool call dictionaries
    """
    tool_calls = []
    
    if isinstance(msg, dict):
        # Check for tool calls in dict format
        if "tool_calls" in msg:
            for tc in msg["tool_calls"]:
                tool_calls.append({
                    "tool": tc.get("name", ""),
                    "args": tc.get("args", {}),
                    "id": tc.get("id", "")
                })
        elif "tool" in msg:
            # Single tool call
            tool_calls.append({
                "tool": msg.get("tool", ""),
                "args": msg.get("args", {}),
                "id": msg.get("id", "")
            })
    else:
        # LangChain message object
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls.append({
                    "tool": tc.get("name", "") if isinstance(tc, dict) else getattr(tc, "name", ""),
                    "args": tc.get("args", {}) if isinstance(tc, dict) else (getattr(tc, "args", {}) if hasattr(tc, "args") else {}),
                    "id": tc.get("id", "") if isinstance(tc, dict) else getattr(tc, "id", "")
                })
    
    return tool_calls


def run_agent_with_trajectory(agent, query: str) -> Dict[str, Any]:
    """
    Run an agent and extract the full trajectory of tool calls and responses.
    
    Args:
        agent: The agent to run
        query: User query
    
    Returns:
        Dictionary with final_response and trajectory
    """
    trajectory = []
    final_response = ""
    all_messages = []
    
    try:
        # Use synchronous invoke (works better in Jupyter notebooks)
        result = agent.invoke({"messages": [("user", query)]})
        
        # Extract messages from result
        if isinstance(result, dict):
            if "messages" in result:
                all_messages = result["messages"]
            elif "output" in result:
                # Some agents return output instead of messages
                all_messages = result.get("messages", [])
            else:
                all_messages = []
        elif hasattr(result, "messages"):
            all_messages = result.messages
        else:
            all_messages = []
        
        # Extract tool calls from messages
        for msg in all_messages:
            tool_calls = extract_tool_calls_from_message(msg)
            for tc in tool_calls:
                trajectory.append({
                    "tool": tc["tool"],
                    "args": tc["args"],
                    "step": len(trajectory)
                })
        
        # Extract final response
        for msg in reversed(all_messages):
            if isinstance(msg, dict):
                if msg.get("content") and not isinstance(msg.get("content"), list):
                    final_response = msg["content"]
                    break
            elif hasattr(msg, "content") and msg.content:
                final_response = msg.content
                break
        
        # Also try to get tool responses for trajectory
        for i, msg in enumerate(all_messages):
            if isinstance(msg, ToolMessage) or (isinstance(msg, dict) and msg.get("type") == "tool"):
                content = msg.content if hasattr(msg, "content") else msg.get("content", "")
                if i > 0 and i <= len(trajectory):
                    trajectory[i-1]["response"] = content
        
    except Exception as e:
        return {
            "final_response": f"Error: {str(e)}",
            "trajectory": trajectory,
            "error": str(e)
        }
    
    return {
        "final_response": final_response,
        "trajectory": trajectory,
        "error": None
    }
