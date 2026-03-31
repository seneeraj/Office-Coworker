import requests

def generate_response(prompt):
    try:
        # Try local Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=2
        )
        return response.json()["response"]

    except:
        # Fallback (cloud-safe)
        return f"(Demo Mode) AI response for: {prompt}"