import streamlit as st
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


DetectorFactory.seed = 0
nltk.download('vader_lexicon', quiet=True)


class MultilingualChatbot:
    def __init__(self):
        
        self.supported_languages = {
            'en': {
                'name': 'English',
                'positive': 'Your positivity is wonderful! How may I assist?',
                'negative': 'I understand your concern. How can I help?',
                'neutral': 'How can I help you today?',
                'keywords': ['hello', 'hi', 'hey', 'what', 'how']
            },
            'hi': {
                'name': 'Hindi',
                'positive': 'आपकी सकारात्मकता अद्भुत है! मैं आपकी कैसे मदद कर सकता हूँ?',
                'negative': 'मैं आपकी चिंता समझता हूँ। मैं आपकी कैसे मदद कर सकता हूँ?',
                'neutral': 'मैं आज आपकी कैसे मदद कर सकता हूँ?',
                'keywords': ['नमस्ते', 'हाय', 'कैसे', 'क्या']
            },
            'es': {
                'name': 'Spanish',
                'positive': '¡Tu positividad es maravillosa! ¿Cómo puedo ayudarte?',
                'negative': 'Entiendo tu preocupación. ¿Cómo puedo ayudarte?',
                'neutral': '¿Cómo puedo ayudarte hoy?',
                'keywords': ['hola', 'qué', 'cómo', 'ayuda']
            },
            'de': {
                'name': 'German',
                'positive': 'Ihre Positivität ist wunderbar! Wie kann ich helfen?',
                'negative': 'Ich verstehe Ihre Bedenken. Wie kann ich helfen?',
                'neutral': 'Wie kann ich Ihnen heute helfen?',
                'keywords': ['hallo', 'wie', 'hilfe']
            },
            'fr': {
                'name': 'French',
                'positive': 'Votre positivité est merveilleuse ! Comment puis-je vous aider ?',
                'negative': 'Je comprends votre préoccupation. Comment puis-je vous aider ?',
                'neutral': 'Comment puis-je vous aider aujourd\'hui ?',
                'keywords': ['bonjour', 'comment', 'vous', 'heure']
            }
        }

        self.context = []  

        #load dialoGPT model for english response generation
        self.generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-small",
            tokenizer="microsoft/DialoGPT-small",
            device=-1  
        )

        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def detect_language(self, text):
        """Detects user language using langdetect or fallback keyword check."""
        try:
            lang_code = detect(text)
            if lang_code in self.supported_languages:
                return lang_code
        except:
            pass

       
        text_lower = text.lower().strip()
        for lang, data in self.supported_languages.items():
            if any(keyword in text_lower for keyword in data['keywords']):
                return lang

        return 'en'  

    def translate_text(self, text, target_lang):
        """Translate text to the desired language using deep_translator."""
        try:
            if target_lang == 'en' or not text.strip():
                return text
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        except:
            return text  

    def analyze_sentiment(self, text):
        """Performs sentiment analysis and returns label."""
        try:
            scores = self.sentiment_analyzer.polarity_scores(text)
            if scores['compound'] > 0.05:
                return 'positive'
            elif scores['compound'] < -0.05:
                return 'negative'
            else:
                return 'neutral'
        except:
            return 'neutral'

    def generate_response(self, prompt, sentiment, lang):
        """Generates a response using context and sentiment prefix."""
        try:
           
            context_prompt = f"{' '.join(self.context[-3:])} {prompt}" if self.context else prompt

            result = self.generator(
                context_prompt,
                max_length=100,
                num_return_sequences=1,
                pad_token_id=50256,
                do_sample=True,
                top_k=40,
                top_p=0.9
            )
            raw_reply = result[0]['generated_text'].replace(context_prompt, '').strip()

            
            prefix = self.supported_languages.get(lang, self.supported_languages['en']).get(sentiment, '')
            response = f"{prefix} {raw_reply}"

            
            self.context.append(prompt)
            self.context.append(response)
            self.context = self.context[-10:]

            return response
        except:
            return "I'm having trouble responding right now. Please try again later."

def main():
    st.set_page_config(page_title="Multilingual Chatbot", page_icon="🤖")
    st.title("🤖 Smart Multilingual Chatbot")

   
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = MultilingualChatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.markdown("**Supported Languages:**")
    for code, lang in st.session_state.chatbot.supported_languages.items():
        st.write(f"• {lang['name']} ({code})")

    
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("👤 You:", key="user_input")
        submit_button = st.form_submit_button(label="Send")

    
    if submit_button and user_input:
        if user_input.lower() in ["exit", "quit", "bye"]:
            st.session_state.messages.append({
                "role": "assistant", "content": "Goodbye! Have a great day! 👋", "lang": "en"
            })
        else:
           
            user_lang = st.session_state.chatbot.detect_language(user_input)
            sentiment = st.session_state.chatbot.analyze_sentiment(user_input)

            st.write(f"🌐 Detected: {st.session_state.chatbot.supported_languages[user_lang]['name']} | Sentiment: {sentiment}")

            
            english_input = (
                st.session_state.chatbot.translate_text(user_input, 'en')
                if user_lang != 'en' else user_input
            )

           
            english_response = st.session_state.chatbot.generate_response(english_input, sentiment, user_lang)
            final_response = (
                st.session_state.chatbot.translate_text(english_response, user_lang)
                if user_lang != 'en' else english_response
            )

        
            st.session_state.messages.append({
                "role": "user", "content": user_input, "lang": user_lang
            })
            st.session_state.messages.append({
                "role": "assistant", "content": final_response, "lang": user_lang
            })


    st.markdown("### 💬 Chat History")
    for msg in st.session_state.messages:
        speaker = "👤 You" if msg["role"] == "user" else "🤖 Bot"
        lang_name = st.session_state.chatbot.supported_languages[msg["lang"]]['name']
        st.markdown(f"**{speaker}** ({lang_name}): {msg['content']}")

if __name__ == "__main__":
    main()
