from core.rag import simple_rag

def process(self, user_input, file_text=None):
    skill = self.skill_engine.match_skill(user_input)

    if skill:
        results = self.executor.run_steps(skill["steps"])
        return {"mode": "task", "skill": skill["name"], "results": results}

    # RAG Mode
    if file_text:
        prompt = simple_rag(user_input, file_text)
    else:
        prompt = user_input

    response = generate_response(prompt)

    return {"mode": "chat", "response": response}

class Agent:
    def __init__(self):
        pass

    def process(self, user_input, file_text=None):
        return {
            "mode": "chat",
            "response": f"Agent working for: {user_input}"
        }
