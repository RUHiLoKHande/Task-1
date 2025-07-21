## Multilingual Sentiment-Aware Chatbot
This is a smart multilingual chatbot built with Streamlit that detects the user's language and sentiment, translates the input, generates a response using a pretrained DialoGPT model, and responds accordingly with emotion-aware messages. It supports English, Hindi, Spanish, German, and French.

## Features
 Automatic language detection (using langdetect)
 Sentiment analysis (positive, neutral, negative using VADER)
 AI response generation (using HuggingFace DialoGPT)
 Multilingual support (translation powered by deep-translator)
 Conversation memory (retains context for smoother interactions)
 Streamlit UI for chat-based interaction

 ## How to Run the App
 pip install -r requirements.txt
 streamlit run app.py
