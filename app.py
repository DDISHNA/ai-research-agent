import streamlit as st
from agent import run_agent, conversation

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖"
)

st.title("AI Research Agent 🤖")
st.write("Ask me Anything")

# Initialize conversation for this browser session
if "conversation" not in st.session_state:
    st.session_state.conversation = conversation

#  display previous questions
for message in st.session_state.conversation:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.write(message['content'])
    elif message['role'] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])

# chat input
question = st.chat_input("Type your Questions here.....")

if question:
    # run th existing agent
    answer = run_agent(question)

    # refresh the page
    st.rerun()