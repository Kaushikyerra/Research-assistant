# 👤 Member 3: The Formalizer & Critic (Quality & Output)

**Role**: You are the "Voice of Rigor". You ensure the agent's output is mathematically sound and formatted as a proper scientific paper.

## 🎯 Objectives
1.  **Formalization**: Convert natural language logic into mathematical notation (LaTeX/Python).
2.  **Critique**: Implement a feedback loop to critique and improve the hypothesis.
3.  **Reporting**: Assemble the final PDF/Markdown report.

## 🛠️ Your Workspace
*   **Directory**: `src/formalizer/`
*   **Key Files**:
    *   `src/formalizer/math_check.py`: Tools for math verification.
    *   `src/formalizer/critic.py`: The "Reviewer" agent logic.
    *   `src/formalizer/report_generator.py`: Compiles the final output.

## 📝 Step-by-Step Instructions

### Step 1: The Math Checker
In `math_check.py`, create a simple tool using `llm` that specifically looks for equations.
*   **Function**: `verify_equations(text)`
*   **Action**: Ask an LLM "Are the variables in this equation defined? Is the dimensional analysis correct?"
*   (Bonus: Use Python `sympy` if applicable to actually solve/check).

### Step 2: The Critic Node
Create a `critique_node(state)` function (to be added to Member 2's graph later).
*   **Role**: Act as "Reviewer #2".
*   **Prompt**: "Find 3 flaws in this hypothesis. Be harsh. Focus on feasibility and novelty."
*   **Output**: A list of critiques.

### Step 3: Report Generation
In `report_generator.py`, create a function `generate_markdown(state)`.
*   It should take the final state (Hypothesis, Reasoning, Context) and format it into a classic paper structure:
    *   `# Title`
    *   `## Abstract`
    *   `## Introduction` (Context)
    *   `## Proposed Method` (Formalization)
    *   `## Discussion` (Critique/Limitations)

### Step 4: The Main Entry Point
Create `main.py` in the project root.
*   This script will import the Graph from Member 2.
*   It will ask for user input: `input("Enter research topic: ")`
*   It checks for environment variables (.env).
*   It runs the graph and saves the output using your Report Generator.

---
**Definition of Done**:
You can take a dummy string "Hypothesis: X is Y" and generate a beautifully formatted `output.md` file with headers and a "Critique" section.
