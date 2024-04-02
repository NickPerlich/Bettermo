import os
import PyPDF2
from fastapi import APIRouter, Depends
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests
import re
import youtube_transcript_api
from tools import get_video_title, break_into_chunks, preprocess_book


router = APIRouter(
    prefix="/insert",
    tags=["insert"],
    #dependencies=[Depends(auth.get_api_key)],
)


class Input(BaseModel):
    link: str

@router.post("/YT")
def update_times(input: Input):

    example_url = input.link
    _id = example_url.split("=")[1].split("&")[0]

    channel_pattern = r'channel=([\w\-]+)'
    
    # Search for the pattern in the URL
    channel = re.search(channel_pattern, example_url)

    title = get_video_title(example_url)

    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(_id)

    text = ""

    for line in transcript:
        text += line['text'] + " "
    

    chunks = break_into_chunks(text)

    print(len(chunks))

    for i in range(len(chunks)):
        print(len(chunks[i]))

    insertChunks(chunks, "YT", author=channel, name=title, link=example_url)

    return "Ok"


class InputPDF(BaseModel):
    filename: str
    startpage: int
    endpage: int


@router.post("/PDF")
def update_times(input: InputPDF):
    filename = input.filename
    startpage = input.startpage
    endpage = input.endpage

    current_path = os.getcwd()
    filepath = current_path + f"/assets/{filename}"

    if filename.endswith('.pdf'):
        pdf_file = open(filepath, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ''
        endpage = int(endpage) if int(endpage) < num_pages else num_pages
        for page_num in range(int(startpage), endpage):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        pdf_file.close()
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()

    chunks = preprocess_book(text)

    with open(filepath + "_preprocessed.txt", 'w', encoding='utf-8') as file:
        file.write(str(chunks))

    print("Inserting chunks:")
    for i in range(0, len(chunks), 100):
        insertChunks(chunks[i:i+100], "PDF")
        print(str(i) + " - " + str(i+100))




model_id = "intfloat/e5-small-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()


def insertChunks(lst, source, name, author, link):

    lst = [chunk for chunk in lst if len(chunk) > 100]

    embeddings = query(lst)
    
    try:
        with db.engine.begin() as connection:
            for text, embedding in zip(lst, embeddings):  
                if text != '':
                    connection.execute(sqlalchemy.text("insert into items (text_value, embedding, source, name, author, link) values (:text, :embedding, ':source', ':name', ':author', 'link');")
            , {"text": text, "embedding": embedding, "source": source, "name": name, "author": author, "link": link})
     
        return "Ok"
    
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")

