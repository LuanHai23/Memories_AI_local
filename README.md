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


## Chat and Long-term Memory Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Streamlit Frontend
    participant API as FastAPI Chat API
    participant MEM as Memory Service
    participant RAG as RAG Service
    participant VDB as ChromaDB
    participant DB as SQLite
    participant LLM as Ollama LLM

    U->>FE: Send message
    FE->>API: POST /chat

    API->>DB: Save user message

    API->>MEM: Extract useful long-term memories
    MEM->>LLM: Ask LLM to identify durable user facts
    LLM-->>MEM: Return structured memory JSON
    MEM->>DB: Save extracted memories

    API->>MEM: Retrieve relevant memories
    MEM->>MEM: Embed user question
    MEM->>DB: Load active memories
    MEM->>MEM: Compute semantic similarity
    MEM-->>API: Return relevant memories

    API->>RAG: Search document context
    RAG->>VDB: Semantic search document chunks
    VDB-->>RAG: Return top matching chunks
    RAG-->>API: Return filtered contexts

    API->>LLM: Build prompt with user question + memories + document context
    LLM-->>API: Generate final answer

    API->>DB: Save assistant response and request log
    API-->>FE: Return answer, memories used, contexts, latency
    FE-->>U: Display assistant response
