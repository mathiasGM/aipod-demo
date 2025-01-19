import streamlit as st
from utils import check_states

from aipod.analyzer import PodcastAnalyzer

# Initialize services
analyzer = PodcastAnalyzer(st.secrets["GEMINI_API_KEY"])

if check_states('uploaded_file', 'transcript'):
    with st.spinner("📑 Generating episode page"):
        episode_page = analyzer.generate_episode_page(st.session_state.transcript)
        st.markdown(episode_page, unsafe_allow_html=True)

else:
    st.warning("Please upload a podcast file first")