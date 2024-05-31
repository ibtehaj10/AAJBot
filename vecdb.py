from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from api import apikey

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Directory where uploaded PDFs will be stored
UPLOAD_FOLDER = 'pdfs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to upload PDF files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

# Route to process uploaded PDF files
@app.route('/process', methods=['GET'])
def process_files():
    pdfss = []
    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".pdf"):
            file_path = os.path.join(UPLOAD_FOLDER, file)
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            pdfss.append(pages)

    embeddings = OpenAIEmbeddings(openai_api_key=apikey)
    for i in range(len(pdfss)):
        db = Chroma.from_documents(pdfss[i], embeddings, persist_directory="mydbs")
        db.persist()

    return jsonify({'message': 'New Database has been created...!!!'}), 200


UPLOAD_FOLDER_PKG = 'birthday/'
@app.route('/package', methods=['POST'])
def package():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER_PKG'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    


if __name__ == '__main__':
    app.run(port=5005,host="0.0.0.0")
