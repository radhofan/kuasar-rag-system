# RAG System with FastAPI, LangChain, and Ollama

This project implements a Retrieval-Augmented Generation (RAG) system using Python, FastAPI, LangChain, Ollama, and a vector store (e.g., Chroma or FAISS). The system allows users to upload documents, generate embeddings, and query the system for answers with source citations. The entire setup is containerized using Docker.

## System Architecture

The system consists of the following components:

1. **FastAPI**: Serves as the API layer for document upload and querying.
2. **Ollama**: Deploys the local LLM (Llama-3) for generating responses.
3. **ChromaDB**: Stores document embeddings automatically.
4. **Docker**: Containerizes the entire setup for easy deployment.

Core Logic:
1. **Question Answering**: Main Api call will be at [/question] endpoint which is handled by FastAPI, the [/question] accepts both question and documentation file (either md or pdf) simulteanously, alternatively it accepts only either one of them but returns error when nothing is being supplied to this endpoint.
2. **Text extraction**: Text extraction will be handled manually using python libraries to clean unnecessary contents such as html syntax etc. The cleaned text will be then stored into ChromaDB as embedding for current/future use.
3. **Cosine Similarity**: When a question is being asked, the system will retrieve the current or similar docs based on the question and embed them using [nomic-embed-test] from ollama, both of those embedding will be compared using the Cosine Similarity Test to ensure that the answer exists. Three different answer cases will appear here: 
                          1. [similarity > 0.1] documentation exist in ChromaDB and answer exist in the documentation
                          2. [similarity > 0.05] documentation exist in ChromaDB but answer isn't found there
                          3. [else] documentation does not exist in ChromaDB

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.10+

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/rag-system.git
cd rag-system
```
### Step 2: Build the Docker Container
```bash
git clone https://github.com/yourusername/rag-system.git
cd rag-system
```
### Step 3: Run the Docker Container
```bash
git clone https://github.com/yourusername/rag-system.git
cd rag-system
```
### Step 4: Test Query Using Pytest
```bash
git clone https://github.com/yourusername/rag-system.git
cd rag-system
```


