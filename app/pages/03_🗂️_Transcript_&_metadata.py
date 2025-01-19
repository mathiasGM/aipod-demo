import streamlit as st
from utils import check_states

from aipod.analyzer import PodcastAnalyzer

# Initialize services
analyzer = PodcastAnalyzer(st.secrets["GEMINI_API_KEY"])

if check_states('uploaded_file', 'transcript'):
    with st.spinner("🗂️ Generating metadata"):
        metadata = analyzer.extract_metadata(st.session_state.transcript)
        st.text_area("Transcript", st.session_state.transcript)
        st.json(metadata)

else:
    st.warning("Please upload a podcast file first")