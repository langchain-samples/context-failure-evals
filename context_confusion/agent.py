"""
Example Shipping Support Agent Implementation

This demonstrates how to use the context_confusion module to create
an agent that handles shipping support queries.
"""

from context_confusion.tools import (
    all_tools,
    shipping_core_tools,
    carrier_tools,
    returns_tools,
    warehouse_tools,
    order_modification_tools,
    customer_service_tools,
    billing_tools
)

from context_confusion.instructions import (
    SHIPPING_SUPPORT_INSTRUCTIONS,
    CARRIER_MANAGEMENT_INSTRUCTIONS,
    RETURNS_INSTRUCTIONS,
    WAREHOUSE_OPERATIONS_INSTRUCTIONS,
    ORDER_MODIFICATION_INSTRUCTIONS,
    CUSTOMER_SERVICE_INSTRUCTIONS,
    BILLING_INSTRUCTIONS
)

from context_confusion.additional_context import IRRELEVANT_INSTRUCTIONS


# =====================================================
# Configuration Options
# =====================================================

# Option 1: Core shipping support only (focused agent)
CORE_TOOLS = shipping_core_tools + carrier_tools
CORE_INSTRUCTIONS = f"""
{SHIPPING_SUPPORT_INSTRUCTIONS}

{CARRIER_MANAGEMENT_INSTRUCTIONS}
"""

# Option 2: Full shipping operations (expanded scope)
FULL_SHIPPING_TOOLS = (
    shipping_core_tools +
    carrier_tools +
    returns_tools +
    warehouse_tools +
    order_modification_tools +
    customer_service_tools +
    billing_tools
)

FULL_SHIPPING_INSTRUCTIONS = f"""
{SHIPPING_SUPPORT_INSTRUCTIONS}

{CARRIER_MANAGEMENT_INSTRUCTIONS}

{RETURNS_INSTRUCTIONS}

{WAREHOUSE_OPERATIONS_INSTRUCTIONS}

{ORDER_MODIFICATION_INSTRUCTIONS}

{CUSTOMER_SERVICE_INSTRUCTIONS}

{BILLING_INSTRUCTIONS}
"""

# Option 3: All tools (context confusion challenge)
ALL_TOOLS = all_tools

ALL_INSTRUCTIONS = f"""
{FULL_SHIPPING_INSTRUCTIONS}

{IRRELEVANT_INSTRUCTIONS}
"""


# =====================================================
# Agent System Message
# =====================================================

SYSTEM_MESSAGE = """You are a helpful shipping support agent for an e-commerce company.

Your primary role is to help customers with:
- Order tracking and status
- Shipment information and delivery estimates
- Addressing shipping delays and issues
- Processing returns and refunds
- Updating delivery preferences

Always be polite, professional, and customer-focused. Verify customer identity before sharing sensitive information.

{instructions}
"""


# =====================================================
# Example Agent Setup Functions
# =====================================================

def create_focused_agent(llm):
    """
    Create an agent with only core shipping support tools.
    
    This configuration minimizes context confusion by providing
    only the essential tools needed for shipping support.
    """
    system_message = SYSTEM_MESSAGE.format(instructions=CORE_INSTRUCTIONS)
    
    # Your agent creation logic here
    # Example:
    # from langgraph.prebuilt import create_react_agent
    # return create_react_agent(llm, CORE_TOOLS, messages_modifier=system_message)
    
    return {
        "tools": CORE_TOOLS,
        "system_message": system_message,
        "description": "Focused shipping support agent"
    }


def create_full_operations_agent(llm):
    """
    Create an agent with full shipping operations capabilities.
    
    This configuration includes returns, warehouse, billing, and
    customer service tools - more realistic for a production system.
    """
    system_message = SYSTEM_MESSAGE.format(instructions=FULL_SHIPPING_INSTRUCTIONS)
    
    return {
        "tools": FULL_SHIPPING_TOOLS,
        "system_message": system_message,
        "description": "Full shipping operations agent"
    }


def create_context_confusion_agent(llm):
    """
    Create an agent with ALL tools including irrelevant domains.
    
    This configuration is designed to test context confusion by
    providing many tools and instructions across diverse domains,
    many of which are not relevant to shipping support.
    """
    system_message = SYSTEM_MESSAGE.format(instructions=ALL_INSTRUCTIONS)
    
    return {
        "tools": ALL_TOOLS,
        "system_message": system_message,
        "description": "Context confusion test agent"
    }


# =====================================================
# Example Test Queries
# =====================================================

EXAMPLE_QUERIES = [
    # Basic shipping queries
    "I'm user@example.com and I want to track my order #84721",
    "What's the status of order 99002?",
    "When will my package arrive? Order #10015",
    
    # Delayed shipment with carrier incident
    "I'm buyer@uk-shop.co.uk and my order #23456 is delayed. What's happening?",
    
    # EU customer privacy scenario
    "I'm manager@euro-corp.eu, can you tell me the status of order #45678?",
    
    # Platinum customer priority
    "Hi, I'm ops@widget.io and I need urgent help with order #10015",
    
    # Return request
    "I need to return order #11111, it was the wrong item",
    
    # Multi-step query
    "Can you check if SKU-123 is in stock and when it can ship to San Francisco?",
    
    # Context confusion test
    "What's the fraud score for order #84721 and can you apply a 20% discount?",
]


# =====================================================
# Usage Example
# =====================================================

if __name__ == "__main__":
    print("Shipping Support Agent Configuration")
    print("=" * 50)
    print()
    
    # Initialize LLM (placeholder)
    llm = None  # Replace with actual LLM initialization
    
    # Show different configurations
    configs = [
        ("Focused Agent", create_focused_agent(llm)),
        ("Full Operations Agent", create_full_operations_agent(llm)),
        ("Context Confusion Agent", create_context_confusion_agent(llm))
    ]
    
    for name, config in configs:
        print(f"{name}:")
        print(f"  Tools: {len(config['tools'])} tools")
        print(f"  Description: {config['description']}")
        print(f"  Instructions length: {len(config['system_message'])} chars")
        print()
    
    print("Example Queries:")
    print("-" * 50)
    for i, query in enumerate(EXAMPLE_QUERIES, 1):
        print(f"{i}. {query}")
    print()
    
    print("To use this agent:")
    print("1. Initialize your LLM")
    print("2. Choose a configuration (focused, full, or context_confusion)")
    print("3. Create the agent with create_*_agent(llm)")
    print("4. Test with example queries or your own")

