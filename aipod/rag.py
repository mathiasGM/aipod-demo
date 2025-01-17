from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings


class PodcastRAG:
    def __init__(self, openai_api_key: str):
        """Initialize the RAG system."""
        self.index = None
        self.query_engine = None
        Settings.llm = OpenAI(temperature=0.3, model="gpt-4o-mini",api_key=openai_api_key)

    def create_index(self, transcripts: list[str]):
        """Create a vector index from a list of podcast transcripts."""
        documents = [Document(text=t) for t in transcripts]
        self.index = VectorStoreIndex.from_documents(documents)
        self.query_engine = self.index.as_query_engine()

    def query(self, query_text: str) -> str:
        """Query the index and return the response."""
        if not self.query_engine:
            raise ValueError("Index has not been created yet. Call create_index() first.")
        
        response = self.query_engine.query(query_text)
        return str(response)