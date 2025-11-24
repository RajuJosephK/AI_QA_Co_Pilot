import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def get_embedding(text: str):
    response = client.embeddings.create(
        model="google/gemini-embedding-001",
        input=text
    )
    return response.data[0].embedding
