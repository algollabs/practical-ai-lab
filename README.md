# Algol Lab's Practical AI 🧪

A comprehensive, hands-on workshop designed to teach mid-to-senior engineers the fundamentals of building AI applications using **LlamaIndex**, **Qdrant**, and **Python**.

Built with ❤️ for the tech community by Zaid Amireh.


## Workshop Content

This repository contains two main labs:

1.  **Lab 1: Company Policy Assistant (RAG)**
    *   Build a Retrieval-Augmented Generation system to query internal PDF policies.
    *   **Stack:** LlamaIndex, Qdrant, Gradio.
    *   **Key Concepts:** Data Ingestion, Vector Stores, Chunking, Citations.
    *   [Go to Lab 1 Guide](docs/LAB1_RAG.md)

2.  **Lab 2: Performance Review Assistant (ReAct Agents)**
    *   Build an Agent that can read files, reason about goals, and write OKR plans.
    *   **Stack:** LlamaIndex (Agent), Rich (CLI).
    *   **Key Concepts:** Tool Use, ReAct Loop (Reason -> Act -> Observe), Function Calling.
    *   [Go to Lab 2 Guide](docs/LAB2_AGENTS.md)

## Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)
- Docker (for Qdrant)

### Setup

1.  **Clone the repo**
    ```bash
    git clone <repo-url>
    cd practical-ai-lab
    ```

2.  **Install Dependencies**
    ```bash
    uv sync
    ```

3.  **Environment Setup**
    ```bash
    cp .env.example .env
    # Edit .env and add your OPENAI_API_KEY
    ```

4.  **Start Vector DB**
    ```bash
    docker-compose up -d
    ```

### Running the Labs

**Run Lab 1 (RAG UI):**
```bash
uv run python -m lab1_rag.app
```
*Access at http://localhost:7860*

**Run Lab 2 (Agent CLI):**
```bash
uv run python -m lab2_agents.cli
```

## Documentation
See the `docs/` folder for detailed guides on theory and implementation details.

