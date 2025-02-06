
# Retrieval-Augmented Generation (RAG) System with FastAPI, and Ollama

This project implements a **Retrieval-Augmented Generation (RAG)** system using Python, FastAPI, Ollama, and ChromaDB. The system allows users to upload documents, generate embeddings, and query the system for answers with source citations. The entire setup is containerized using Docker for easy deployment.

## System Architecture

The system consists of the following components:

1. **FastAPI**: Provides the API layer for document upload and querying.
2. **Ollama**: Hosts the local LLM (Llama-3) for generating responses.
3. **ChromaDB**: Stores document embeddings for current and future use.
4. **Docker**: Containerizes the FastAPI and Ollama for setup and deployment.

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
    - Both the document and question are embedded using `nomic-embed-test` from Ollama.
    - The embeddings are compared using the **Cosine Similarity** metric to determine relevance.
    - Three potential outcomes:
      1. **[similarity > 0.1]**: Documentation exists in ChromaDB and an answer is found in the documentation.
      2. **[similarity > 0.05]**: Documentation exists in ChromaDB but no answer is found.
      3. **[else]**: Documentation does not exist in ChromaDB.
    - The `llama3` model from Ollama will be used for prompting.
    - A custom calculation will be used for token usage.

4. **Logging**:
    - Logging will be done via the `/logs` endpoint, it will return success/failure rates, requests       count, average response time and token usage.

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

### Step 2: Build the Docker Container
```bash
docker compose build
```

### Step 3: Run the Docker Container
```bash
docker compose up -d
```

### Step 4: Test Query Using Pytest
The pytest file has two custom parameters which is `--file` and `--question`, `--file` is the path of your file from the root directory, all files are located in either samples/md (for markdown) or samples/pdf (for pdf). Sample files are already given.
```bash
pytest tests/test_question.py --file=[filepath] --question=[your question] -s
```
Test example:
```bash
pytest tests/test_question.py --file=samples/md/FASTAPI_README.md --question="What is FastAPI" -s
```
### API Monitoring
```bash
pytest tests/logs.py -s
```
## Ideas for Future Improvements

### **1. Better LLM Model for Faster Prompting**  
A better LLM model for faster response times would be **GPT-3.5 Turbo**, **GPT 4**, or any other fast and quick LLM models to provide lower latency and better efficiency compared to outdated models like **llama3**, making it ideal for real-time applications.  

### **2. Dedicated Logging/Statistics Library for API Model**  
For monitoring API performance, **Prometheus with Grafana** would be a suitable choice. Prometheus collects real-time metrics such as response time, request counts, and error rates, while Grafana provides an interactive dashboard for visualization and analysis. This combination helps in identifying bottlenecks and optimizing system performance.  

### **3. Improved Algorithm to Determine Question-Document Similarity**  
To enhance the accuracy of question-document similarity, **SBERT (Sentence-BERT)** can be used instead of traditional cosine similarity. SBERT generates more meaningful and context-aware embeddings, leading to improved retrieval precision and better matching between questions and relevant documents.

