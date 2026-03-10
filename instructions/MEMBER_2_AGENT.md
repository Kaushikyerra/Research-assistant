# 👤 Member 2: The Agent Architect (Core Logic)

**Role**: You are building the "Brain". You will use `LangGraph` to define how the agent thinks, plans, and executes the research process.

## 🎯 Objectives
1.  **State Management**: Define the `ReasoningState`.
2.  **Workflow**: Create the graph nodes (modules) and edges.
3.  **Prompting**: Write the system prompts for the Reasoning Engine.

## 🛠️ Your Workspace
*   **Directory**: `src/agent_core/`
*   **Key Files**:
    *   `src/agent_core/graph.py`: The LangGraph setup.
    *   `src/agent_core/prompts.py`: Storage for long system prompts.
    *   `src/agent_core/nodes.py`: The functions for each step (Reasoning, Hypothesis, etc.).

## 📝 Step-by-Step Instructions

### Step 1: Define the State
In `graph.py`, define a TypedDict `ResearchState`:
```python
class ResearchState(TypedDict):
    topic: str
    context: List[str]  # Retrieved papers
    reasoning_trace: str
    hypothesis: str
    feedback: str
    is_satisfactory: bool
```

### Step 2: Create the Nodes (in `nodes.py`)
You need to implement functions for:
1.  **`reasoning_node(state)`**: Calls LLM to break down the topic.
2.  **`retrieval_node(state)`**: Calls Member 1's retrieval tool.
3.  **`hypothesis_node(state)`**: Generates the core scientific idea based on context.

### Step 3: Build the Graph
In `graph.py`:
1.  Initialize `StateGraph(ResearchState)`.
2.  Add nodes: "reason", "retrieve", "hypothesize".
3.  Define edges:
    *   Start -> retrieve
    *   retrieve -> reason
    *   reason -> hypothesize
    *   hypothesize -> END (for now, later connects to Member 3's critique).

### Step 4: Prompt Engineering
This is critical. In `prompts.py`, write a prompt for the Hypothesis Node that encourages **novelty**.
*   *Example Instruction*: "You are a senior principal researcher. Given the background context, propose a novel hypothesis that contradicts common assumptions..."

---
**Definition of Done**:
You can run `graph.invoke({"topic": "AI in Medicine"})` and see the state move through retrieval -> reasoning -> hypothesis, resulting in a text output.
