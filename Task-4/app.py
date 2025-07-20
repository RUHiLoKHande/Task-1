import streamlit as st
from chatbot import query_bot
from scraper import scrape_website
from embedder import embed_texts
from vectordb import create_or_update_faiss
from utils import chunk_text
import threading
import numpy as np

st.set_page_config(page_title="💡 Gemini Knowledge Chatbot")

st.title("💡 Gemini Knowledge Chatbot")
st.write("Ask me anything from the updated knowledge base.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

query = st.chat_input("Type your question...")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    answer = query_bot(query)
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


# Updating vector DB from Wikipedia
def update_vector_db():
    urls = [
        "https://en.wikipedia.org/wiki/Natural_language_processing"
    ]
    chunks = []
    for url in urls:
        text = scrape_website(url)
        chunks.extend(chunk_text(text, max_len=1000))

    embeddings = embed_texts(chunks)
    create_or_update_faiss(np.array(embeddings), chunks)
    print("Vector DB updated!")


# Manual update button
if st.button("🔁 Update Knowledge Now"):
    update_vector_db()
    st.success("Knowledge base updated!")

# Auto-schedule every 24h
def schedule_update():
    update_vector_db()
    threading.Timer(86400, schedule_update).start()

if "started" not in st.session_state:
    schedule_update()
    st.session_state.started = True
