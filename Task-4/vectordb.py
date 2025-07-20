import faiss
import os
import pickle
import numpy as np

def save_faiss(index, metadata, path="data/faiss_index"):
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, os.path.join(path, "index.faiss"))
    with open(os.path.join(path, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)

def load_faiss(path="data/faiss_index"):
    index = faiss.read_index(os.path.join(path, "index.faiss"))
    with open(os.path.join(path, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def create_or_update_faiss(vectors, texts, path="data/faiss_index"):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    save_faiss(index, texts, path)
