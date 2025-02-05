import chromadb

def clear_chroma():
    client = chromadb.PersistentClient(path="../app/data/chromadb")
    
    try:
        collection = client.get_collection("embeddings")
        all_items = collection.get()
        ids = all_items["ids"]  
        
        if ids:
            collection.delete(ids=ids)  
            print("Embeddings collection cleared (but not deleted).")
        else:
            print("Collection is already empty.")
    
    except chromadb.errors.InvalidCollectionException:
        print("Collection 'embeddings' does not exist.")

if __name__ == "__main__":
    clear_chroma()
