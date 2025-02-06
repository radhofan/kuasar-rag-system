# RAG System with FastAPI, LangChain, and Ollama

This project implements a Retrieval-Augmented Generation (RAG) system using Python, FastAPI, LangChain, Ollama, and a vector store (e.g., Chroma or FAISS). The system allows users to upload documents, generate embeddings, and query the system for answers with source citations. The entire setup is containerized using Docker.

## System Architecture

The system consists of the following components:

1. **FastAPI**: Serves as the API layer for document upload and querying.
2. **LangChain**: Handles the RAG implementation, including document ingestion, embedding generation, and query processing.
3. **Ollama**: Deploys the local LLM (Llama-3.2) for generating responses.
4. **Vector Store**: Stores document embeddings (e.g., Chroma or FAISS).
5. **Docker**: Containerizes the entire setup for easy deployment.

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


