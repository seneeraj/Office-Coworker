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
# -----------------------------
# CHAT HISTORY INIT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🧠 Clarity AI")

    if st.button("➕ New Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.write("Modes")
    mode = st.radio("Select Mode", ["Task", "Chat"])

# -----------------------------
# MAIN CHAT UI
# -----------------------------
st.title("💬 Clarity AI Workspace")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    result = agent.process(user_input, file_text, memory)

    if result["mode"] == "task":
        output = format_task_output(result["skill"], result["results"])
        response = str(output)
    else:
        response = result["response"]

    # Show AI message
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    memory.save(user_input, response)

# -----------------------------
# DEBUG (OPTIONAL)
# -----------------------------
# st.write("Memory object:", memory)
