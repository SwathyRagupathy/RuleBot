import os
import time
import json
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from gpt4all import GPT4All

# ========== CONFIG ==========
st.set_page_config(page_title="RIT Dining Chatbot", layout="centered")

# ========== SIMPLE ORANGE THEME STYLES ==========
st.markdown("""
    <style>
    body {
        background-color: #fff8f0;
    }
    /* User chat bubble: white background, orange left border */
    .chat-bubble-user {
        background-color: #ffffff;
        border-left: 5px solid #f76b00;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 6px 0;
        width: fit-content;
        max-width: 80%;
    }
    /* Bot chat bubble: light orange background, orange left border */
    .chat-bubble-assistant {
        background-color: #fff1e6;  /* soft light orange */
        border-left: 5px solid #f76b00;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 6px 0;
        width: fit-content;
        max-width: 80%;
    }
    /* Typing indicator style */
    .typing {
        color: #f76b00;
        font-style: italic;
        font-weight: 500;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ========== LOAD FAISS INDEX ==========
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_index_path = os.path.join("venv/faiss_index")
    return FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)

# ========== LOAD LOCAL LLM ==========
@st.cache_resource
def load_llm_model():
    return GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

vectorstore = load_vectorstore()
model = load_llm_model()

# ========== SESSION STATE ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

# ========== HEADER ==========
st.image("venv/data/logo.png", width=1000)
st.markdown("<h1 style='color:#f76b00; margin-bottom:0;'>Dining Service Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:black; margin-bottom:0;'> 📖 Student Employee Guide, Auxiliary Services</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='color:#f76b00; margin-bottom:0;'> Ask questions about rules & policies</h5>", unsafe_allow_html=True)

# ========== DISPLAY CHAT ==========
#for msg in st.session_state.messages:
    #with st.chat_message(msg["role"], avatar="🐯" if msg["role"] == "user" else "🧑🏻‍🍳"):
        #st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🐯"):
            st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🧑🏻‍🍳"):
            st.markdown(f"<div class='chat-bubble-assistant'>{msg['content']}</div>", unsafe_allow_html=True)

# ========== IF CHAT ENDED ==========
if st.session_state.chat_ended:
    st.markdown("👋 Chat ended. Thank you for using the Dining Assistant!")
    if st.button("🔁 Clear Chat and Restart"):
        st.session_state.messages = []
        st.session_state.chat_ended = False
        st.rerun()
    st.stop()

# ========== CHAT INPUT ==========
if prompt := st.chat_input("Type your dining policy question..."):
    user_input = prompt.strip().lower()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐯"):
        st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)

    # Bot response logic
    with st.chat_message("assistant", avatar="🧑🏻‍🍳"):
        thinking = st.empty()
        thinking.markdown("<div class='typing'>RIT Dining Assistant is typing...</div>", unsafe_allow_html=True)

        greeting_keywords = {"hi", "hello", "hey", "yo"}
        exit_keywords = {"exit", "quit", "bye", "goodbye","great,bye", "thanks", "thank you"}

        if user_input in greeting_keywords:
            answer = "👋 Hello! I'm the RIT Dining Assistant. You can ask me about dining rules, meal plans, or policy-related questions."
        elif user_input in exit_keywords:
            answer = "👋 Thank you for using the RIT Dining Assistant. See you next time!"
            st.session_state.chat_ended = True
        else:
            try:
                docs = vectorstore.similarity_search(prompt, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])

                prompt_template = f"""
You are an RIT Dining Assistant. Use ONLY the following context to answer the user's question.

CONTEXT:
{context}

User question: {prompt}

Answer (clear, concise, and policy-based):
""".strip()

                with model.chat_session():
                    answer = model.generate(prompt_template, max_tokens=200)

            except Exception as e:
                answer = "⚠️ Sorry, I couldn't process your question."
                print("Error:", e)

        thinking.markdown(f"<div class='chat-bubble-assistant'>{answer}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # End chat after sending goodbye
        if user_input in exit_keywords:
            time.sleep(1.5)
            st.rerun()