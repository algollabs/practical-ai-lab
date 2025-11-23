import os
from llama_index.core.tools import FunctionTool

# --- Tool Implementation Functions ---

def read_file(file_path: str) -> str:
    """
    Reads the content of a file from the filesystem.
    Useful for reading context, previous plans, or guidelines.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        with open(file_path, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def save_plan(file_path: str, content: str) -> str:
    """
    Saves the given content (text) to a file.
    Use this to save the final OKR plan or draft.
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully saved content to '{file_path}'."
    except Exception as e:
        return f"Error saving file: {str(e)}"

def get_okr_guidelines() -> str:
    """
    Returns the official guidelines for writing OKRs (Objectives and Key Results).
    Always consult this before drafting a plan.
    """
    return """
    # OKR Guidelines (Practical AI Corp)
    
    1. **Objective**: What do you want to achieve? (Qualitative, Inspirational, Time-bound)
    2. **Key Results**: How will we know we've achieved it? (Quantitative, Measurable, 3-5 per Objective)
    
    **Best Practices:**
    - KRs should be outcomes, not tasks.
    - Avoid binary KRs (Done/Not Done) where possible.
    - Stretch goals are encouraged (expect 70% completion).
    
    **Format Example:**
    **Objective:** Improve the reliability of the payment processing system.
    **KR 1:** Reduce 5xx error rate from 1% to 0.1%.
    **KR 2:** Increase unit test coverage from 60% to 85%.
    """

# --- LlamaIndex Tool Definitions ---
# We wrap the python functions in FunctionTool so the LLM can understand them.

read_file_tool = FunctionTool.from_defaults(
    fn=read_file,
    name="read_file",
    description="Read the content of a file. Input: file_path."
)

save_plan_tool = FunctionTool.from_defaults(
    fn=save_plan,
    name="save_plan",
    description="Save text content to a file. Inputs: file_path, content."
)

okr_guidelines_tool = FunctionTool.from_defaults(
    fn=get_okr_guidelines,
    name="get_okr_guidelines",
    description="Get the official guidelines for writing OKRs."
)

ALL_TOOLS = [read_file_tool, save_plan_tool, okr_guidelines_tool]

