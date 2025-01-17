import google.generativeai as genai


class PodcastTranscriber:
    def __init__(self, api_key: str = None):
        """Initialize the transcriber with optional API key."""
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def transcribe(self, audio_file: bytes) -> str:
        prompt = "Please transcribe this podcast episode and return the transcribed text"
        
        response = self.model.generate_content([
            prompt,
            {
                "mime_type": "audio/mp3",
                "data": audio_file
            }
        ])
        return response.text