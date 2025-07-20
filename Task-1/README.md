Please Read this before using app: 
In this project, I have used Ollama as the main framework to implement an article generator chatbot using three different
open-source LLMs:
        1.Llama3 – Best for generating detailed, well-structured long-form content.
        2.Mistral – Optimized for speed and concise text generation.
        3.Falcon – Good for factual and technical content.
The chatbot allows users to select an LLM model, enter a topic, and generate an AI-written article based on their input.


How to Run the model :
    1.Make sure you have Streamlit and LangChain installed. If not, install them using:
        pip install streamlit 
        pip install langchain-community
    2.Ollama provides an easy way to run open-source LLMs locally.
        Download the Ollama installer from the official website
        Run the installer
        Open Command Prompt:
            ollama pull llama3
            ollama pull mistral
            ollama pull falcon
    3. Running the Streamlit App
        streamlit run app.py




