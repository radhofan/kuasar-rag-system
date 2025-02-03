import requests
import chromadb
import uuid  # To generate a unique ID

def get_chroma_client():
    # Initialize the Chroma client with persistence
    client = chromadb.PersistentClient(path="app/data/chromadb")
    # Create or get the collection
    collection = client.get_or_create_collection("embeddings")
    return collection

# Function to store embeddings in Chroma
def store_embedding_in_chroma(collection, unique_id, embedding, file_name):
    try:
        # Check if all lists have the same length
        # print(f"Documents list length: {len([file_name])}")
        # print(f"Embeddings list length: {len([embedding])}")
        # print(f"IDs list length: {len([unique_id])}")

        # Store the embedding
        collection.add(
            documents=[file_name],  # Store the document (file name)
            embeddings=[embedding],  # Store the embedding
            metadatas=[{"source": file_name}],  # Optional metadata
            ids=[unique_id]  # Store the unique ID for the embedding
        )
        print(f"Embedding stored successfully for {file_name} with ID {unique_id}")
    except Exception as e:
        print(f"Error storing embedding in Chroma: {e}")

def generate_embedding_with_ollama(text: str, file_name: str):
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
        # url = "http://localhost:11434/api/embeddings"   
        # payload = {
        #     "prompt": text,
        #     "model": "nomic-embed-text"  
        # }
        # response = requests.post(url, json=payload)
        
        # if response.status_code == 200:
        #     embedding = response.json()["embedding"]

        #     if not embedding:
        #         print("Embedding list is empty.")
        #     else:
        #         print(f"Embedding list contains {len(embedding)} values.")

        #     # Generate a unique ID using UUID
        #     unique_id = str(uuid.uuid4())  # Generate a unique UUID

        #     # Get Chroma client and collection
        #     collection = get_chroma_client()
        #     # print(f"CHROMA COLLECTION NAME: {collection}")

        #     # Store embedding in Chroma with the unique ID
        #     store_embedding_in_chroma(collection, unique_id, embedding, file_name)

        #     # Return the document ID (which is the unique UUID)
        #     return unique_id  # This is the unique document ID that you can use in other functions
        # else:
        #     raise Exception("Failed to generate embedding from Ollama.")
    except Exception as e:
        print(f"Error generating embedding with Ollama: {e}")
        return None
