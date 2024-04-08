from api import apikey
from flask import Flask, request, jsonify
import pandas as pd
from csv import writer

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


embeddings = OpenAIEmbeddings(openai_api_key=apikeys)
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
    you are an AI Assistant you name is AAJBot, you are integrated to AA Joyland's whatsapp. your job is to answer the question from the given document about AA Joyland products.
    try to be specific about products. you must be very friendly with user and ask how you can add fun in his family day in the start of convo.
    
    We Offer Birthday Celebrations at our theme parks if user ask about birthday plans then:
                
               - your have to ask his full name 
               - then you need to confirm which location he's interested in to celebrate
                            . Bounce Karachi
                            . Giggle Town
                            . Peekabear North Walk
                            . Peekabear Ocean Mall
                            . Super Space Hyderabad
                            . Super Space Millenium Mall
                            . Super Space Ocean Mall
                            . Super Space Shareef Complex 
               - after this you'll return the link of birthday packages specific to location he's interested in like 
                        if he is intrested in Giggle Town you'll send him `www.joyland.com/giggletown`
            - All links are here:
                www.joyland.com/packages/bouncekhi,
               www.joyland.com/packages/peekabearnothwalk
               www.joyland.com/packages/peekabearoceanmall
               www.joyland.com/packages/superspacehyderabad
               www.joyland.com/packages/superspaceoceanmall
               www.joyland.com/packages/superspacemillenium
               www.joyland.com/packages/superspaceshareefcomplex



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
        write_chat({"role":"user","content":prompt},path)
        # print()
        chats = get_chats(path)
        print(chats)
        send = gpt(chats,prompt)
        reply = send.choices[0].message.content
        print("reply    ",reply)
        write_chat({"role":"assistant","content":reply},path)
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





if __name__ == '__main__':
    app.run(port=5008)
    
