import requests
import numpy as np
import chromadb 
from app.ingestion.embedding import generate_embedding_with_ollama  

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
        document_text = None
        source = None  

        if document_id:
            original_document_text = get_document_from_db(document_id)
            document_text = " ".join(original_document_text[0])
            source = f"Document ID: {document_id}"
        else:
            similar_document = get_similar_document(question)
            document_text = " ".join(similar_document["documents"][0])
            source = f"Similar Document Source: {similar_document['source']}"  

        question_embedded = generate_embedding_with_ollama(question)
        answer_embedded = generate_embedding_with_ollama(document_text)
        similarity_score = cosine_similarity(question_embedded, answer_embedded)

        print("Similarity Score:", similarity_score)

        if similarity_score > 0.1:
            prompt = (f"Based on the given document, provide a clear and precise answer to the question:\n\n"
                f"Document:\n{document_text}\n\n"
                f"Question:\n{question}\n\n"
                f"Your response should include:\n"
                f"- A Comprehensive and Detailed Answer, and an example if possible\n"
                f"- A reference to the document, stating 'Based on the latest documentation' or 'According to my sources, near line X' or 'In this section' if possible\n")
            return call_ollama_for_answer(prompt)

        return ("The document is related to your question, but I couldn't find a direct answer."
                if similarity_score > 0.05 else
                "The document does not seem relevant to your question. Try another document or rephrase the question.")
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."



def estimate_tokens(text: str) -> int:
    average_tokens_per_word = 0.03  
    words = text.split()
    return int(len(words) * average_tokens_per_word)

def call_ollama_for_answer(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {"prompt": prompt, "model": "llama3", "stream": False}

    try:
        prompt_tokens = estimate_tokens(prompt)
        print(f"Estimated prompt tokens: {prompt_tokens}")

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            answer = response.json().get("response", "")
            if answer:
                answer_tokens = estimate_tokens(answer)
                print(f"Estimated answer tokens: {answer_tokens}")

                total_tokens = prompt_tokens + answer_tokens
                print(f"Total estimated tokens used: {total_tokens}")

                return answer, total_tokens
            else:
                raise ValueError("Response field is empty")
        else:
            raise Exception("Failed to get an answer from Ollama.")
    except Exception as e:
        print(f"Error getting answer from Ollama: {e}")
        return "An error occurred while getting the answer."
