from sentence_transformers import SentenceTransformer

# Load the model once at module-level
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list[float]:
    # Encode returns a numpy array, convert to list
    embedding = model.encode(text)
    return embedding.tolist()
