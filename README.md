# AAJBot - WhatsApp Integrated AI Chatbot

AAJBot is a WhatsApp integrated AI chatbot designed to assist users with queries related to AA Joyland products and services. The bot can manage user interactions, handle document uploads, and perform chat analysis.

## Project Structure
- main.py: Handles the core chatbot functionalities, including user management, interaction with OpenAI API, and chat analysis.
- vecdb.py: Provides API endpoints for uploading new documents to the vector database, creating a knowledge base for the chatbot.
- wapp.py: Manages the integration with WhatsApp using the pywa library, allowing the bot to interact with users directly on WhatsApp.
  
## Prerequisites
- Python 3.7 or higher
- Flask
- OpenAI API Key
- pywa library

## Installation
Clone the repository:

```sh

git clone https://github.com/yourusername/AAJBot.git

```
cd AAJBot
Install the required packages:

```sh

pip install -r requirements.txt
```
## Set up your environment variables for OpenAI API and WhatsApp credentials:

```sh

export OPENAI_API_KEY='your_openai_api_key'
export WHATSAPP_PHONE_ID='your_whatsapp_phone_id'
export WHATSAPP_TOKEN='your_whatsapp_token'
export WHATSAPP_VERIFY_TOKEN='your_whatsapp_verify_token'
```
## Usage
- Running the Chatbot API (main.py)
Start the Flask server for the chatbot API:

```sh

python main.py
```
This will run the chatbot on http://0.0.0.0:5008.

- Running the Vector Database API (vecdb.py)
Start the Flask server for document upload and processing:

```sh
python vecdb.py
```
This will run the server on http://0.0.0.0:5005.

- Running the WhatsApp Integration (wapp.py)
Start the Flask server for WhatsApp integration:
```sh
python wapp.py
```
This will run the WhatsApp integration on http://0.0.0.0:5001.

#API Endpoints

main.py
- /chat (POST): Handles user interactions and returns chatbot responses.
- /get_chats (POST): Retrieves chat history for a given user.
- /keywords (GET): Analyzes and returns the most common keywords in the chats.
- /hours (GET): Analyzes and returns the distribution of messages by hour.
- /count (GET): Returns the total number of chats and messages.

vecdb.py
- /upload (POST): Uploads a new PDF file to the server.
- /process (GET): Processes uploaded PDFs to create a new vector database.
- /package (POST): Uploads birthday package PDFs to the server.

wapp.py
Listens for incoming WhatsApp messages, processes them using the chatbot, and replies accordingly.
Notes
Ensure your OpenAI API key and WhatsApp credentials are set correctly.
Make sure the directories for storing PDFs (pdfs/, birthday/) exist or are created before running the servers.
