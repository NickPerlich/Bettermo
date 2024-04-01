import json
import os
from fastapi import APIRouter, Depends
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests
from unidecode import unidecode
import requests


router = APIRouter(
    prefix="/insertEmbedding",
    tags=["insertEmbedding"],
    #dependencies=[Depends(auth.get_api_key)],
)

model_id = "intfloat/e5-small-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()


class Texts(BaseModel):
    texts: list[str]

@router.post("/")
def update_times(inputs: Texts):

    print(inputs.texts)
    
    embeddings = query(inputs.texts)
    
    try:
        with db.engine.begin() as connection:
            for text, embedding in zip(inputs.texts, embeddings):  
                connection.execute(sqlalchemy.text("insert into items (text_value, embedding) values (:text, :embedding);")
            , {"text": text, "embedding": embedding})
           
     
        return "Ok"
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")
    

