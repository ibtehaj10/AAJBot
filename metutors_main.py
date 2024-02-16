import os
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFDirectoryLoader, CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from api import apikey
from flask import Flask, request, jsonify
import pandas as pd
from csv import writer
import time
import json
import jsonpickle
from langchain.document_loaders import PyPDFLoader
apikeys = apikey

app = Flask(__name__)


document = []
document_folder_path = "new/"
OPENAI_API_KEY = "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"
def vactorDB():
    for file in os.listdir(document_folder_path):
        if file.endswith((".pdf")):
            file_path = os.path.join(document_folder_path, file)
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            document.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200, length_function=len)
    docs = text_splitter.split_documents(document)
    gds_data_split = docs

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    support_data = gds_data_split
    support_store = Chroma.from_documents(support_data, embeddings, collection_name="support",persist_directory="support_store")
    # print('support_data : ',support_data)
    return support_store


@app.route('/chat', methods=['POST'])
def answer_question():
    question = request.json['prompt']

    
 

    DEFAULT_SYSTEM_PROMPT = """
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
        """.strip()

    def generate_prompt(prompt, system_prompt=DEFAULT_SYSTEM_PROMPT):
            return f"""
        [INST] <>
        {system_prompt}
        <>

        {prompt} [/INST]
        """.strip()

    SYSTEM_PROMPT = "Use the following pieces of context to answer the question at the end. Don't try to make up an answer."

    template = generate_prompt(
            """
        {context}

        Question: {question}
        """,
            system_prompt=SYSTEM_PROMPT,
        )
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        result = qa_chain(question)['result'].strip()
        result = str(result)
        results.append(result)

    return results



# Example usage





if __name__ == '__main__':
    app.run()
    