import re
import unicodedata
from pytube import YouTube

def get_video_title(video_url):
    try:
        yt = YouTube(video_url)
        return yt.title
    except Exception as e:
        print("Error:", e)
        return None
    

def break_into_chunks(text, max_words=200, overlap=30):

    # Split the text into words
    words = re.findall(r'\w+', text)
    
    chunks = []
    current_chunk = []
    
    for i, word in enumerate(words):
        # If adding the current word to the current chunk would exceed the max word limit,
        # add the current chunk to the list of chunks and start a new chunk
        if len(current_chunk) + 1 > max_words:
            chunks.append(' '.join(current_chunk[:-overlap]))
            current_chunk = current_chunk[-overlap:]
        
        # Add the current word to the current chunk
        current_chunk.append(word)
    
    # Add the last chunk to the list of chunks
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    chunks = [chunk for chunk in chunks if len(chunk) > 80]

    return chunks


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