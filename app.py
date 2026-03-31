import streamlit as st
import sys
import os

# Fix path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agent import Agent
from core.memory import Memory
from services.formatter import format_task_output

# -----------------------------
# SESSION SAFE INIT
# -----------------------------
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "memory" not in st.session_state:
    st.session_state.memory = Memory()

agent = st.session_state.agent
memory = st.session_state.memory

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Clarity AI", layout="wide")
st.title("🚀 Clarity AI Workspace")

# -----------------------------
# FILE UPLOAD (TOP)
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload a document")

file_text = ""

if uploaded_file:
    try:
        file_text = uploaded_file.read().decode("utf-8")
        st.success("File loaded successfully")
    except:
        file_text = ""
        st.error("Unsupported file format")

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns([1, 2])

# -----------------------------
# LEFT PANEL (Controls)
# -----------------------------
with col1:
    st.subheader("🧠 Controls")

    mode = st.radio("Mode", ["Task", "Chat"])
    use_case = st.selectbox("Use Case", ["General", "Business", "Finance"])

# -----------------------------
# RIGHT PANEL (Workspace)
# -----------------------------
with col2:
    st.subheader("💬 Workspace")

    user_input = st.text_input("Enter your task")

    if st.button("Run"):
        if not user_input:
            st.warning("Please enter a task")
        else:
            result = agent.process(user_input, file_text)

            # TASK MODE OUTPUT
            if result["mode"] == "task":
                st.success(f"Executed: {result['skill']}")

                output = format_task_output(result["skill"], result["results"])
                st.json(output)

                memory.save(user_input, str(output))

            # CHAT MODE OUTPUT
            else:
                st.write(result["response"])

                memory.save(user_input, result["response"])

# -----------------------------
# DEBUG (OPTIONAL)
# -----------------------------
# st.write("Memory object:", memory)
