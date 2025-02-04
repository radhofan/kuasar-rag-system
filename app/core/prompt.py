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

def get_similar_document(question):
    client = chromadb.PersistentClient(path="app/data/chromadb")
    collection = client.get_collection("embeddings") 
    answer = collection.query(
        query_texts=[question],
        n_results=1,
    )
    return answer

def generate_answer_from_ollama(document_id, question):
    try:
        if document_id is not None: 
            document_text = get_document_from_db(document_id)
            # print(document_text)
            original_document_text = document_text
            document_text = document_text[0]
            document_text = " ".join(document_text)
            question_embedded = generate_embedding_with_ollama(question)
            answer_embedded = generate_embedding_with_ollama(document_text)
            similarity_score = cosine_similarity(question_embedded, answer_embedded)
            print("Similarity Score: ", similarity_score)
            if similarity_score > 0.1:  
                prompt = f"Given the following document:\n{original_document_text}.\nAnswer the following question:\n{question}.\n"
                answer = call_ollama_for_answer(prompt)
                return answer if answer else "The document is relevant, but no specific answer was found."

            elif similarity_score > 0.05:  
                return "The document is related to your question, but I couldn't find a direct answer."

            else:  
                return "The document does not seem relevant to your question. Try another document or rephrase the question."
        else:
            document_text = get_similar_document(question)
            document_text = document_text["documents"][0]
            document_text = " ".join(document_text)
            question_embedded = generate_embedding_with_ollama(question)
            answer_embedded = generate_embedding_with_ollama(document_text)
            similarity_score = cosine_similarity(question_embedded, answer_embedded)
            print("Similarity Score: ", similarity_score)
            if similarity_score > 0.1:  
                prompt = f"Given the following document:\n{document_text}.\nAnswer the following question:\n{question}.\n"
                answer = call_ollama_for_answer(prompt)
                return answer if answer else "The document is relevant, but no specific answer was found."

            elif similarity_score > 0.05:  
                return "The document is related to your question, but I couldn't find a direct answer."

            else:  
                return "The document does not seem relevant to your question. Try another document or rephrase the question." 
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."


def call_ollama_for_answer(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {"prompt": prompt, "model": "llama3", "stream": False}

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            answer = response.json().get("response", "")  
            if answer:  
                return answer  
            else:
                raise ValueError("Response field is empty")
        else:
            raise Exception("Failed to get an answer from Ollama.")
    except Exception as e:
        print(f"Error getting answer from Ollama: {e}")
        return "An error occurred while getting the answer."
