from typing import List
import json
import google.generativeai as genai
import typing_extensions as typing


class PodcastAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize the analyzer with optional API key."""
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def summarize(self, transcript: str) -> str:
        prompt = f"""
        Provide a concise summary of this podcast transcript in 2-3 sentences. 
        Focus on the main topic and key message.
        
        Transcript: {transcript}
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def extract_key_insights(self, transcript: str) -> str:
        prompt = f"""
        Extract the most important insights from this podcast transcript.
        Focus on unique, valuable, and actionable takeaways.
        Format each insight as a clear bullet point.
        Include only truly significant insights - quality over quantity.
        
        Respond in markdown format.
        
        Transcript: {transcript}
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def extract_metadata(self, transcript: str) -> dict:

        class MetaData(typing.TypedDict):
            category: str
            topics: List[str]

        prompt = f"""
        Analyze this podcast transcript and extract:
        1. Primary category: Choose the single main category this podcast falls under from:
           Business, Technology, Politics, Science, Sports, Culture, Health, or Education
        2. Specific topics: Key subjects discussed in detail
        
        Format the response as:
        Category: [single category]
        Topics: [topic 1], [topic 2], etc.
        
        Only include topics that are substantially discussed.
        
        Transcript: {transcript}
        """

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=1.0,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type="application/json",
                response_schema=MetaData
            ),)
        
        return json.loads(response.text)
    
    def generate_episode_page(self, transcript: str) -> str:
        
        class PodcastEpisodeSummary(typing.TypedDict):
            html: str

        prompt = f"""
        Create an HTML webpage for this podcast episode. First, generate a short engaging and intriguing title 
        that captures the essence of the episode's main topic or key insight. Format this as an H3 header.
        Then provide a brief summary in plain text, followed by a section called 'Key Takeaways' (formatted as H4) with 3-5 
        bullet points. Each bullet point (takeaway) should have a bold title, brief explanation, and supporting quote in 
        italics from the transcript.
        Transcript: {transcript}. 
        
        ALWAYS RETURN THE JSON RESPONSE in this format: {PodcastEpisodeSummary.__annotations__}
        """

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=1.0,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type="application/json",
                response_schema=PodcastEpisodeSummary
            ),)
        
        return json.loads(response.text)["html"]