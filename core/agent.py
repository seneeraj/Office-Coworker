from core.skill_engine import SkillEngine
from core.executor import Executor
from services.llm import generate_response

class Agent:
    def __init__(self):
        self.skill_engine = SkillEngine()
        self.executor = Executor()

    def process(self, user_input, file_text=None, memory=None):
        # 1. Try skill
        skill = self.skill_engine.match_skill(user_input)

        if skill:
            results = self.executor.run_steps(skill["steps"], user_input)
            return {
                "mode": "task",
                "skill": skill["name"],
                "results": results
            }

        # 2. Build context from memory
        context = ""
        if memory:
            history = memory.fetch_recent()
            context = "\n".join(
                [f"User: {h[0]} AI: {h[1]}" for h in history]
            )

        # 3. Add file context (RAG)
        if file_text:
            context += f"\n\nDocument:\n{file_text[:2000]}"

        # 4. Final prompt
        final_prompt = f"{context}\nUser: {user_input}"

        response = generate_response(final_prompt)

        return {
            "mode": "chat",
            "response": response
        }
