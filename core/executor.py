from services.llm import generate_response

class Executor:
    def run_steps(self, steps, user_input=None):
        results = []

        for step in steps:
            result = generate_response(f"Execute this step: {step}")
            results.append(result)

        return results