## Project Overview

**Memories Agent** is a local-first AI assistant that combines Retrieval-Augmented Generation (RAG), long-term memory, local LLM inference, document understanding, and observability.

The system allows users to chat with an AI assistant, upload documents, retrieve relevant knowledge from local vector storage, automatically extract long-term memories from conversations, and monitor system behavior such as latency, retrieved chunks, memory usage, and request status.

The project is designed as a portfolio-ready AI Engineering system, focusing on practical components commonly used in real-world AI applications:

- Local LLM inference with Ollama
- Document ingestion and chunking
- Local embedding generation
- Vector search with ChromaDB
- Semantic long-term memory retrieval
- FastAPI backend
- Streamlit frontend
- SQLite-based metadata storage
- Observability dashboard for request tracking

## High-level Architecture

```mermaid
flowchart LR
    User[User] --> Frontend[Streamlit Frontend]

    Frontend --> ChatAPI[FastAPI Chat API]
    Frontend --> DocumentAPI[FastAPI Document API]
    Frontend --> MemoryAPI[FastAPI Memory API]
    Frontend --> LogsAPI[FastAPI Logs API]

    ChatAPI --> LLM[Ollama Local LLM]
    ChatAPI --> RAG[RAG Service]
    ChatAPI --> MemoryService[Memory Service]
    ChatAPI --> Logger[Observability Service]

    DocumentAPI --> FileLoader[File Loader]
    DocumentAPI --> Chunking[Chunking Service]
    DocumentAPI --> Embedding[Embedding Service]
    DocumentAPI --> VectorDB[ChromaDB Vector Store]

    RAG --> Embedding
    RAG --> VectorDB

    MemoryService --> SQLite[(SQLite Database)]
    MemoryService --> Embedding

    Logger --> SQLite
    DocumentAPI --> SQLite
    ChatAPI --> SQLite

    LLM --> ChatAPI
    ChatAPI --> Frontend
