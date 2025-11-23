# Specifications: Practical AI Lab

## 1. Project Overview
**Name:** `practical-ai-lab`
**Description:** A comprehensive, open-source, hands-on workshop designed to teach mid-to-senior engineers the fundamentals of building AI applications. The workshop covers RAG (Retrieval-Augmented Generation) and ReAct (Reasoning + Acting) Agents using modern Python tooling.
**Theme:** "Practical AI Corp" - A fictional corporate environment where participants build internal tools for HR policies and performance evaluations.

## 2. Design Philosophy & Goals
-   **Educational Focus:** Code is written to be read and understood. Priority on clarity over brevity.
-   **Framework First:** Utilize LlamaIndex as the primary abstraction layer for LLM interactions to ensure model agnosticism (supporting OpenAI, Anthropic, Ollama/Local).
-   **Hands-on:** Participants build working software, not just run notebooks.
-   **Zero-Magic:** While using frameworks, we explicitly explain *what* is happening under the hood (e.g., inspecting retrieval nodes, visualizing agent thought processes).

## 3. Technical Stack

### Core Dependencies
-   **Language:** Python 3.11+
-   **Environment Manager:** `uv`
-   **Orchestration Framework:** `llama-index` (Core, LLMS, Embeddings)
-   **Vector Database:** `qdrant-client` (Dockerized Qdrant instance)
-   **Interface:** `gradio` (Web UI for Lab 1), `rich` or `typer` (CLI for Lab 2)
-   **Utilities:** `python-dotenv`, `pydantic`

### Inference Layer (Critical Change)
-   **Primary:** OpenAI (GPT-4o or GPT-4-Turbo)
-   **Local/Alternative:** Ollama (Llama 3, Mistral)
-   **Implementation:** All LLM calls must use LlamaIndex `LLM` abstractions (`Settings.llm`). **Do not use the raw `openai` client directly**, to ensure easy swapping of backends.

## 4. Repository Structure

```text
practical-ai-lab/
├── docs/                  # Workshop guides and theory
│   ├── LAB1_RAG.md
│   ├── LAB2_AGENTS.md
│   ├── SETUP.md
│   └── THEORY.md
├── lab1_rag/             # RAG Workshop
│   ├── app.py            # Gradio Interface
│   ├── pipeline.py       # Core RAG Logic
│   └── data/             # PDF Documents
├── lab2_agents/          # Agents Workshop
│   ├── agent.py          # Agent Implementation
│   ├── tools.py          # Function Definitions
│   └── cli.py            # CLI Interaction
├── shared/               # Shared utilities (optional)
│   └── utils.py
├── .env.example          # Config template
├── docker-compose.yml    # Qdrant setup
├── pyproject.toml        # Dependencies
└── README.md             # Entry point
```

## 5. Lab Specifications

### Lab 1: Company Policy Assistant (RAG)
**Goal:** Build a system to query internal PDF documents.

**Components:**
1.  **Data Ingestion:**
    -   Load generic PDF policies (e.g., "Remote Work Policy", "Code of Conduct") using `SimpleDirectoryReader`.
    -   Implement chunking strategy using LlamaIndex `TokenTextSplitter` or `SentenceSplitter`.
2.  **Vector Store:**
    -   Initialize `QdrantVectorStore`.
    -   Create a `VectorStoreIndex` from documents.
    -   **Feature:** Implement "Smart Loading" (check if collection exists before re-ingesting).
3.  **Retrieval & Query:**
    -   Build a Query Engine with `retriever_mode="embedding"`.
    -   Return source nodes to display citations.
4.  **Interface (Gradio):**
    -   Simple Chat Interface.
    -   Sidebar to show retrieved context/citations for the last answer.
    -   "Reload Knowledge Base" button.

**Refactoring Note:** Ensure the `Settings.embed_model` and `Settings.llm` are strictly used.

### Lab 2: Performance Review Assistant (ReAct Agent)
**Goal:** Build an agent that helps managers draft OKRs (Objectives and Key Results).

**Components:**
1.  **Tools (Function Calling):**
    -   `read_file(path)`: Read context.
    -   `save_plan(path, content)`: Write the final OKR plan.
    -   `get_okr_guidelines()`: A simple tool returning a string of best practices.
2.  **Agent Logic:**
    -   Implement a **ReAct Loop**.
    -   *Option A (Hard Mode):* Manually implement the loop (Reason -> Act -> Observe) using `llm.chat()` or `llm.predict()` to teach the concept, parsing tool calls manually or using LlamaIndex's lower-level tool calling API.
    -   *Option B (Framework Mode):* Use LlamaIndex's `ReActAgent` factory.
    -   *Selection:* Use **Option A (Manual Loop with LlamaIndex Abstractions)** for the educational value of seeing the loop, but use `llm.chat_with_tools` if available or standard `chat` to show how the model interacts.
    -   **Crucial:** The LLM must be instantiated via `llama-index` so it works with Ollama.
3.  **CLI Interface:**
    -   Interactive session.
    -   **Verbose Mode:** Stream the agent's "Thought", "Action", and "Observation" steps clearly to the console using specific colors (e.g., Blue for thoughts, Yellow for tools, Green for results).

## 6. Content & Assets

### Sample Data (Lab 1)
-   Generate 3-5 fictitious "Practical AI Corp" policy PDFs.
    -   *Policy 01: Work from Home* (Contains specific rules about days/hours).
    -   *Policy 02: Expense Reimbursement* (Contains limits and categories).
    -   *Policy 03: IT Security* (Password rotations, 2FA).

### Sample Scenarios (Lab 2)
-   A markdown file `SCENARIOS.md` with prompts like:
    -   "Create OKRs for a Senior Backend Engineer focusing on system reliability."
    -   "Draft a plan to improve the hiring pipeline speed by 20%."

## 7. Configuration & Environment

**Environment Variables (`.env`):**
```env
# LLM Provider (openai | ollama)
LLM_PROVIDER=openai

# OpenAI Config
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo

# Ollama Config (Optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Vector DB
QDRANT_URL=http://localhost:6333
```

**Initialization:**
-   A `settings.py` or `config.py` should handle the logic of initializing `Settings.llm` and `Settings.embed_model` based on `LLM_PROVIDER`. This centralizes the switch logic.

## 8. Documentation Requirements
-   **Setup Guide:** Clear instructions for installing `uv`, Docker, and (optionally) Ollama.
-   **Inline Comments:** Every major block of code (Retrieval, Loop, Tool definition) must have a comment explaining *why* we are doing this.
-   **"Try This" Sections:** In the lab guides, include small experiments (e.g., "Change the chunk size to 100. How does it affect the answer?").


