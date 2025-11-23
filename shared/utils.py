import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.openai import OpenAIEmbedding
# Note: For local embeddings with Ollama, we might typically use HuggingFaceEmbedding, 
# but for this workshop we'll stick to OpenAI embeddings or a simple placeholder if strictly local is requested.
# To keep it simple and robust for the "Zero-Magic" philosophy, we will default to OpenAI embeddings 
# unless explicitly changed, but we'll leave room for extension.

def init_settings():
    """
    Initializes LlamaIndex Settings based on environment variables.
    
    This function demonstrates the "Framework First" and "Model Agnostic" philosophy.
    By setting `Settings.llm` and `Settings.embed_model` globally, all subsequent
    LlamaIndex operations (Index creation, Query Engine, etc.) will automatically
    use these configured models without needing to pass them explicitly.
    """
    load_dotenv()
    
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    # --- LLM Configuration ---
    if llm_provider == "openai":
        # Zero-Magic: Explicitly setting the model and api_key ensures clarity.
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")
            
        print(f"Initializing Settings with OpenAI LLM: {model}")
        Settings.llm = OpenAI(model=model, api_key=api_key)
        
        # For OpenAI, we also use their embeddings by default
        print("Initializing Settings with OpenAI Embeddings")
        Settings.embed_model = OpenAIEmbedding(api_key=api_key)

    elif llm_provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3")
        
        print(f"Initializing Settings with Ollama LLM: {model} ({base_url})")
        Settings.llm = Ollama(
            model=model, 
            base_url=base_url,
            request_timeout=120.0 # Longer timeout for local inference
        )
        
        # For a purely local setup, we would ideally use HuggingFaceEmbedding.
        # However, to avoid adding heavy torch dependencies just for this step if not needed,
        # we will warn the user. For now, we assume OpenAI embeddings are acceptable even with Ollama 
        # (Hybrid) OR the user must install `llama-index-embeddings-huggingface` and configure it here.
        # For this workshop's simplicity, we'll default to OpenAI embeddings if available, or raise an error.
        if os.getenv("OPENAI_API_KEY"):
             print("Using OpenAI Embeddings with Ollama (Hybrid Mode)")
             Settings.embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            # Educational note: This is where we'd plug in a local embedding model.
            print("WARNING: No OpenAI API key found for embeddings. Using LlamaIndex default (Mock/OpenAI) which may fail.")
            # In a real local-only setup:
            # from llama_index.embeddings.huggingface import HuggingFaceEmbedding
            # Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
            
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {llm_provider}")

    return Settings

