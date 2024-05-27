from api import apikey
from flask import Flask, request, jsonify
import pandas as pd
from csv import writer
from collections import Counter
import nltk
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import time
import openai
import json
import jsonpickle
from langchain.document_loaders import PyPDFLoader
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
apikeys = apikey
from openai import OpenAI
from api import apikey
client = OpenAI(api_key=apikey)
app = Flask(__name__)


embeddings = OpenAIEmbeddings(openai_api_key=apikey)
db = Chroma(persist_directory="mydb", embedding_function=embeddings)
# db.get()
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# db = Chroma.from_documents(docs, embedding_function)
############################## 
def retrieve_combined_documents(query, max_combined_docs=4):
    retriever = db.as_retriever(search_type="mmr")

    rev_doc = retriever.get_relevant_documents(query)
    lim_rev_doc = rev_doc[:max_combined_docs]

    docs = db.similarity_search(query)
    lim_docs = docs[:max_combined_docs]

    combined_docs = str(lim_rev_doc) + str(lim_docs)
    # combined_docs=db.similarity_search(query)

    return combined_docs


############## GPT PROMPT ####################
def gpt(inp,prompt):
    
    systems = {"role":"system","content":"""
 you are an AI Assistant you name is AAJBot, you are integrated to AA Joyland's whatsapp dont use # for headings use *. 
               your job is to answer the question from the given document about AA Joyland products we serve in pakistan and UAE.
    try to be specific about products. you must be very friendly with user and say ''“Hello from AA Joyland, your 1st choice for family entertainment. How can I help you today?' in the start of convo.
    If user ask about SuperSpaces first confirm him the location:


   BIRTHDAYS
    We Offer Birthday Celebrations at our theme parks if user ask about birthday plans then give answer accordingly:
                            . Super Space Hyderabad
                            . Super Space Millenium Mall
                            . Super Space Ocean Mall
                            . Super Space Shareef Complex 
               
               -  you need to confirm which location he's interested in to celebrate
                            . Bounce Karachi
                            . Giggle Town
                            . Peekabear North Walk
                            . Peekabear Ocean Mall
                            . Super Space Hyderabad
                            . Super Space Millenium Mall
                            . Super Space Ocean Mall
                            . Super Space Shareef Complex 
               - after this you'll return the link of birthday packages specific to location he's interested in like 
                        if he is intrested in Giggle Town you'll send him `www.joyland.com/packages/giggletown`
            - All links are here:
                www.joyland.com/packages/bouncekhi,
               www.joyland.com/packages/peekabearnothwalk
               www.joyland.com/packages/peekabearoceanmall
               www.joyland.com/packages/superspacehyderabad
               www.joyland.com/packages/superspaceoceanmall
               www.joyland.com/packages/superspacemillenium
               www.joyland.com/packages/superspaceshareefcomplex
            - your have to ask his full name after providing packages so our team will reach him out for booking.
            - if they are interested ask for the number of guests, Date and time they wants to come
            - then confirm his name, the facility he picks and the number of guests
FEEDBACK
if user want to give any feedback you have to ask him nicely.

SCHOOL
if user wants to plan school trip in any of our product
- you have ask his school name
- number of students they wants to bring
- Date and time 
- Entity they're intrested 
- after that just tell them our support team will contact them soon
IMPORTANT : Ask one question at a time like : name then number of guests etc
IMPORTANT: if you dont find anything in doc dont say you dont have it in document just tell user that you're unable to provide the information and redirect him to  inquiry@aajoyland.com
IMPORTANT: While providing any link dont use [URL](URL) method just provide the link normal way. 
Important:" your answers should not be too long



"""}
    rcd = retrieve_combined_documents(prompt)
    systems2 = {"role":"system","content":str(rcd)}
    new_inp = inp
    new_inp.insert(0,systems)
    new_inp.insert(1,systems2)
    print("inp : \n ",new_inp)
    # openai.api_key = apikeys
    print('&&&&&&&&&&&&^^^^^^^^^^^^%$######################$%^&*((((((((((((((()))))))))))))))')
    completion = client.chat.completions.create(
    model="gpt-4-turbo-preview", 
    messages=new_inp)
    print(completion)
    return completion

