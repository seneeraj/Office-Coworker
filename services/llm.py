from groq import Groq
import streamlit as st

def generate_response(prompt):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "❌ GROQ_API_KEY not found in secrets"

        client = Groq(api_key=api_key)

        model = "mixtral-8x7b-32768"   # MOST STABLE MODEL

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
