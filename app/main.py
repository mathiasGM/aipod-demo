import streamlit as st
from aipod.transcriber import PodcastTranscriber

transcriber = PodcastTranscriber(st.secrets["GEMINI_API_KEY"])

st.markdown("""# Aipod""")

podcast_file = st.file_uploader("Upload podcast", type=["mp3", "mp4", "m4a", "wav"])
if podcast_file:
    st.session_state.uploaded_file = podcast_file

    with st.spinner("🎧 Processing podcast"):
        transcript = transcriber.transcribe(podcast_file.getvalue())
        st.session_state.transcript = transcript
        st.success("Podcast processed successfully") 

st.text("")
st.text("")
st.markdown(
    """
    ##### 💡 Some ideas for future development
    - Short audio clips in summary
    - Let RAG responds with audio clips
    - Generate AI podcast on top - let hosts discuss the podcast
    - Episode2Webpage
    - Webpage2Podcast
    """)