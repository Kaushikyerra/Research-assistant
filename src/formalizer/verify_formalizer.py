"""
Verification script for Member 3's Formalizer module.
Tests math validation, critique, and report generation.
"""

from math_check import MathTools, verify_equations
from critic import MockCritic, critique_node
from report_generator import generate_markdown, save_report

def test_math_tools():
    print("=" * 60)
    print("Testing Math Tools")
    print("=" * 60)
    
    tools = MathTools()
    
    # Test with equations
    hypothesis_with_math = """
    The ionic conductivity follows: sigma = A * exp(-Ea / RT)
    where Ea is activation energy and R is gas constant.
    """
    result1 = tools.check_equations(hypothesis_with_math)
    print(f"Test 1 (with equations): {result1}\n")
    
    # Test without equations
    hypothesis_no_math = "This is a simple hypothesis without any math."
    result2 = tools.check_equations(hypothesis_no_math)
    print(f"Test 2 (no equations): {result2}\n")

def test_critic():
    print("=" * 60)
    print("Testing Critic")
    print("=" * 60)
    
    critic = MockCritic()
    
    # Test comprehensive hypothesis
    good_hypothesis = """
    Problem Statement: Battery degradation in cold temperatures.
    Hypothesis: Novel electrolyte additives can improve performance.
    Mathematical Formulation: sigma = A * exp(-Ea / RT)
    Proposed Mechanism: The additive reduces activation energy.
    Way Forward: Test at -20°C with various concentrations.
    """ * 3  # Make it long enough
    
    result1 = critic.evaluate(good_hypothesis)
    print(f"Test 1 (comprehensive):")
    print(f"  Score: {result1['score']}")
    print(f"  Feedback: {result1['feedback']}\n")
    
    # Test short hypothesis
    short_hypothesis = "Batteries work better with new chemicals."
    result2 = critic.evaluate(short_hypothesis)
    print(f"Test 2 (insufficient):")
    print(f"  Score: {result2['score']}")
    print(f"  Feedback: {result2['feedback']}\n")

def test_report_generation():
    print("=" * 60)
    print("Testing Report Generation")
    print("=" * 60)
    
    # Mock state
    state = {
        "topic": "Battery Optimization in Cold Temperatures",
        "hypothesis": """
        **Problem Statement**: Standard Li-ion batteries lose 60% capacity at -20°C.
        
        **Hypothesis**: Adding 2% fluoroethylene carbonate (FEC) to the electrolyte 
        will reduce charge transfer resistance by 40% at low temperatures.
        
        **Mathematical Formulation**: 
        Ionic conductivity: sigma = A * exp(-Ea / RT)
        Charge transfer resistance: Rct = RT / (nFi0)
        
        **Proposed Mechanism**: FEC forms a stable SEI layer that maintains 
        ionic conductivity even at low temperatures by reducing desolvation energy.
        
        **Way Forward**: Test with coin cells at -20°C, measure impedance spectroscopy.
        """,
        "context": [
            "[1] Low-Temperature Electrolytes (2023) - Standard electrolytes fail below -10°C",
            "[2] FEC Additives Study (2024) - FEC improves SEI stability"
        ],
        "reasoning_trace": "Analyzed literature gap in cold-weather battery performance.",
        "feedback": "Approved - Hypothesis is well-structured and testable."
    }
    
    report = generate_markdown(state)
    print("Generated Report Preview:")
    print(report[:500] + "...\n")
    
    # Save to file
    save_report(report, "test_output.md")
    print("Full report saved to test_output.md")

if __name__ == "__main__":
    print("\n🧪 Member 3 Formalizer Module Verification\n")
    
    test_math_tools()
    test_critic()
    test_report_generation()
    
    print("\n" + "=" * 60)
    print("✅ All Member 3 tests completed!")
    print("=" * 60)
