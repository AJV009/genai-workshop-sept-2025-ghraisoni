"""
INDEX.PY - Document Indexing Script

What it does:
- Loads all text files from the source_text folder
- Splits them into smaller chunks for better search results
- Converts each chunk into embeddings using Google Gemini
- Stores the embeddings in Pinecone vector database for fast similarity search

How it works:
1. Finds all .txt files in the source_text directory
2. Reads each file content
3. Splits the text into chunks of 500 words each using a simple word-based splitter
4. For each chunk:
   - Generates an embedding using Gemini
   - Creates a unique ID based on filename and chunk number
   - Stores in Pinecone with the original text as metadata
5. Prints progress as it processes each file

Run this once to index all your documents before using the chatbot.
"""

import os
import glob
from pinecone import Pinecone
from dotenv import load_dotenv
from embedding import get_embedding

load_dotenv()

# Initialize clients
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def simple_text_splitter(text, chunk_size=500):
    """Simple text splitter that splits text into chunks"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def load_and_index_files():
    """Load all text files and index them in Pinecone"""
    txt_files = glob.glob("source_text/*.txt")
    
    for file_path in txt_files:
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        chunks = simple_text_splitter(content)
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{os.path.basename(file_path)}_{i}"
            embedding = get_embedding(chunk)
            
            index.upsert(vectors=[{
                "id": chunk_id,
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "filename": os.path.basename(file_path)
                }
            }])
        
        print(f"Indexed {len(chunks)} chunks from {file_path}")

if __name__ == "__main__":
    load_and_index_files()
    print("All files indexed successfully!")