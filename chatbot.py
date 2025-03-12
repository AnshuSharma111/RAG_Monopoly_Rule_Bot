from db import generate_context, add_to_db
from preprocess import generate_chunks
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()


# Set up chroma client
client = chromadb.PersistentClient()

# create collection using multi-qa-mpnet-base-dot-v1 as the embedding model
embedding_model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
class CustomEmbeddingFunction:
    def __call__(self, input: List[str]) -> List[List[float]]:
        return embedding_model.encode(input).tolist()

collection = client.get_or_create_collection(
    name="monopoly",
    embedding_function=CustomEmbeddingFunction()
)

# Add chunks (if not already added)
path = "monopoly.pdf"
chunks = generate_chunks(path)
add_to_db(chunks)

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gen_client = genai.Client(api_key=GEMINI_API_KEY)

def prompt(query):
    context = generate_context(query)

    prompt = f"""
    Context:
    {context}

    Question:
    {query}

    You are an AI assistant answering questions about Monopoly. Use only the retrieved rulebook text as your primary source.

    - If the rulebook explicitly answers the question, provide a concise response.
    - If relevant, add a brief strategy tip to help the player, but do not introduce new facts outside the context.
    - Keep answers **short and structured:  
        Rule-based answer first
        Optional strategy tip (only if relevant)
    - Avoid text such as "according to context" to give away that you are using the context.

    Final Answer:
    """

    answer = gen_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1000,
        )
    )

    return answer.text

while True:
    query = input("Enter your question: (-1 to exit)\n")
    if query == "-1":
        break
    answer = prompt(query)
    print(answer)