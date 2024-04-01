import json
import os
import unicodedata
from fastapi import APIRouter, Depends
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
from unidecode import unidecode
import requests
import re
import PyPDF2


router = APIRouter(
    prefix="/insertPDF",
    tags=["insertPDF"],
    #dependencies=[Depends(auth.get_api_key)],
)


def preprocess_book(text):

    # Remove header/footer patterns
    text = re.sub(r'(?m)^\(c\) \w+\s\d{4}.*?$', '', text)  # Remove copyright lines
    text = re.sub(r'(?m)^Chapter \d+\s*$', '', text)  # Remove chapter headers
    
    # Remove page numbers
    text = re.sub(r'(?m)^\d+\s*$', '', text)  # Remove line numbers
    
    # Normalize text (optional)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Split into input units (e.g., paragraphs)
    paragraphs = re.split(r'\n\n+', text)
    
    preprocessed_inputs = []
    for paragraph in paragraphs:
        if len(paragraph) > 0:
            preprocessed_inputs.append(paragraph)
    
    return preprocessed_inputs

model_id = "intfloat/e5-small-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()


def insertChunks(lst):
     
    embeddings = query(lst)
    
    try:
        with db.engine.begin() as connection:
            for text, embedding in zip(lst, embeddings):  
                connection.execute(sqlalchemy.text("insert into items (text_value, embedding) values (:text, :embedding);")
            , {"text": text, "embedding": embedding})
     
        return "Ok"
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")



@router.post("/{filename}")
def update_times(filename, startpage, endpage):

    current_path = os.getcwd()
    filepath = current_path + f"/assets/{filename}"

    if filename.endswith('.pdf'):
        pdf_file = open(filepath, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        pdf_file.close()
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()

    chunks = preprocess_book(text)

    with open(filepath + "_preprocessed.txt", 'w', encoding='utf-8') as file:
        file.write(str(chunks))

    for i in range(0, len(chunks), 100):
        insertChunks(chunks[i:i+100])
        print(i)
