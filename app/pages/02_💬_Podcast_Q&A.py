import streamlit as st
from utils import check_states

from aipod.rag import PodcastRAG

rag = PodcastRAG(st.secrets["OPENAI_API_KEY"])

if check_states('uploaded_file', 'transcript'):
    with st.spinner("🎧 Indexing podcast"):
        rag.create_index([st.session_state.transcript])
        st.session_state.rag = rag

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if query := st.chat_input("Ask a question about the podcast"):
        # Display user message in chat message container
        st.chat_message("user").markdown(query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        # Get response from RAG
        with st.spinner("💭 Thinking..."):
            response = st.session_state.rag.query(query)
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.warning("Please upload a podcast file first")