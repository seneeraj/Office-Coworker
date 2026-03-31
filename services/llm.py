from groq import Groq
import streamlit as st

def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_response(prompt):
    try:
        client = get_client()

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-70b-versatile"
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
