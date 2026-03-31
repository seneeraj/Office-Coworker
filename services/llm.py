from groq import Groq
import streamlit as st

def generate_response(prompt):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    models = [
        "llama-3.3-8b-instant",   # primary
        "mixtral-8x7b-32768",    # fallback
    ]

    for model in models:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=model
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            continue

    return "(Error) All models failed. Please try again."
