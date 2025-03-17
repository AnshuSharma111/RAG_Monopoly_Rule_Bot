import chromadb
from sentence_transformers import SentenceTransformer
from typing import List
from preprocess import generate_chunks
import hashlib

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

def generate_id (text, index):
    hash_value = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"chunk_{index}_{hash_value}"

def is_chunk_already_stored(chunk_id):
    """Check if a chunk is already in ChromaDB."""
    existing = collection.get(ids=[chunk_id])
    return len(existing["ids"]) > 0

def add_to_db(chunks):
    for i in range(len(chunks)):
        chunk_id = generate_id(chunks[i], i)
        if not is_chunk_already_stored(chunk_id):
            collection.add(
                documents=[chunks[i]],
                metadatas=[{
                    "chunk_id":i,
                    "source":"monopoly"
                }],
                ids=[chunk_id]
            )
        else:
            print(f"Chunk {i} already stored in ChromaDB")

# Generate context for chatbot to use
def generate_context (query):
    result = collection.query(
        query_texts=[query],
        n_results=5
    )
    retrieved_texts = result["documents"][0] if "documents" in result else []
    print("CONTEXT PROVIDED:\n", retrieved_texts, "\n\n")
    # Format context as a single string
    context = "\n\n".join(retrieved_texts)  

    return context

print("Generating chunks...")
chunks = generate_chunks("monopoly.pdf")
print("Adding chunks to ChromaDB...")
add_to_db(chunks)
print("Done!")