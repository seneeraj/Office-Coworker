import streamlit as st
import sys
import os
import uuid

# Fix import paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agent import Agent
from core.memory import Memory
from services.formatter import format_task_output

# -----------------------------
# SESSION INIT (AGENT + MEMORY)
# -----------------------------
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "memory" not in st.session_state:
    st.session_state.memory = Memory()

agent = st.session_state.agent
memory = st.session_state.memory

# -----------------------------
# MULTI-CHAT INIT
# -----------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Clarity AI", layout="wide")
st.title("🚀 Clarity AI Workspace")

# -----------------------------
# FILE UPLOAD (RAG)
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
# SIDEBAR (CHAT MANAGEMENT)
# -----------------------------
with st.sidebar:
    st.title("🧠 Clarity AI")

    # New chat
    if st.button("➕ New Chat"):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = []

    st.markdown("---")
    st.subheader("💬 Chat History")

    for chat_id in list(st.session_state.chats.keys()):
        messages = st.session_state.chats[chat_id]

        # Chat label (first message preview)
        if messages:
            label = messages[0]["content"][:25]
        else:
            label = "New Chat"

        col1, col2 = st.columns([3, 1])

        with col1:
            if st.button(label, key=f"chat_{chat_id}"):
                st.session_state.current_chat = chat_id

        with col2:
            if st.button("❌", key=f"del_{chat_id}"):
                del st.session_state.chats[chat_id]

                if st.session_state.current_chat == chat_id:
                    new_id = str(uuid.uuid4())
                    st.session_state.current_chat = new_id
                    st.session_state.chats[new_id] = []

# -----------------------------
# CHAT UI
# -----------------------------
st.subheader("💬 Chat")

messages = st.session_state.chats[st.session_state.current_chat]

# Display chat history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Process with agent
    result = agent.process(user_input, file_text, memory)

    # Handle response
    if result["mode"] == "task":
        output = format_task_output(result["skill"], result["results"])
        response = str(output)
    else:
        response = result["response"]

    # Save AI message
    messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

    # Save to memory DB
    memory.save(user_input, response)
