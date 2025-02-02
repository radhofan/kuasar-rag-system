from app.ingestion.embedding import generate_embedding_with_ollama  # Import the embedding function
import requests
import numpy as np
import chromadb  # Assuming you have a vector DB for storing embeddings

# Function to calculate cosine similarity between two embeddings
def cosine_similarity(emb1, emb2):
    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    return dot_product / (norm1 * norm2)

def get_document_from_db(document_id):
    """
    Retrieve both the document text and embedding from the ChromaDB vector store.
    """
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path="app/data/chromadb")  # Ensure this path is correct
    collection = client.get_collection("embeddings")  # Ensure this collection exists

    # Retrieve document from ChromaDB
    document_data = collection.get(ids=[document_id])

    if not document_data or "documents" not in document_data or not document_data["documents"]:
        return None, None  # Handle case where document isn't found
    
    document_text = document_data["documents"][0]  # Extract stored text
    document_embedding = document_data["embeddings"][0]  # Extract stored embedding

    return document_text, document_embedding

def generate_answer_from_ollama(document_id, question):
    try:
        # Get the document text and embedding from the DB
        document_text, document_embedding = get_document_from_db(document_id)
        
        if document_text is None or document_embedding is None:
            raise Exception("Document not found in database.")

        # Generate embedding for the question
        question_embedding = generate_embedding_with_ollama(question)
        
        if question_embedding is None:
            raise Exception("Failed to generate question embedding.")

        # Calculate similarity between the document embedding and the question embedding
        similarity = cosine_similarity(document_embedding, question_embedding)
        
        # Set a threshold to decide if the question is relevant to the document
        if similarity < 0.7:  # Adjust threshold based on your requirements
            return "Sorry, I couldn't find a relevant answer to your question."

        # Now `document_text` is properly retrieved and can be used in the prompt
        prompt = f"Given the following document:\n\n{document_text}\n\nAnswer the following question:\n{question}"
        answer = call_ollama_for_answer(prompt)  # Assuming the function exists

        return answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."

# Function to call Ollama for the answer
def call_ollama_for_answer(prompt: str):
    url = "http://localhost:11411/v1/answer"  # Ollama endpoint for answering
    payload = {"prompt": prompt, "model": "answer-model"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["answer"]
        else:
            raise Exception("Failed to get an answer from Ollama.")
    except Exception as e:
        print(f"Error getting answer from Ollama: {e}")
        return "An error occurred while getting the answer."
