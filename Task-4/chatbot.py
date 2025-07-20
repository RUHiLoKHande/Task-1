import google.generativeai as genai
from embedder import embed_texts
from vectordb import load_faiss
import numpy as np

genai.configure(api_key="AIzaSyDjDapkVSfBf6djZBhvuvNa4FV9VvLwNiU")  # Replace with your Gemini API key

def query_bot(query):
    index, texts = load_faiss()
    q_vec = embed_texts([query])
    D, I = index.search(np.array(q_vec), k=3)

    relevant_chunks = [texts[i] for i in I[0] if i < len(texts)]
    context = "\n".join(relevant_chunks)

    prompt = f"""You are a helpful assistant. Use the context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Answer:"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
