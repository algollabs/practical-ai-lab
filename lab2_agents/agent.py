import json
from typing import List, Optional
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.tools import BaseTool
from llama_index.core.agent import ReActAgent
from shared.utils import init_settings

# Initialize settings to ensure LLM is ready
init_settings()

class ManualReActAgent:
    """
    A Manual implementation of the ReAct (Reasoning + Acting) Loop.
    
    Educational Purpose:
    Instead of using `ReActAgent.from_tools()` which hides the loop, 
    we implement the "Think -> Act -> Observe" cycle explicitly.
    
    We use LlamaIndex's `llm.chat_with_tools` (if available) or standard `llm.chat` 
    to handle the heavy lifting of tool selection, but we control the execution flow.
    """
    def __init__(self, tools: List[BaseTool], system_prompt: str = ""):
        self.tools = {t.metadata.name: t for t in tools}
        self.tools_list = tools
        from llama_index.core import Settings
        self.llm = Settings.llm
        self.system_prompt = system_prompt
        self.chat_history: List[ChatMessage] = [
            ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)
        ]

    def chat(self, user_input: str, verbose: bool = True) -> str:
        """
        Executes the ReAct Loop for a single user turn.
        """
        # 1. Add user message to history
        self.chat_history.append(ChatMessage(role=MessageRole.USER, content=user_input))
        
        # 2. Start the Loop (Reason -> Act -> Observe)
        max_iterations = 10
        current_iter = 0
        
        while current_iter < max_iterations:
            current_iter += 1
            
            if verbose:
                print(f"\n--- ReAct Step {current_iter} ---")
            
            # CALL LLM
            # We use chat_with_tools if the LLM supports it (OpenAI does), 
            # which gives us structured tool calls.
            # If the LLM doesn't support native tool calling (some local models), 
            # this method might fallback or fail, but for this workshop we assume 
            # a capable model (OpenAI or Tool-calling Ollama).
            try:
                response = self.llm.chat_with_tools(
                    self.tools_list, 
                    chat_history=self.chat_history,
                    verbose=False # We handle verbosity manually
                )
            except AttributeError:
                # Fallback for LLMs that don't implement chat_with_tools directly 
                # (though most LlamaIndex LLM wrappers do now).
                # In a real scenario, we'd use a ReActOutputParser here.
                # For simplicity, let's assume we are using OpenAI/compatible.
                response = self.llm.chat(self.chat_history)

            # APPEND Assistant Message to History
            # The response message contains the content (Thought) and potentially tool_calls
            message = response.message
            self.chat_history.append(message)
            
            # VISUALIZE "Thought"
            if verbose and message.content:
                print(f"🔵 THOUGHT: {message.content}")

            # CHECK for Tool Calls
            tool_calls = message.additional_kwargs.get("tool_calls", [])
            
            if not tool_calls:
                # No tools called -> Final Answer
                if verbose:
                    print(f"🟢 FINAL ANSWER: {message.content}")
                return message.content

            # ACT (Execute Tools)
            for tool_call in tool_calls:
                # Parse Function Name and Args
                # Note: OpenAI returns tool calls in a specific format handled by LlamaIndex wrappers
                # structure: tool_call.function.name, tool_call.function.arguments
                
                # LlamaIndex standardizes this in message.additional_kwargs usually, 
                # but let's rely on the abstraction if possible. 
                # Actually, `chat_with_tools` returns a response where `message.tool_calls` 
                # might be populated depending on the version.
                # Let's look at the raw additional_kwargs for OpenAI style.
                
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if verbose:
                    print(f"🟡 ACTION: Calling `{function_name}` with {function_args}")
                
                # Execute
                if function_name in self.tools:
                    tool = self.tools[function_name]
                    try:
                        # LlamaIndex tools have a .call method or we use the fn directly
                        tool_output = tool.call(**function_args)
                        tool_result_str = str(tool_output.content)
                    except Exception as e:
                        tool_result_str = f"Error executing tool: {e}"
                else:
                    tool_result_str = f"Error: Tool {function_name} not found."

                if verbose:
                    print(f"Please observe: {tool_result_str[:100]}...")

                # OBSERVE (Add Tool Output to History)
                # We must add a message with role=TOOL to the history so the LLM knows the result.
                tool_msg = ChatMessage(
                    role=MessageRole.TOOL,
                    content=tool_result_str,
                    additional_kwargs={"tool_call_id": tool_call.id}
                )
                self.chat_history.append(tool_msg)

        return "Error: Max iterations reached."

