import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

#Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

#initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """Analyze text sentiment with adjusted thresholds"""
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.1:
        return 'positive'
    elif scores['compound'] <= -0.1:
        return 'negative'
    return 'neutral'

def get_response(sentiment):
    """Return appropriate response based on sentiment"""
    responses = {
        "positive": [
            "Glad you're happy! How can I help?",
            "Great to hear! What can I do for you today?",
            "Your positivity is wonderful! How may I assist?"
        ],
        "neutral": [
            "How can I help you today?",
            "What would you like to know?",
            "I'm here to help. What do you need?"
        ],
        "negative": [
            "I'm sorry to hear that. How can I help?",
            "Let me help improve your experience.",
            "I understand your concern. How can I assist?"
        ]
    }
    return random.choice(responses[sentiment])

#app layout
st.title("💬 Sentiment Chatbot")
st.caption("I respond differently based on your emotions")

#Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"Detected sentiment: {msg['sentiment']}")

#Chat input
if prompt := st.chat_input("Type a message..."):
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    #Analyze sentiment and get response
    sentiment = get_sentiment(prompt)
    response = get_response(sentiment)
    
    #Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "sentiment": sentiment
    })
    
    #rerun to update the chat
    st.rerun()