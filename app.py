import streamlit as st
from agent import run_agent, conversation

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖"
)

st.title("AI Research Agent 🤖")
st.write("Ask me Anything")


#  display previous questions
for message in conversation:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.write(message['content'])
    elif message['role'] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])

# chat input
question = st.chat_input("Type your Questions here.....")

if question:
    # display users' question immediately
    with st.chat_message("user"):
        st.write(question)
    answer = run_agent(question)

    # display agent answer
    with st.chat_message("assistant"):
        st.write(answer)