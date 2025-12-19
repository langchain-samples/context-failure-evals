# Context Management with LangSmith Evaluations

> ⚠️ **Work in Progress**: This demo is being refined to show clear metrics demonstrating the impact of context management strategies.


## Context Management Patterns

### 1. Context Confusion

Demonstrating how **context confusion** - superfluous context from excessive tools, verbose instructions, and irrelevant information - degrades LLM agent performance, and how to fix it with LangSmith evaluations.

## The Problem

Adding more tools to an agent seems helpful, but the Berkeley Function-Calling Leaderboard shows **every model performs worse with more tools**. This is context confusion: too much in the context leads to poor tool selection, unnecessary calls, and incorrect responses.

Three problems measured with **trajectory-based evaluation**:

1. **Tool Overload** - ~75 tools → confusion and poor selection
2. **Irrelevant Noise** - Unrelated tools distract even at moderate counts  
3. **Instruction Bloat** - Verbose multi-domain instructions reduce focus

## Evaluators

- **Trajectory Match**: Do tool calls match expected tools?
- **Correctness** (openevals): Is the response accurate?
- **LLM Trajectory Judge**: Are tool calls appropriate?
- **Tool Efficiency**: Ratio of expected/actual tool calls


### 2. [Pattern Name TBD]

- 

### 3. [Pattern Name TBD]

- 

### 4. [Pattern Name TBD]

-


```bash
# Install dependencies
uv sync

# Set environment variables
cp .env.example .env  # Add your ANTHROPIC_API_KEY and LANGSMITH_API_KEY

# Run the notebook
jupyter notebook context_confusion_demo.ipynb
```


## Structure

```
context_confusion/
├── tools.py              # 75 tools including confusing near-duplicates
├── instructions.py       # Simple base instructions
├── additional_context.py # Irrelevant domain instructions for Problem 3
└── resources/            # Mock data (orders, customers, carriers, warehouses)

context_confusion_demo.ipynb  # context confusion demonstration notebook
```

