import streamlit as st
import nltk
import fitz  # PyMuPDF
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import heapq
import os

#force download required NLTK data with fallback
def initialize_nltk():
    required_data = [
        ('tokenizers/punkt', 'punkt'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/wordnet', 'wordnet'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('tokenizers/punkt_tab', 'punkt_tab')  # Added this missing resource
    ]
    
    for path, package in required_data:
        try:
            nltk.data.find(path)
        except LookupError:
            st.info(f"Downloading NLTK data: {package}...")
            try:
                nltk.download(package)
            except Exception as e:
                st.warning(f"Could not download {package}: {str(e)}")
                continue

#extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

#extract text from TXT
def extract_text_from_txt(txt_file):
    try:
        return txt_file.read().decode("utf-8").strip()
    except UnicodeDecodeError:
        try:
            return txt_file.read().decode("latin-1").strip()
        except Exception as e:
            st.error(f"Error reading TXT file: {e}")
            return None
    except Exception as e:
        st.error(f"Error reading TXT file: {e}")
        return None

#preprocess text
def preprocess_text(text):
    #remove extra whitespace and newlines
    text = ' '.join(text.split())
    return text

# Summarize text using word frequency
def summarize_text(text, summary_ratio=0.3):
    try:
        #preprocess the text first
        text = preprocess_text(text)
        
        sentences = sent_tokenize(text)
        if not sentences:
            return "No sentences found."

        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        table = str.maketrans("", "", string.punctuation)
        word_freq = {}

        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [word.translate(table) for word in words]
            words = [lemmatizer.lemmatize(w) for w in words if w and w not in stop_words]
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

        if not word_freq:
            return "Not enough meaningful content to summarize."

        max_freq = max(word_freq.values())
        for word in word_freq:
            word_freq[word] /= max_freq

        sentence_scores = {}
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words)
            sentence_scores[sentence] = score

        summary_len = max(1, int(len(sentences) * summary_ratio))
        summary_sentences = heapq.nlargest(summary_len, sentence_scores, key=sentence_scores.get)
        return " ".join(summary_sentences).replace("\n", " ").strip()
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "An error occurred while generating the summary."

#streamlit page setup
st.set_page_config(page_title="📝 Text Summarizer", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; padding: 20px; }
    .preview-box, .summary-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
        max-height: 300px;
        overflow-y: auto;
    }
    h1, h3 { color: #2c3e50; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stDownloadButton>button {
        background-color: #008CBA;
        color: white;
    }
    .stDownloadButton>button:hover {
        background-color: #007B9E;
    }
    .error-box {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #c62828;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("📝 Extractive Text Summarizer")
    st.markdown("Upload a **PDF** or **TXT** file and get a concise summary of the content.")

    #Initialize nltk resources
    with st.spinner("Checking NLTK resources..."):
        initialize_nltk()

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"], 
                                   help="Supported formats: PDF and plain text files")

    if uploaded_file:
        file_details = {"FileName": uploaded_file.name, 
                       "FileType": uploaded_file.type, 
                       "FileSize": f"{uploaded_file.size/1024:.2f} KB"}
        st.write(file_details)

        if uploaded_file.type == "application/pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            document_text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Only PDF and TXT files are supported.")
            return

        if not document_text:
            st.error("Unable to read the uploaded file.")
            return

        st.subheader("📄 Text Preview")
        preview_text = document_text[:1000] + ("..." if len(document_text) > 1000 else "")
        st.markdown(f'<div class="preview-box">{preview_text}</div>', 
                   unsafe_allow_html=True)

        summary_ratio = st.slider(
            "Select Summary Length",
            0.1, 0.5, 0.3, step=0.05,
            help="Adjust the ratio to control how long the summary should be (0.1 = 10%, 0.5 = 50%)"
        )

        if st.button("🧠 Generate Summary"):
            with st.spinner("Analyzing and summarizing the document..."):
                try:
                    summary = summarize_text(document_text, summary_ratio)
                    if summary.startswith("An error occurred"):
                        st.markdown(f'<div class="error-box">{summary}</div>', 
                                  unsafe_allow_html=True)
                    else:
                        st.subheader("🔍 Summary")
                        st.markdown(f'<div class="summary-box">{summary}</div>', 
                                  unsafe_allow_html=True)

                        st.download_button(
                            label="💾 Download Summary",
                            data=summary,
                            file_name=f"summary_{os.path.splitext(uploaded_file.name)[0]}.txt",
                            mime="text/plain",
                            help="Download the generated summary as a text file"
                        )
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()