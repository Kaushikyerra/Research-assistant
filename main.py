from agent_graph import app
from langchain_core.messages import HumanMessage

def main():
    print("=" * 60)
    print("SCIENTIFIC RESEARCH AGENT")
    print("=" * 60)
    print("\nThis agent will:")
    print("1. Search arXiv for relevant research papers")
    print("2. Analyze all 10 papers individually")
    print("3. Generate a novel scientific hypothesis")
    print("4. Refine it through critic feedback\n")

    user_input = input("Enter your research question: ").strip()
    if not user_input:
        print("No input provided. Using default question...")
        user_input = "seismic data denoising"

    print(f"\nResearch Question: {user_input}")
    print("\nStarting Scientific Agent...")

    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "research_data": "",
        "hypothesis": "",
        "critique_feedback": "",
        "revision_count": 0
    }

    # Accumulate full state across all node outputs
    full_state = dict(initial_state)

    for output in app.stream(initial_state):
        for node_name, value in output.items():
            print(f"Finished Node: {node_name}")
            # Merge every key from this node's output into full_state
            for k, v in value.items():
                if v:
                    full_state[k] = v
            print("-" * 20)

    print("\nAgent execution finished.")

    # ── SECTION 1: PAPER ANALYSIS ────────────────────────────────
    print("\n")
    print("=" * 80)
    print("  SECTION 1: PAPER ANALYSIS REPORT (All 10 Retrieved Papers)")
    print("=" * 80)
    print(full_state.get("research_data", "No research data available."))

    # ── SECTION 2: SCIENTIFIC PROPOSAL ───────────────────────────
    print("\n")
    print("=" * 80)
    print("  SECTION 2: SCIENTIFIC PROPOSAL")
    print("=" * 80)
    hypothesis = full_state.get("hypothesis", "No hypothesis generated.")

    # Ensure all 5 sections are present, warn if any are missing
    sections = [
        "Problem Statement",
        "Hypothesis",
        "Mathematical Formulation",
        "Proposed Mechanism",
        "Way Forward"
    ]
    print(hypothesis)

    print("\n")
    print("=" * 80)
    print("  SECTION 3: REVIEW SUMMARY")
    print("=" * 80)
    print(f"  Topic          : {user_input}")
    print(f"  Papers Fetched : 10 (from arXiv)")
    print(f"  Revisions Done : {full_state.get('revision_count', 0)}")
    print(f"  Final Feedback : {full_state.get('critique_feedback', 'N/A')}")
    missing = [s for s in sections if s.lower() not in hypothesis.lower()]
    if missing:
        print(f"  Missing Sections: {', '.join(missing)}")
    else:
        print("  All 5 proposal sections present: Problem Statement, Hypothesis,")
        print("  Mathematical Formulations, Proposed Mechanism, Way Forward")
    print("=" * 80)

if __name__ == "__main__":
    main()
