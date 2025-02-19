import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Hack for streamlit cloud
from aipod.transcriber import PodcastTranscriber

transcriber = PodcastTranscriber(st.secrets["GEMINI_API_KEY"])

st.markdown("""# Aipod""")

podcast_file = st.file_uploader("Upload podcast", type=["mp3", "mp4", "m4a", "wav"])
if podcast_file:
    st.session_state.uploaded_file = podcast_file

    with st.spinner("🎧 Processing podcast"):
        transcript = transcriber.transcribe(podcast_file)
        st.session_state.transcript = transcript
        st.success("Podcast processed successfully") 

st.text("")
st.text("")