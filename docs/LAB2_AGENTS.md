# Lab 2: Performance Review Assistant (ReAct Agents) 🕵️

**Goal**: Build an AI Agent that can reason about tasks, read files, and write OKR plans.

## Overview

In this lab, we move beyond simple Q&A. We build an Agent that can **do** things. The Agent helps managers write OKRs (Objectives and Key Results) by providing tools to read context and save the final plan.

## The ReAct Loop Implementation

We explicitly implement the "Reason -> Act -> Observe" loop in `lab2_agents/agent.py` instead of hiding it behind a framework one-liner. This is for educational clarity.

### The Class: `ManualReActAgent`

1.  **`chat_with_tools`**: We use the LLM's ability to decide *if* a tool is needed.
2.  **The Loop**:
    *   **While Loop**: We allow up to 10 steps to prevent infinite loops.
    *   **Check Tool Calls**: If the LLM returns `tool_calls`, we pause generation.
    *   **Execution**: We find the matching python function in `self.tools`.
    *   **Observation**: We append a `ChatMessage` with `role=MessageRole.TOOL` containing the output.
    *   **Resume**: The loop continues, sending the tool output back to the LLM.

### Tools (`tools.py`)

We define standard Python functions and wrap them with `FunctionTool`.

*   `read_file(path)`: Safely reads a text file.
*   `save_plan(path, content)`: Writes the generated plan to disk.
*   `get_okr_guidelines()`: Returns a static string of best practices. This simulates fetching data from a knowledge base.

### CLI Interface (`cli.py`)

We use `rich` and `typer` to build a pretty CLI.

*   **Color Coding**:
    *   🔵 **Blue**: Agent Thoughts (Reasoning).
    *   🟡 **Yellow**: Tool Actions (Calling functions).
    *   🟢 **Green**: Final Answer or success.

## How to Run

1.  **Run the CLI**:
    ```bash
    uv run python -m lab2_agents.cli
    ```

2.  **Interact**:
    *   Type: *"Create a performance plan for a Senior Engineer."*
    *   Watch the Agent "Think", check the guidelines, and ask you for more info or draft a plan.

## Example Scenario

**User**: *"Draft OKRs for the new mobile app launch and save it to `plans/mobile_launch.md`."*

**Agent Flow**:
1.  **Thought**: "I need to draft OKRs. First I should check the guidelines."
2.  **Action**: Calls `get_okr_guidelines()`.
3.  **Observation**: Receives formatting rules.
4.  **Thought**: "Now I will draft the plan following these rules..."
5.  **Action**: Calls `save_plan("plans/mobile_launch.md", "Objective: ...")`.
6.  **Final Answer**: "I have saved the plan to `plans/mobile_launch.md`."

## Experimentation Ideas

*   **Add a Tool**: Create a `send_email(to, body)` tool in `tools.py` (just print the email) and add it to `ALL_TOOLS`. Ask the agent to email the plan.
*   **Break the Loop**: Ask a question that requires a tool that doesn't exist. How does the agent react?

