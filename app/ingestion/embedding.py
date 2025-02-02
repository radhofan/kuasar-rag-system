import requests
import chromadb
import uuid  # To generate a unique ID

# Initialize the Chroma client and collection
def get_chroma_client():
    client = chromadb.Client()
    collection = client.create_collection("embeddings", persist_directory="app/data/chromadb")
    return collection

# Function to store embeddings in Chroma
def store_embedding_in_chroma(collection, unique_id, embedding, file_name):
    try:
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

# Function to generate embedding and store it in Chroma
def generate_embedding_with_ollama(text: str, file_name: str):
    try:
        url = "http://localhost:11411/v1/embedding"  # Ollama API URL
        payload = {
            "text": text,
            "model": "embed-model"  # Adjust model name if necessary
        }
        response = requests.post(url, json=payload)
        
        # Check if the response is valid
        if response.status_code == 200:
            embedding = response.json()["embedding"]
            
            # Generate a unique ID using UUID
            unique_id = str(uuid.uuid4())  # Generate a unique UUID

            # Get Chroma client and collection
            collection = get_chroma_client()

            # Store embedding in Chroma with the unique ID
            store_embedding_in_chroma(collection, unique_id, embedding, file_name)

            # Return the document ID (which is the unique UUID)
            return unique_id  # This is the unique document ID that you can use in other functions
        else:
            raise Exception("Failed to generate embedding from Ollama.")
    except Exception as e:
        print(f"Error generating embedding with Ollama: {e}")
        return None
