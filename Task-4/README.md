# Gemini Knowledge Chatbot

This project is a dynamic, intelligent chatbot built with Streamlit, Google Gemini API, FAISS, and Sentence Transformers. It is capable of updating its knowledge base by scraping live content from web sources such as Wikipedia. The chatbot retrieves the most relevant information using vector similarity search and responds to user questions using Google's Gemini 1.5 model.

## Features

- Dynamically updates its knowledge base using web scraping
- Stores and retrieves contextual data using FAISS vector search
- Embeds text using MiniLM (Sentence Transformers)
- Generates human-like responses using Gemini 1.5 Flash
- Easy-to-use chat interface built with Streamlit
- Supports manual or automatic 24-hour update cycles

# Install dependencies:
pip install -r requirements.txt
# Running the Application
streamlit run app.py

