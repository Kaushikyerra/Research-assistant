import json

class MockCritic:
    def __init__(self):
        self.call_count = 0

    def evaluate(self, hypothesis: str):
        """
        Mock evaluation of a hypothesis.
        First call: Fails and asks for equations/novelty.
        Subsequent calls: Passes.
        """
        self.call_count += 1
        print(f"[MockCritic] Evaluating hypothesis (Attempt {self.call_count})...")
        
        if self.call_count == 1:
            return {
                "score": 0.4,
                "feedback": "The hypothesis lacks mathematical formalism. Please formulate the correlation between viscosity and temperature using an Arrhenius-type equation and propose a specific additive mechanism."
            }
        else:
            return {
                "score": 0.9,
                "feedback": "Excellent. The hypothesis is now formally stated with governing equations and a clear mechanism. Approved."
            }
