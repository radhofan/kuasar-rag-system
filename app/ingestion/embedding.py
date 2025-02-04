import chromadb
import uuid 
import requests

# def get_chroma_client():
#     client = chromadb.PersistentClient(path="app/data/chromadb")
#     collection = client.get_or_create_collection("embeddings")
#     return collection

# def store_embedding_in_chroma(collection, unique_id, embedding, file_name):
#     try:
#         collection.add(
#             documents=[file_name],  
#             embeddings=[embedding],  
#             metadatas=[{"source": file_name}],  
#             ids=[unique_id]  
#         )
#         print(f"Embedding stored successfully for {file_name} with ID {unique_id}")
#     except Exception as e:
#         print(f"Error storing embedding in Chroma: {e}")

def generate_embedding_with_ollama(text: str):
    try:
        url = "http://localhost:11434/api/embeddings"   
        payload = {
            "prompt": text,
            "model": "nomic-embed-text"  
        }
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            embedding = response.json()["embedding"]
            return embedding
        else:
            raise Exception("Failed to generate embedding from Ollama.")
    except Exception as e:
        print(f"Error generating embedding with Ollama: {e}")
        return None
    
def store_file_chroma(text: str, file_name: str):
    try:
        client = chromadb.PersistentClient(path="app/data/chromadb")
        collection = client.get_or_create_collection("embeddings")
        unique_id = str(uuid.uuid4())
        collection.add(
            documents=[text],
             metadatas=[{"file_name": file_name}],
            ids=[unique_id ]
        )
        return unique_id
    except Exception as e:
        print(f"Error generating embedding with Ollama: {e}")
        return None
