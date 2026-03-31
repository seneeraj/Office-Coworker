import streamlit as st
from core.agent import Agent
from core.memory import Memory
from services.formatter import format_task_output

agent = Agent()
memory = Memory()

st.set_page_config(page_title="Clarity AI", layout="wide")

st.title("🚀 Clarity AI Workspace")

mode = st.radio("Select Mode", ["Task Mode", "Chat Mode"])

user_input = st.text_input("Enter your task")

if st.button("Run"):
    result = agent.process(user_input)

    if result["mode"] == "task":
        output = format_task_output(result["skill"], result["results"])
        st.json(output)
        memory.save(user_input, str(output))

    else:
        st.write(result["response"])
        memory.save(user_input, result["response"])
        
        
        
uploaded_file = st.file_uploader("Upload a document")

file_text = ""

if uploaded_file:
    try:
        file_text = uploaded_file.read().decode("utf-8")
    except:
        file_text = "Unsupported file format"


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🧠 Controls")
    mode = st.radio("Mode", ["Task", "Chat"])
    use_case = st.selectbox("Use Case", ["General", "Business", "Finance"])

with col2:
    st.subheader("💬 Workspace")

    user_input = st.text_input("Enter your task")

    if st.button("Run"):
        result = agent.process(user_input, file_text)

        if result["mode"] == "task":
            st.success(f"Executed: {result['skill']}")
            for r in result["results"]:
                st.write("✔", r)
        else:
            st.write(result["response"])    