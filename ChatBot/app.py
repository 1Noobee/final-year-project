# Import necessary libraries
import gradio as gr
import datetime
import time
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser

# Load environment variables
_ = load_dotenv(find_dotenv())

# Determine LLM model name based on current date
current_date = datetime.datetime.now().date()
llm_name = "gpt-3.5-turbo-0301" if current_date < datetime.date(2023, 9, 2) else "gpt-3.5-turbo"

# Initialize components
embedding = OpenAIEmbeddings()  # Initialize OpenAI Embeddings
persist_directory = './docs/chroma/'  # Set the directory for persisting Chroma data
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)  # Initialize Chroma vector store
llm = ChatOpenAI(model_name=llm_name, temperature=0.2)  # Initialize OpenAI Chat Model

# Define template for conversation prompt
template = """To answer your question about the Nigerian Constitution using our AI-based question-answering system, consider the following:
    - Our system is designed and implemented specifically for this purpose, leveraging artificial intelligence and natural language processing.
    - We have extensively studied the Nigerian Constitution and incorporated its provisions into our system's knowledge base.
    - Our system's architecture allows for efficient retrieval and analysis of relevant information from the Constitution.
    {context}
    Previous conversation:
    {chat_history}
    New question about the Nigerian Constitution: {question}
    Response:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)  # Define prompt template for the QA chain

# Define memory for conversation buffer
memory = ConversationBufferMemory(
    memory_key="chat_history",
    output_key='answer',
    return_messages=True
)

# Initialize retriever for vector search
retriever = vectordb.as_retriever(search_kwargs={"k": 2})  # Initialize retriever for vector search

# Define function for chatting with the AI
def chat_with_lawio(prompt, history):
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        get_chat_history=lambda h: h,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
    )  # Initialize ConversationalRetrievalChain
    result = chain({"question": prompt})  # Get result from the chain
    answer_len = len(result["answer"])  # Get length of the answer
    output = result["answer"]  # Get the answer
    for i in range(min(answer_len, answer_len + 5)):  # Iterate over the answer
        time.sleep(0.001)  # Add a delay
        yield output[: i+1]  # Yield partial output

# Define app interface
title = "LAW.IO"  # Set title for the app
css = ".gradio-container {background-color: green}"  # Define custom CSS for the app
app = gr.ChatInterface(
    fn=chat_with_lawio,
    title=title,
    retry_btn=None,
    undo_btn=None,
    clear_btn=None,
    theme=gr.themes.Glass(),
    css=css
).queue()

# Launch the app
app.launch(
    server_name="127.0.0.1",
    server_port=7860,
   
    inline=False
)
