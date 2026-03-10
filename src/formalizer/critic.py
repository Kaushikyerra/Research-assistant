class MockCritic:
    def __init__(self):
        pass
    
    def evaluate(self, hypothesis: str):
        """
        Evaluates the hypothesis and provides a score and feedback.
        Returns a dict with 'score' and 'feedback'.
        """
        print(f"[Critic] Evaluating hypothesis...")
        
        # Basic quality checks
        word_count = len(hypothesis.split())
        has_structure = any(keyword in hypothesis.lower() for keyword in 
                           ['hypothesis', 'problem', 'mechanism', 'equation', 'proposed'])
        
        # Scoring logic
        if word_count > 500 and has_structure:
            return {
                "score": 8,
                "feedback": "Approved - Hypothesis is comprehensive and well-structured."
            }
        elif word_count > 300:
            return {
                "score": 6,
                "feedback": "Needs more detail in the mathematical formulation and proposed mechanism."
            }
        else:
            return {
                "score": 4,
                "feedback": "Insufficient detail. Please expand on the hypothesis, add mathematical formulations, and describe the mechanism more clearly."
            }

def critique_node(state):
    """
    Acts as Reviewer #2 to critique the hypothesis.
    Compatible with LangGraph state management.
    """
    print(f"--- [Node: Critique] Reviewing Hypothesis ---")
    hypothesis = state.get("hypothesis", "")
    
    critic = MockCritic()
    evaluation = critic.evaluate(hypothesis)
    
    score = evaluation['score']
    feedback = evaluation['feedback']
    
    print(f"Critic Score: {score}")
    print(f"Critic Feedback: {feedback}")
    
    # Increment revision count if it exists in state
    current_revisions = state.get('revision_count', 0)
    
    return {
        "feedback": feedback,
        "critique_feedback": feedback,
        "revision_count": current_revisions + 1
    }
