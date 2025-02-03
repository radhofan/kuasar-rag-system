import json
from app.ingestion.embedding import generate_embedding_with_ollama  # Import the embedding function
import requests
import numpy as np
import chromadb  

def cosine_similarity(emb1, emb2):
    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    return dot_product / (norm1 * norm2)

def get_document_from_db(document_id):
    client = chromadb.PersistentClient(path="app/data/chromadb")  
    collection = client.get_collection("embeddings")  

    document_data = collection.get(ids=[document_id])
    
    document_text = document_data["documents"]  

    return document_text

def generate_answer_from_ollama(document_id, question):
    try:
        document_text= get_document_from_db(document_id)
        prompt = f"Given the following document:\n{document_text}.\nAnswer the following question:\n{question}.\n"
        # print(prompt)
        answer = call_ollama_for_answer(prompt) 
        # print("This is the answer: ", answer) 

        return answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."

def call_ollama_for_answer(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {"prompt": prompt, "model": "llama3", "stream": False}

    try:
        # Send the request
        response = requests.post(url, json=payload)
        # print(response.text)
        if response.status_code == 200:
            # Extract the answer directly from the response
            answer = response.json().get("response", "")  # Get the "response" field
            if answer:  # Check if the answer exists
                return answer  # Return the plain string
            else:
                raise ValueError("Response field is empty")
        else:
            raise Exception("Failed to get an answer from Ollama.")
    except Exception as e:
        print(f"Error getting answer from Ollama: {e}")
        return "An error occurred while getting the answer."
