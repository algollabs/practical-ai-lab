import gradio as gr
from lab1_rag.pipeline import get_query_engine

# Initialize the query engine once at startup
print("Initializing Query Engine...")
query_engine = get_query_engine()

def format_sources(response):
    """
    Extracts and formats source nodes from the LlamaIndex response object.
    """
    sources = []
    for node in response.source_nodes:
        # Metadata contains file_name, page_label, etc.
        file_name = node.metadata.get("file_name", "Unknown File")
        score = f"{node.score:.4f}" if node.score else "N/A"
        text_snippet = node.node.get_content()[:200] + "..."
        
        source_html = f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
            <div style="font-weight: bold; color: #2b3137;">📄 {file_name} <span style="font-size: 0.8em; color: #666;">(Score: {score})</span></div>
            <div style="font-size: 0.9em; margin-top: 5px; color: #444;">"{text_snippet}"</div>
        </div>
        """
        sources.append(source_html)
    
    if not sources:
        return "No specific sources used."
    
    return "\n".join(sources)

def chat_response(message, history):
    """
    Gradio chat function.
    Args:
        message: The user's input string.
        history: Chat history (unused here as LlamaIndex engine maintains its own context if configured, 
                 but for simple QueryEngine we might treat each query independently or upgrade to ChatEngine).
    """
    # Query the RAG engine
    response = query_engine.query(message)
    
    # Extract answer text
    answer = str(response)
    
    # Extract sources
    sources_html = format_sources(response)
    
    # Gradio ChatInterface expects just the message, but we want to update the sidebar too.
    # Since ChatInterface is restrictive, we'll use a custom Blocks layout to update multiple outputs.
    return answer, sources_html

# Build Custom UI Layout
with gr.Blocks(title="Practical AI Lab: Policy Assistant", theme=gr.themes.Soft(), analytics_enabled=False) as demo:
    gr.Markdown("# 🏢 Practical AI Corp: Policy Assistant")
    gr.Markdown("Ask questions about company policies (WFH, Expenses, Security).")
    
    with gr.Row():
        # Left Column: Chat
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500, type="messages", allow_tags=False)
            msg = gr.Textbox(placeholder="How much is the travel meal allowance?", label="Your Question")
            clear = gr.Button("Clear Conversation")
            
            # Example Queries
            gr.Markdown("### 💡 Try these examples")
            examples = gr.Examples(
                examples=[
                    # Working queries
                    ["What is the reimbursement limit for team dinners?"],
                    ["Can I use a personal device for work?"],
                    ["How many days a week must I be in the office?"],
                    # Queries likely to fail (out of domain)
                    ["What is the company's stock price?"],
                    ["How do I reset the coffee machine?"],
                ],
                inputs=msg
            )

        # Right Column: Citations
        with gr.Column(scale=1):
            gr.Markdown("### 📚 Retrieved Context")
            sources_box = gr.HTML(value="<em>Sources will appear here...</em>")

    def user_message(user_input, history):
        return "", history + [{"role": "user", "content": user_input}]

    def bot_response(history):
        user_input = history[-1]["content"]
        answer, sources = chat_response(user_input, history[:-1])
        history.append({"role": "assistant", "content": answer})
        return history, sources

    # Event Wiring
    msg.submit(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, [chatbot], [chatbot, sources_box]
    )
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    # Launch the app
    # server_name="0.0.0.0" allows access from outside the container if dockerized
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
