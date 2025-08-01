# === utils/embedder.py ===
import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Use MiniLM model (small + fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_DIR = "faiss_index"
INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
META_PATH = os.path.join(INDEX_DIR, "meta.pkl")

# Create and store embeddings
def generate_and_store_embeddings(chunks):
    os.makedirs(INDEX_DIR, exist_ok=True)
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)

# Query the FAISS index
def query_top_chunks(query, top_k=3):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)
    q_embed = model.encode([query])
    D, I = index.search(np.array(q_embed), top_k)
    top_chunks = [chunks[i] for i in I[0]]
    return top_chunks