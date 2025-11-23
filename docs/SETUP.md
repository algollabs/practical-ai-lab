# Setup Guide 🛠️

Welcome to the Practical AI Lab! This guide will help you set up your development environment to run the workshops.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

1.  **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
2.  **Docker Desktop**: Required for running the Vector Database (Qdrant). [Download Docker](https://www.docker.com/products/docker-desktop/)
3.  **uv**: A blazing fast Python package manager. [Install uv](https://github.com/astral-sh/uv)

    ```bash
    # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/algollabs/practical-ai-lab.git
cd practical-ai-lab
```

### 2. Install Dependencies

We use `uv` to manage dependencies. It will create a virtual environment and install all required packages.

```bash
uv sync
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` in your editor and configure your LLM provider.

**Option A: OpenAI (Recommended for stability)**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...  # Your OpenAI API Key
OPENAI_MODEL=gpt-4-turbo    # or gpt-3.5-turbo
```

**Option B: Ollama (Local)**
Ensure you have [Ollama](https://ollama.com/) running locally with a model pulled (e.g., `ollama pull llama3`).
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

### 4. Start Infrastructure

We use Docker to run Qdrant, our Vector Database.

```bash
docker-compose up -d
```

Verify that Qdrant is running by visiting: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## Verification

To verify everything is set up correctly, run the text generation test script (if available) or try running Lab 1:

```bash
uv run python -m lab1_rag.app
```

If you see a URL like `Running on local URL:  http://0.0.0.0:7860`, you are good to go! Press `Ctrl+C` to stop it.

## Troubleshooting

-   **Docker connection refused**: Ensure Docker Desktop is running.
-   **Missing API Key**: Double-check your `.env` file.
-   **uv not found**: Restart your terminal after installing uv.

