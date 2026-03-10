import os
import sys
from dotenv import load_dotenv

# Add src to path just in case
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables (API Keys)
load_dotenv()

from src.agent_core.graph import build_graph
from src.rag_engine.db import ResearchDB
from src.formalizer.report_generator import generate_markdown, save_report

def main():
    print("🧪 Agentic Research Assistant - v0.1")
    print("-------------------------------------")
    
    # 1. Setup Phase
    print("[System] Initializing ChromaDB...")
    db = ResearchDB()  # Initialize database
    
    print("[System] Building Agent Graph...")
    app = build_graph()
    
    # 2. User Input
    topic = input("\nEnter your research topic/question: ")
    if not topic:
        print("Exiting...")
        return

    print(f"\n[Agent] Starting research on: '{topic}'")
    print("[Agent] This may take a few minutes...\n")
    
    # 3. Execution
    initial_state = {
        "topic": topic,
        "context": [],
        "reasoning_trace": "",
        "hypothesis": "",
        "feedback": "",
        "is_satisfactory": False,
        "revision_count": 0
    }
    
    try:
        # Run the graph and collect final state
        final_state = None
        for output in app.stream(initial_state):
            for node_name, state_update in output.items():
                print(f"✓ Completed: {node_name}")
                final_state = {**initial_state, **state_update} if final_state is None else {**final_state, **state_update}
        
        # 4. Generate Report
        print("\n[System] Generating research report...")
        report = generate_markdown(final_state)
        
        # Save to file
        filename = f"research_report_{topic[:30].replace(' ', '_')}.md"
        save_report(report, filename)
        
        print(f"\n✅ [Success] Report generated at: {filename}")
        print("\n" + "="*60)
        print("PREVIEW:")
        print("="*60)
        print(report[:500] + "...\n")
        
    except Exception as e:
        print(f"\n❌ [Error] An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
