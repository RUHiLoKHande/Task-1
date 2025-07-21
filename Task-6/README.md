# AI Assistant (Text, Image, and PDF Chatbot)

This is a powerful Streamlit-based AI Assistant that allows users to interact with Google Gemini models using text input, images, or PDFs. It supports file uploads (PDFs, JPG/PNG images) and gives AI-powered responses in real time.

---

## Features

- Chat with Gemini 1.5 Flash (Fast) or Gemini 1.5 Pro (Advanced)
- Upload and chat with PDF files (extracts and summarizes content)
- Upload images and ask questions about them
- Maintains chat history for the current session

---

## Note on Image Generation

This application currently **does not support AI image generation** because the **Gemini API for image creation requires a paid (billing-enabled) Google Cloud account**.

You can still upload and analyze images using the **vision model**, but **creating images (like DALL·E or Stable Diffusion) is not possible** unless you integrate a third-party service.

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API (`google.generativeai`)
- PyMuPDF (`fitz`) for reading PDFs
- PIL for image handling
- dotenv for API key management

---

## Setup Instructions
1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

2. **Run the app:**
streamlit run app.py

