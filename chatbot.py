import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Environment Variables Load Karna
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# API Key Check Karna
if not api_key:
    st.error("❌ Error: GEMINI_API_KEY not found in .env file!")
    st.stop()

# Gemini API Configure Karna
genai.configure(api_key=api_key)

# Streamlit Page Config (Sabse Pehle)
st.set_page_config(page_title="Faizee's AI Chatbot", layout="wide")

# Custom CSS Styling (New UI for Faizee)
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to right, #FFDEE9, #B5FFFC);
            padding: 20px;
        }
        .chat-container {
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.1);
        }
        .user-message {
            background: #FFDEE9;
            color: black;
            padding: 12px;
            border-radius: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #FF80AB;
        }
        .bot-message {
            background: #E1F5FE;
            color: black;
            padding: 12px;
            border-radius: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #4FC3F7;
        }
        .suggestion-btn button {
            background: #4FC3F7;
            color: white;
            border-radius: 8px;
            padding: 10px;
            margin-right: 10px;
            font-size: 14px;
            border: none;
            cursor: pointer;
        }
        .suggestion-btn button:hover {
            background: #039BE5;
        }
    </style>
""", unsafe_allow_html=True)

# UI Setup
st.title("🤖 Faizee’s AI | Your Personal Chat Companion")

# Session State to Store Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Gemini Response Function
def get_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        time.sleep(1)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Function to Handle Input
def handle_input():
    user_input = st.session_state.user_message
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.empty():
            for i in range(3):
                st.write("🤖 Thinking" + "." * (i+1))
                time.sleep(0.5)
        response = get_response(user_input)
        st.session_state.messages.append({"role": "bot", "content": response})
        st.session_state.user_message = ""

# Suggested Questions
st.markdown("#### 💡 Quick Suggestions:")
suggestions = [
    "What is AI?",
    "Tell me a fun fact!",
    "How can I improve my coding skills?",
    "Explain the concept of cloud computing.",
    "Give me a motivational quote!"
]
col1, col2, col3 = st.columns(3)

for i, suggestion in enumerate(suggestions):
    with [col1, col2, col3][i % 3]:
        if st.button(suggestion, key=f"suggestion_{i}", help="Click to ask this question"):
            st.session_state.user_message = suggestion
            handle_input()

# User Input Field
col1, col2 = st.columns([4, 1])
with col1:
    st.text_input("💬 Type your message:", key="user_message", on_change=handle_input)


# Clear Chat Button
if st.button("🔄 Clear Chat"):
    st.session_state.messages = []

# Chat Messages Display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>🧑‍💻 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Extra Feature: Chat Summary
def summarize_chat():
    if st.session_state.messages:
        full_chat = "\n".join([msg['content'] for msg in st.session_state.messages])
        summary = get_response(f"Summarize this conversation briefly:\n{full_chat}")
        st.markdown(f"### 📚 Chat Summary:\n{summary}")

if st.button("📘 Get Chat Summary"):
    summarize_chat()

# Extra Feature: Fun Facts
if st.button("🔔 Random Fun Fact"):
    fact = get_response("Tell me a fun, interesting fact!")
    st.success(f"🎉 {fact}")

# Done! 🎯
