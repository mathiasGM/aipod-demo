import google.generativeai as genai
import os
from streamlit.runtime.uploaded_file_manager import DeletedFile, UploadedFile
import requests

class PodcastTranscriber:
    def __init__(self, api_key: str = None):
        """Initialize the transcriber with optional API key."""
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def transcribe(self, audio_file: UploadedFile) -> str:
        prompt = "Please transcribe this podcast episode and return the transcribed text"

        LARGE_FILE_THRESHOLD = 60 * 1024 * 1024 
        file_size = audio_file.size  

        if file_size > LARGE_FILE_THRESHOLD:
            print("Processing large file")

            # Save the audio file locally to work with large files
            local_file = "podcast.mp3"
            with open(local_file, "wb") as f:
                f.write(audio_file.read()) 

            f = genai.upload_file(local_file)
            response = self.model.generate_content([
                prompt,
                f
            ])

        else:
            print("Processing small file")
            response = self.model.generate_content([
                prompt,
                {
                    "mime_type": audio_file.type,
                        "data": audio_file.read() 
                    }
            ])
        return response.text