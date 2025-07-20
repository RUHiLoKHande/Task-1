import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# title
st.title("📝 Multi-LLM Article Generator")

# this is for model selection
llm_choice = st.selectbox(
    "Choose an LLM Model",
    ["Llama3", "Mistral", "Falcon"]
)

# I use the coditional statemrnt for selection of LLMs 
if llm_choice == "Llama3":
    llm = Ollama(model="llama3.1")  #the most appropriate model for article creation
elif llm_choice == "Mistral":
    llm = Ollama(model="mistral")   #it is fast and efficient but  short articles
elif llm_choice == "Falcon":
    llm = Ollama(model="falcon")    #open-source good factual accuracy Best for technical & factual content

# inlize the prompt for article generation
article_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI writer. Generate a detailed, well-structured, and informative article on the given topic."),
    ("user", "Topic: {topic}")
])

# input for article topic
topic = st.text_input("Enter the topic for your article:")

# run the model
if st.button("Submit"):
    if topic:
           output_parser = StrOutputParser()
           chain = article_prompt | llm | output_parser
           generated_article = chain.invoke({"topic": topic})
    else:
        st.warning("Please enter the topic before submiitig")
    
        
 
    # display Output
    st.subheader("Generated Article:")
    st.write(generated_article)
