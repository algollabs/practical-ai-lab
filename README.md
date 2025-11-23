# Algol Lab's Practical AI 🧪

A comprehensive, hands-on workshop designed to teach mid-to-senior engineers the fundamentals of building AI applications.

**Theme:** "Practical AI Corp" — You will build internal tools for HR policies (RAG) and performance evaluations (Agents).

## 📚 Workshop Content

### Lab 1: Company Policy Assistant (RAG)
Build a Retrieval-Augmented Generation system to query internal PDF policies.
- **Key Concepts:** Data Ingestion, Vector Stores (Qdrant), Chunking strategies, Citation handling.
- **Stack:** LlamaIndex, Qdrant, Gradio.
- [**Start Lab 1**](docs/LAB1_RAG.md)

### Lab 2: Performance Review Assistant (ReAct Agents)
Build an Agent that can read files, reason about goals, and act on them.
- **Key Concepts:** The ReAct Loop (Reason -> Act -> Observe), Tool use, Function Calling.
- **Stack:** LlamaIndex (Agent), Rich (CLI).
- [**Start Lab 2**](docs/LAB2_AGENTS.md)

## 📖 Documentation

We believe in understanding *why*, not just *how*.

- [**Core Theory**](docs/THEORY.md): Deep dive into LLMs, Embeddings, RAG, and Agents.
- [**Setup Guide**](docs/SETUP.md): Detailed installation instructions (Python, Docker, uv).
- [**Lab 1 Guide**](docs/LAB1_RAG.md): RAG implementation details.
- [**Lab 2 Guide**](docs/LAB2_AGENTS.md): Agent implementation details.

## ⚡ Quick Start

For detailed prerequisites and troubleshooting, see the [Setup Guide](docs/SETUP.md).

1.  **Clone & Install**
    ```bash
    git clone https://github.com/algollabs/practical-ai-lab.git
    cd practical-ai-lab
    uv sync
    ```

2.  **Configure**
    ```bash
    cp .env.example .env
    # Add your OpenAI API Key in .env
    ```

3.  **Run Infrastructure**
    ```bash
    docker-compose up -d
    ```

4.  **Run Labs**
    ```bash
    # Lab 1 (RAG UI)
    uv run python -m lab1_rag.app

    # Lab 2 (Agent CLI)
    uv run python -m lab2_agents.cli
    ```

---
Built with ❤️ by Zaid Amireh for the tech community.
