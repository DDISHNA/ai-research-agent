import streamlit as st

from agent import run_agent, conversation
from tools import read_pdf


st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖"
)

st.title("AI Research Agent 🤖")
st.write("Ask me Anything")


# --------------------------------
# PDF Upload
# --------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


pdf_text = None


if uploaded_file:

    # Save uploaded PDF temporarily
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read PDF
    pdf_text = read_pdf("uploaded.pdf")

    if pdf_text.startswith("PDF reading error"):

        st.error(pdf_text)

    else:

        st.success("📄 PDF uploaded successfully!")

        st.caption(
            f"Extracted {len(pdf_text)} characters from the PDF."
        )


# --------------------------------
# Conversation
# --------------------------------

st.session_state.conversation = conversation


# Display previous conversation

for message in st.session_state.conversation:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):
            st.write(message["content"])


# --------------------------------
# Chat input
# --------------------------------

question = st.chat_input(
    "Type your Questions here....."
)


if question:

    # --------------------------------
    # Show user's question immediately
    # --------------------------------

    with st.chat_message("user"):
        st.write(question)

    # --------------------------------
    # Tool activity
    # --------------------------------

    tool_status = st.empty()

    def show_tool(message):

        tool_status.info(message)

    # --------------------------------
    # Run agent
    # --------------------------------

    answer = run_agent(
        question,
        tool_callback=show_tool,
        pdf_text=pdf_text
    )

    # --------------------------------
    # Clear tool status
    # --------------------------------

    tool_status.empty()

    # --------------------------------
    # Show final answer
    # --------------------------------

    with st.chat_message("assistant"):
        st.write(answer)

    # --------------------------------
    # Refresh
    # --------------------------------

    st.rerun()