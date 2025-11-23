# Lab 1: Company Policy Assistant (RAG) 📚

**Goal**: Build a "Smart" Policy Assistant that can answer questions based on internal PDF documents.

## Overview

In this lab, we implement a standard RAG pipeline using LlamaIndex and Qdrant. The system allows employees to ask questions about "Work from Home", "Expenses", and "Security" policies.

## Architecture

1.  **Data**: PDFs located in `lab1_rag/data/`.
2.  **Database**: Qdrant (running via Docker).
3.  **Backend**: LlamaIndex `VectorStoreIndex`.
4.  **Frontend**: Gradio Chat Interface.

## Implementation Details

### 1. The Pipeline (`pipeline.py`)

The core logic resides in `build_or_load_index`. We implement a **"Smart Loading"** pattern:

*   **Check First**: Instead of blindly re-ingesting data every time (which costs money and time), we check Qdrant.
*   `client.get_collections()`: We see if `practical_ai_policies` exists.
*   **If Exists**: We use `VectorStoreIndex.from_vector_store(...)`. This loads the index metadata without re-reading PDFs.
*   **If New**: We use `VectorStoreIndex.from_documents(...)`. This triggers:
    *   Text Splitting (`SentenceSplitter` with 1024 chunk size).
    *   Embedding Generation (OpenAI/Ollama).
    *   Upsertion into Qdrant.

### 2. Citations

We want to show *where* the answer came from.

*   `query_engine.query(message)` returns a `Response` object.
*   `response.source_nodes` contains the chunks used for the answer.
*   In `app.py`, `format_sources` iterates through these nodes to display the **filename**, **relevance score**, and a **text snippet** in the UI sidebar.

## How to Run

1.  **Start Qdrant**:
    ```bash
    docker-compose up -d
    ```

2.  **Run the App**:
    ```bash
    uv run python -m lab1_rag.app
    ```

3.  **Access UI**: Open [http://localhost:7860](http://localhost:7860).

## Experimentation Ideas

*   **Change Chunk Size**: In `pipeline.py`, change `chunk_size` in `SentenceSplitter` to `256`. Re-run. Does the retrieval get more specific or lose context?
*   **New Policy**: Add a dummy PDF to `lab1_rag/data/` and restart. Does the bot know about it? (Note: You might need to delete the collection in Qdrant or change `COLLECTION_NAME` to force re-ingestion).

