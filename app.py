
import streamlit as st

from agent import run_agent, conversation
from tools import read_pdf


st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖"
)

st.title("AI Research Agent 🤖")
st.write("Ask me anything")


# --------------------------------
# 1. Initialize conversation
# --------------------------------

if "conversation" not in st.session_state:
    st.session_state.conversation = conversation


# --------------------------------
# 2. Display previous messages
# --------------------------------

for message in st.session_state.conversation:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------
# 3. Chat input with file attachment
# --------------------------------

prompt = st.chat_input(
    "Type your question here...",
    accept_file="multiple",
    file_type=["pdf"]
)


# --------------------------------
# 4. Process question and attachments
# --------------------------------

if prompt:

    question = prompt.text or ""
    uploaded_files = prompt.files

    pdf_text = None

    # --------------------------------
    # Read attached PDFs
    # --------------------------------

    if uploaded_files:

        extracted_documents = []

        for uploaded_file in uploaded_files:

            with st.spinner(
                f"Reading {uploaded_file.name}..."
            ):

                # Save PDF temporarily
                with open("uploaded.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())

                # Extract text using pypdf or OCR
                text = read_pdf("uploaded.pdf")

                if text.startswith("PDF reading error:"):
                    st.error(
                        f"Could not read {uploaded_file.name}: {text}"
                    )
                    continue

                if not text.strip():
                    st.warning(
                        f"No text could be extracted from "
                        f"{uploaded_file.name}."
                    )
                    continue

                extracted_documents.append(
                    f"Document: {uploaded_file.name}\n{text}"
                )

        if extracted_documents:
            pdf_text = "\n\n".join(extracted_documents)

    # --------------------------------
    # Validate input
    # --------------------------------

    if not question.strip() and not pdf_text:
        st.warning(
            "Please enter a question or attach a readable PDF."
        )
        st.stop()

    if uploaded_files and not pdf_text:
        st.error(
            "I couldn't extract readable text from the attached PDF."
        )
        st.stop()

    # --------------------------------
    # Display user's message
    # --------------------------------

    with st.chat_message("user"):

        st.write(
            question or "Please summarize the uploaded PDF."
        )

        for uploaded_file in uploaded_files:
            st.caption(f"📎 {uploaded_file.name}")

    # --------------------------------
    # Tool activity callback
    # --------------------------------

    tool_status = st.empty()

    def show_tool(message):
        tool_status.info(message)

    # --------------------------------
    # Run the agent
    # --------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = run_agent(
                question or "Summarize the uploaded PDF.",
                tool_callback=show_tool,
                pdf_text=pdf_text
            )

        tool_status.empty()

        st.write(answer)

    # --------------------------------
    # Refresh chat
    # --------------------------------

    st.rerun()
