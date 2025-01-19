import streamlit as st

from utils import check_states
from aipod.analyzer import PodcastAnalyzer

# Initialize services
analyzer = PodcastAnalyzer(st.secrets["GEMINI_API_KEY"])

if check_states('uploaded_file', 'transcript'):
    with st.spinner("📑 Generating episode page"):
        episode_page = analyzer.generate_episode_page(st.session_state.transcript)
        st.html(episode_page)

else:
    st.warning("Please upload a podcast file first")