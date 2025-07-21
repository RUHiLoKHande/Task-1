import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime
import fitz  # PyMuPDF for PDF reading

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

# Get API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please add it to your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini models
text_model = genai.GenerativeModel("gemini-1.5-flash")
vision_model = genai.GenerativeModel("gemini-1.5-pro-vision")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("AI Assistant")
st.caption("Chat with text, images, or PDFs")

# Sidebar - Settings
with st.sidebar:
    st.header("Settings")
    model_choice = st.radio("Model", ["Fast (Gemini 1.5 Flash)", "Advanced (Gemini 1.5 Pro)"])
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Function to extract PDF text
def extract_pdf_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Function to get Gemini Response
def get_gemini_response(user_input, uploaded_file=None):
    try:
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                pdf_text = extract_pdf_text(uploaded_file)
                response = text_model.generate_content(f"PDF text: {pdf_text[:2000]}\n\nQuery: {user_input}", stream=True)
            else:
                img = Image.open(uploaded_file)
                response = vision_model.generate_content([user_input, img], stream=True)
        else:
            selected_model = text_model if model_choice.startswith("Fast") else genai.GenerativeModel("gemini-1.5-pro")
            response = selected_model.generate_content(user_input, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Uploaded Image", use_column_width=True)

# User input
user_input = st.chat_input("Type your message...")
uploaded_file = st.file_uploader("Upload image or PDF", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")

# On submit
if user_input or uploaded_file:
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Display user input
    with st.chat_message("user"):
        if user_input:
            st.markdown(user_input)
        if uploaded_file and uploaded_file.type.startswith("image/"):
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input or "File uploaded",
        "type": "text" if user_input else "image" if uploaded_file.type.startswith("image/") else "text",
        "time": timestamp
    })

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input, uploaded_file)
            if response:
                response_text = ""
                container = st.empty()
                for chunk in response:
                    if chunk.text:
                        response_text += chunk.text
                        container.markdown(response_text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "type": "text",
                    "time": timestamp
                })