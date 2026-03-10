"""
Integration Test for Agentic Research Assistant
Tests all three members' work together.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_member_1_rag():
    """Test Member 1's RAG Engine"""
    print("\n" + "="*60)
    print("Testing Member 1: RAG Engine")
    print("="*60)
    
    from src.rag_engine.retriever import fetch_arxiv_papers
    from src.rag_engine.db import ResearchDB
    
    # Test ArXiv retrieval
    print("\n[Test 1.1] Fetching papers from ArXiv...")
    papers = fetch_arxiv_papers("machine learning", max_results=3)
    assert len(papers) > 0, "Should fetch at least one paper"
    print(f"✓ Fetched {len(papers)} papers")
    
    # Test ChromaDB
    print("\n[Test 1.2] Testing ChromaDB ingestion...")
    db = ResearchDB()
    db.ingest_papers(papers)
    print("✓ Papers ingested successfully")
    
    # Test search
    print("\n[Test 1.3] Testing semantic search...")
    results = db.search("neural networks", n_results=2)
    assert len(results) > 0, "Should return search results"
    print(f"✓ Found {len(results)} relevant papers")
    
    print("\n✅ Member 1 tests passed!")
    return True

def test_member_2_agent():
    """Test Member 2's Agent Core"""
    print("\n" + "="*60)
    print("Testing Member 2: Agent Core")
    print("="*60)
    
    from src.agent_core.graph import build_graph, ResearchState
    from src.agent_core.prompts import RESEARCH_PLANNER_PROMPT, HYPOTHESIS_GENERATOR_PROMPT
    
    # Test graph building
    print("\n[Test 2.1] Building agent graph...")
    app = build_graph()
    assert app is not None, "Graph should be built successfully"
    print("✓ Graph compiled successfully")
    
    # Test prompts
    print("\n[Test 2.2] Testing prompt templates...")
    assert "{topic}" in RESEARCH_PLANNER_PROMPT, "Prompt should have topic placeholder"
    assert "{topic}" in HYPOTHESIS_GENERATOR_PROMPT, "Prompt should have topic placeholder"
    print("✓ Prompts are properly formatted")
    
    print("\n✅ Member 2 tests passed!")
    return True

def test_member_3_formalizer():
    """Test Member 3's Formalizer"""
    print("\n" + "="*60)
    print("Testing Member 3: Formalizer")
    print("="*60)
    
    from src.formalizer.math_check import MathTools, verify_equations
    from src.formalizer.critic import MockCritic, critique_node
    from src.formalizer.report_generator import generate_markdown
    
    # Test math tools
    print("\n[Test 3.1] Testing math validation...")
    tools = MathTools()
    result = tools.check_equations("E = mc^2")
    assert "valid" in result.lower() or "detected" in result.lower(), "Should validate equations"
    print("✓ Math validation working")
    
    # Test critic
    print("\n[Test 3.2] Testing hypothesis critic...")
    critic = MockCritic()
    evaluation = critic.evaluate("This is a test hypothesis with equations: x = y + z")
    assert "score" in evaluation, "Should return score"
    assert "feedback" in evaluation, "Should return feedback"
    print(f"✓ Critic returned score: {evaluation['score']}")
    
    # Test report generation
    print("\n[Test 3.3] Testing report generation...")
    mock_state = {
        "topic": "Test Topic",
        "hypothesis": "Test hypothesis",
        "context": ["Test context"],
        "reasoning_trace": "Test reasoning",
        "feedback": "Test feedback"
    }
    report = generate_markdown(mock_state)
    assert "# Research Report" in report, "Should generate proper markdown"
    assert "Test Topic" in report, "Should include topic"
    print("✓ Report generated successfully")
    
    print("\n✅ Member 3 tests passed!")
    return True

def test_full_integration():
    """Test full end-to-end workflow"""
    print("\n" + "="*60)
    print("Testing Full Integration")
    print("="*60)
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  Warning: No API keys found. Skipping full integration test.")
        print("   Set OPENAI_API_KEY or GOOGLE_API_KEY in .env to run full test.")
        return True
    
    from src.agent_core.graph import build_graph
    from src.formalizer.report_generator import generate_markdown
    
    print("\n[Test 4.1] Running mini workflow...")
    app = build_graph()
    
    # Use a simple topic for quick test
    initial_state = {
        "topic": "quantum computing",
        "context": [],
        "reasoning_trace": "",
        "hypothesis": "",
        "feedback": "",
        "is_satisfactory": False,
        "revision_count": 0
    }
    
    print("   Note: This will make real API calls and may take time...")
    print("   Streaming graph execution...")
    
    try:
        final_state = None
        for output in app.stream(initial_state):
            for node_name, state_update in output.items():
                print(f"   ✓ Node completed: {node_name}")
                final_state = {**initial_state, **state_update} if final_state is None else {**final_state, **state_update}
        
        assert final_state is not None, "Should have final state"
        assert final_state.get("hypothesis"), "Should generate hypothesis"
        print("✓ Workflow completed successfully")
        
        # Generate report
        print("\n[Test 4.2] Generating final report...")
        report = generate_markdown(final_state)
        assert len(report) > 100, "Report should have substantial content"
        print("✓ Report generated")
        
        print("\n✅ Full integration test passed!")
        return True
        
    except Exception as e:
        print(f"\n⚠️  Integration test encountered error: {e}")
        print("   This might be due to API rate limits or network issues.")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 AGENTIC RESEARCH ASSISTANT - INTEGRATION TEST")
    print("="*60)
    
    results = []
    
    # Test each member's work
    try:
        results.append(("Member 1 (RAG)", test_member_1_rag()))
    except Exception as e:
        print(f"\n❌ Member 1 tests failed: {e}")
        results.append(("Member 1 (RAG)", False))
    
    try:
        results.append(("Member 2 (Agent)", test_member_2_agent()))
    except Exception as e:
        print(f"\n❌ Member 2 tests failed: {e}")
        results.append(("Member 2 (Agent)", False))
    
    try:
        results.append(("Member 3 (Formalizer)", test_member_3_formalizer()))
    except Exception as e:
        print(f"\n❌ Member 3 tests failed: {e}")
        results.append(("Member 3 (Formalizer)", False))
    
    # Full integration test
    try:
        results.append(("Full Integration", test_full_integration()))
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        results.append(("Full Integration", False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 All tests passed! Ready to push to Git.")
    else:
        print("\n⚠️  Some tests failed. Please review errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
