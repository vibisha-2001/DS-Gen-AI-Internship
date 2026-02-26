import streamlit as st
from backend.groq_client import generate_response
from backend.prompt_engine import career_advisor_prompt

st.set_page_config(page_title="Career Advisor Chatbot")

st.title("🎓 Career Advisor Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)

user_input = st.chat_input("Ask your career question...")

if user_input:

    messages = []

    system_prompt = career_advisor_prompt()
    messages.append({"role": "system", "content": system_prompt})

    for role, message in st.session_state.chat_history:
        messages.append({"role": role, "content": message})

    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(messages)
            st.write(response)

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", response))

if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()