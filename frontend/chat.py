import streamlit as st
import requests
import uuid

API_URL = "https://lemniscarag-1.onrender.com"

st.set_page_config(page_title="ClearPath RAG Chat", layout="wide")

st.title("📄 ClearPath Documentation Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = f"conv_{uuid.uuid4().hex[:8]}"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
question = st.chat_input("Ask about ClearPath documentation...")

if question:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    # Call API
    payload = {
        "question": question,
        "conversation_id": st.session_state.conversation_id
    }

    response = requests.post(API_URL, json=payload)

    data = response.json()

    answer = data["answer"]

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):

        st.write(answer)

        # Sources
        st.subheader("Sources")

        for source in data["sources"]:
            st.write(
                f"- {source['document']} "
                f"(score: {source['relevance_score']})"
            )

        # Metadata
        with st.expander("Metadata"):

            st.json(data["metadata"])