############    GET CHATS BY USER ID ##################
def get_chats(id):
    path = id
    isexist = os.path.exists(path)
    if isexist:
        data = pd.read_json(path)
        chats = data.chat
        return  list(chats)
    else:
        return "No Chat found on this User ID."





############### APPEND NEW CHAT TO USER ID JSON FILE #################
def write_chat(new_data, id):
    with open(id,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["chat"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)



################################ CHECK IF USER IS ALREADY EXIST IF NOT CREATE ONE ELSE RETURN GPT REPLY ##################
@app.route('/chat', methods=['POST'])
def check_user():
    
    ids = request.json['user_id']
    prompt = request.json['prompt']
    # status = request.json['status']
    print("asd")
    path = str(os.getcwd())+'//chats//'+ids+'.json'
    # path = str(os.getcwd())+'\\'+"5467484.json"
    isexist = os.path.exists(path)
    if isexist:
        # try:
        print(path," found!")
        write_chat({"role":"user","content":prompt,"datetime":str(datetime.now())},path)
        # print()
        chats = get_chats(path)
        print(chats)
        send = gpt(chats,prompt)
        reply = send.choices[0].message.content
        print("reply    ",reply)
        write_chat({"role":"assistant","content":reply,"datetime":str(datetime.now())},path)
        return {"message":reply,"status":"OK"}
        # except:
        #     return {"message":"something went wrong!","status":"404"}

    else:
        print(path," Not found!")
        dictionary = {
        "user_id":ids,
        "chat":[]


        }
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        
        # Writing to sample.json
        with open(path, "w") as outfile:
            outfile.write(json_object)
        reply = check_user()
        return reply

####################   NEW ENPOINT GET CHAT ##############################
@app.route('/get_chats', methods=['POST'])
def get_chatss():
    ids = request.json['user_id']
    return jsonpickle.encode(get_chats(ids))

################################# get_latest_datetime_per_json ####################################
def get_latest_datetime_per_json(directory_path):
    """Get the latest datetime from each JSON file in the directory."""
    latest_datetimes = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)['chat']
                # Find the latest datetime in this file
                latest_datetime = max(chat['datetime'] for chat in data)
                # Store it in a dictionary with the filename without extension
                latest_datetimes[os.path.splitext(filename)[0]] = latest_datetime
    return latest_datetimes



# ####################   NEW ENPOINT GET CHAT ##############################
# @app.route('/get_chats', methods=['POST'])
# def get_chatss():
#     ids = request.json['user_id']
#     return jsonpickle.encode(get_chats(ids))

################################# get user number and last message time  ####################################
@app.route('/get_user', methods=['POST'])
def get_user():
    directory_path = 'chats/'  # Update this path
    datetime_info = get_latest_datetime_per_json(directory_path)
    print(datetime_info)
    

################################# ANALYSIS START HERE ####################################
def load_chats(directory_path):
    """ Load chat data from multiple JSON files in a given directory. """
    chats = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):  # Ensure the file is a JSON file
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                chats.extend(json.load(file)['chat'])
    return chats

def count_keywords(chat_data):
    """ Count keywords in chat data, excluding stop words. """
    word_counts = Counter()
    for chat in chat_data:
        # Assuming the chat is a list of dictionaries with keys 'user' and 'assistant'
        user_words = word_tokenize(chat['content'].lower())
        # assistant_words = word_tokenize(chat['assistant'].lower())
        
        # Filter out stop words and count the rest
        words = [word for word in user_words  if word.isalpha() and word not in stop_words]
        word_counts.update(words)
    
    return word_counts

################################# Fetch most used keywords ####################################
@app.route('/keywords', methods=['POST'])
def keywords():
    directory_path = 'chats/'  # Update this path
    all_chats = load_chats(directory_path)
    keyword_counts = count_keywords(all_chats)
    print(keyword_counts.most_common(10))
    return keyword_counts.most_common(10)



if __name__ == '__main__':
    app.run(port=5008,host='0.0.0.0')
    
