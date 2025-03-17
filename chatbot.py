from db import generate_context
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

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