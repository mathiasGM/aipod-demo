import streamlit as st
from aipod.transcriber import PodcastTranscriber
from aipod.analyzer import PodcastAnalyzer
from aipod.rag import PodcastRAG

transcriber = PodcastTranscriber(st.secrets["GEMINI_API_KEY"])
analyzer = PodcastAnalyzer(st.secrets["GEMINI_API_KEY"])
rag = PodcastRAG(st.secrets["OPENAI_API_KEY"])

st.markdown("""## Aipod""")
st.text("")
podcast_file = st.file_uploader("Upload podcast episode", type=["mp3", "wav", "m4a"])
st.text("")

if podcast_file:    
    # Use session state to store transcript and processed data
    if 'transcript' not in st.session_state or st.session_state.podcast_file != podcast_file:
        with st.spinner("🎧 Processing your podcast"):
            st.session_state.transcript = transcriber.transcribe(podcast_file.getvalue())
            st.session_state.episode_page = analyzer.generate_episode_page(st.session_state.transcript)
            st.session_state.podcast_file = podcast_file
            rag.create_index([st.session_state.transcript])
            st.session_state.rag = rag
    
    st.text("")
    st.markdown(st.session_state.episode_page, unsafe_allow_html=True)
    st.text("")

    st.markdown("### Podcast Q&A")
    query = st.text_input("Enter your question")
    if query:
        response = st.session_state.rag.query(query)
        st.markdown(response)