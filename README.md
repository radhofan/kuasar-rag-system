
# Retrieval-Augmented Generation (RAG) System with FastAPI, LangChain, and Ollama

This project implements a **Retrieval-Augmented Generation (RAG)** system using Python, FastAPI, LangChain, Ollama, and a vector store (e.g., Chroma or FAISS). The system allows users to upload documents, generate embeddings, and query the system for answers with source citations. The entire setup is containerized using Docker for easy deployment.

## System Architecture

The system consists of the following components:

1. **FastAPI**: Provides the API layer for document upload and querying.
2. **Ollama**: Hosts the local LLM (Llama-3) for generating responses.
3. **ChromaDB**: Stores document embeddings for current and future use.
4. **Docker**: Containerizes the entire setup for simplified deployment.

### Core Logic

1. **Question Answering**:
    - The main API call is at the `/question` endpoint.
    - The `/question` endpoint accepts:
      - Both a question and a document file (either Markdown or PDF) simultaneously.
      - Alternatively, either the question or document file.
    - The system returns an error if no input (question or document) is supplied.

2. **Text Extraction**:
    - Text is extracted manually from documents using Python libraries.
    - Unnecessary content, such as HTML tags, is cleaned.
    - The cleaned text is then stored in ChromaDB as embeddings for current and future use.

3. **Cosine Similarity**:
    - When a question is asked, the system retrieves relevant documents based on the question.
    - Both the document and question are embedded using [nomic-embed-test] from Ollama.
    - The embeddings are compared using the **Cosine Similarity** metric to determine relevance.
    - Three potential outcomes:
      1. **[similarity > 0.1]**: Documentation exists in ChromaDB and an answer is found in the documentation.
      2. **[similarity > 0.05]**: Documentation exists in ChromaDB but no answer is found.
      3. **[else]**: Documentation does not exist in ChromaDB.

## Setup Instructions

### Prerequisites

Before setting up the system, ensure you have the following installed:

- Docker
- Docker Compose
- Python 3.10+

### Step 1: Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/yourusername/rag-system.git
cd rag-system
```

## Step 2: Build the Docker Container
```bash
docker compose build
```

### Step 3: Run the Docker Container
```bash
docker compose up -d
```

### Step 4: Test Query Using Pytest
The pytest file has two custom parameters which is --file and --question, --file is the path of your file from the root directory, all files are located in either samples/md (for markdown) or samples/pdf (for pdf). Sample files are already given.
```bash
pytest tests/test_question.py --file=[filepath] --question=[your question] -s
```
Test example:
```bash
pytest tests/test_question.py --file=samples/md/FASTAPI_README.md --question="What is FastAPI" -s
```



