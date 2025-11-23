# Practical AI Lab - Theory Materials 🧠

## Learning Path Overview

This theory session builds foundational understanding for the **Practical AI Lab**. Think of these concepts as building blocks—each one builds on the previous to help us construct our RAG and Agent systems.

---

## 1. What is an LLM?

### Simple Explanation
An LLM (Large Language Model) is like an extremely sophisticated autocomplete. It was trained on massive amounts of text and learned patterns about:
- How language works
- What topics are related
- How to structure responses

### How It Works (Simplified)
```
User Input: "The capital of France is"
           ↓
    [Neural Network Process]
           ↓
LLM predicts next token: "Paris"
           ↓
User sees: "The capital of France is Paris"
```

### Key Concept: Tokens
- Text is broken into small pieces called **tokens**
- ~4 characters = 1 token on average
- LLMs predict one token at a time
- Temperature controls randomness: lower = more predictable, higher = more creative

### LLM vs Traditional Programming
| | Traditional Code | LLM |
|---|---|---|
| **Logic** | Explicit rules written by developers | Learned patterns from data |
| **Output** | Deterministic (same input = same output) | Probabilistic (same input = different outputs) |
| **Strength** | Good for logic & calculation | Good for language & reasoning |
| **Limit** | Limited by programmer's knowledge | Limited by training data |

### Limitations to Remember
- **Knowledge cutoff:** Only knows what it saw during training (e.g., GPT-4 has a cutoff date).
- **Hallucinations:** Can confidently make things up.
- **No real reasoning:** Pattern matching, not true understanding.
- **No learning:** Can't remember conversations (unless you remind it via context).

---

## 2. What is Prompt Engineering?

### Definition
Prompt engineering is the art of asking LLMs questions in ways that produce better results.

### Simple Examples

**Bad Prompt:**
```
What's the best way to improve employee retention?
```
*(Generic, could answer anything)*

**Better Prompt:**
```
I'm an HR manager at a tech company with high developer turnover. 
Suggest 3 specific, low-cost initiatives we could implement this quarter 
to improve retention. Focus on remote-friendly options.
```
*(Specific context, clear constraints, defined output)*

### Key Techniques

#### 1. **System vs User Prompts**
- **System Prompt:** Sets the role/behavior (once at the start).
  ```
  You are an expert HR consultant with 20 years of experience 
  in tech companies.
  ```
- **User Prompt:** The actual question (each message).
  ```
  How can we improve time-to-hire?
  ```

#### 2. **Few-Shot vs Zero-Shot**
- **Zero-shot:** "Here's a task, do it."
  ```
  Extract the job title: "John is a Senior Engineer at Practical AI Corp"
  ```
- **Few-shot:** "Here are examples, now do it."
  ```
  Extract the job title:
  Example 1: "Jane is a Manager" → Manager
  Example 2: "Bob works as Engineer" → Engineer
  Now: "John is a Senior Engineer at Practical AI Corp" →
  ```

#### 3. **Chain of Thought**
Ask the LLM to think step-by-step:
```
"Let's think step by step:
1. First, identify the core objective
2. Then, break it into measurable components
3. Finally, set success criteria"
```

### Golden Rules
1. **Be specific:** Don't ask "tell me about AI"—ask "explain how embeddings work in RAG systems".
2. **Give context:** More context = better answers.
3. **Specify format:** "Respond as a JSON object" or "List as bullet points".
4. **Iterate:** First prompt won't be perfect, refine based on results.

---

## 3. What is an Embedding?

### Simple Explanation
An embedding is a mathematical representation of text—specifically, a list of numbers that captures meaning.

### Visual Concept
```
Text: "The manager is evaluating employee performance"
           ↓
    [Embedding Model]
           ↓
Vector: [0.2, -0.5, 0.8, 0.1, -0.3, ...]
        (e.g., 1536 numbers for OpenAI embeddings)
```

### What Do The Numbers Mean?
Don't think of them as specific meanings. Instead:
- Similar texts have **similar vectors**.
- Distance between vectors = semantic difference.
- We can measure this mathematically (Cosine Similarity).

### Similarity Example
```
Sentence 1: "The employee received a promotion"
Sentence 2: "The staff member got advanced"
Sentence 3: "The computer broke down"

Similarity(1, 2) = High (similar meaning)
Similarity(1, 3) = Low (different meaning)
```

### Why Embeddings Matter
1. **Search:** Find relevant documents by similarity.
2. **Categorization:** Group similar content.
3. **RAG:** Core to retrieval systems (Lab 1).

### Embedding Models
- **OpenAI:** `text-embedding-3-small` (efficient), `text-embedding-3-large` (more powerful).
- **Open-source:** `sentence-transformers` (free, run locally).
- **Trade-off:** Quality vs Speed vs Cost.

---

## 4. What is Chunking?

### The Problem
You have a 50-page PDF policy. You can't pass all of it to an LLM and embed it all at once. So... chunking!

### Definition
Breaking large documents into smaller, overlapping pieces that:
- Fit within token limits.
- Preserve context.
- Maintain semantic coherence.

### Chunking Strategies

#### Strategy 1: Fixed Size with Overlap
```
Document: "The Practical AI Corp policy states that employees 
get 20 days of vacation. Sick leave is separate. 
Holidays are paid..."

Chunk 1: "The Practical AI Corp policy states that employees 
get 20 days of vacation. Sick leave is separate."

Chunk 2: "Sick leave is separate. Holidays are paid..."
                    ↑ overlap ↑
```

#### Strategy 2: Smart Splitting
- Split by paragraph boundaries (preserve meaning).
- Split by sentence boundaries (more granular).
- Split by section/heading (domain-aware).

### Chunk Size Decisions
| Size | Pros | Cons |
|------|------|------|
| **Small** (100 words) | ✓ Focused, fast | ✗ Context loss |
| **Medium** (500 words) | ✓ Balance | ✓ Most common |
| **Large** (2000 words) | ✓ Full context | ✗ Expensive |

### Overlap Helps
- **Without overlap:** Information at boundaries could be missed.
- **With overlap:** Queries matching overlapping regions get both chunks.
- **Typical:** 20-30% overlap.

### In Lab 1
We use LlamaIndex's `SentenceSplitter` to handle chunking automatically (1024 tokens size, 20 overlap), ensuring we capture full policy details.

---

## 5. What is a Vector Database?

### Traditional Database vs Vector Database

**Traditional Database (e.g., PostgreSQL):**
```
SELECT * FROM users WHERE name = 'John'
        ↓
Exact match
```

**Vector Database (e.g., Qdrant):**
```
SEARCH similar_vectors TO [0.2, -0.5, 0.8, ...]
        ↓
"Find the 5 closest matches"
```

### How It Works
```
1. Store: Chunk + Embedding
   Chunk: "Company offers flexible hours"
   Embedding: [0.1, 0.3, -0.2, ...]

2. Query: "What's the flexible work policy?"
   Query Embedding: [0.11, 0.31, -0.18, ...]

3. Search: Which stored embeddings are closest?
   Similarity Score: 0.94 (Very similar!)

4. Retrieve: Return the chunk that matched
   Result: "Company offers flexible hours"
```

### Why Not Use Traditional Databases?
- Traditional DBs use exact matching (poor for semantics).
- Vector DBs use similarity (perfect for meaning).
- Vector DBs are optimized for high-dimensional data.

### In Lab 1
We use **Qdrant** (running in Docker) to store all the embeddings from our `data/` folder and enable semantic search.

---

## 6. What is RAG?

### The Problem RAG Solves

**Without RAG:**
```
User: "What is Practical AI Corp's WFH policy?"
LLM: "I don't know your specific internal policies. 
      I can tell you typical WFH policies are..."
```
*(Generic answer, not your specific policy)*

**With RAG:**
```
User: "What is Practical AI Corp's WFH policy?"
       ↓
[System retrieves: "Employees can work from home on Tuesdays and Thursdays..."]
       ↓
LLM: "According to the policy, employees can work from home on Tuesdays and Thursdays..."
```
*(Specific, accurate answer)*

### RAG = Retrieval + Augmentation + Generation

```
User Query: "What is the expense limit for team dinners?"
            ↓
    [RETRIEVE] From vector DB, find relevant policy chunks
            ↓
Retrieved: "Dinner expenses are capped at $50 per person. 
           Receipts must be uploaded within 48 hours."
            ↓
    [AUGMENT] Add retrieved chunks to the prompt
            ↓
Augmented Prompt: "Given this context: [chunks], 
                  answer: What is the expense limit?"
            ↓
    [GENERATE] LLM generates answer using context
            ↓
Answer: "The expense limit for team dinners is $50 per person."
```

### Why RAG is Powerful
1. **Up-to-date:** Uses current documents, not training data.
2. **Accurate:** Grounds answers in your actual data.
3. **Traceable:** Can show which document the answer came from (Citations).
4. **Cost-effective:** Smaller context window needed.

### In Lab 1
We build this pipeline: **Embed PDF policies → Store in Qdrant → Retrieve & Augment → Generate Answers.**

---

## 7. What is the ReAct Pattern?

### ReAct = Reasoning + Acting

### The Concept
An agent that alternates between:
1. **Reasoning:** "What should I do next?"
2. **Acting:** "Use this tool to do it."

### Example Flow
```
User: "Draft OKRs for the new mobile app launch and save it."

Step 1 (Reason):
Agent thinks: "I need to draft OKRs. First I should check the guidelines 
              to ensure I follow the company format."

Step 2 (Act):
Agent: "I'll use the 'get_okr_guidelines' tool."
       → Calls tool

Step 3 (Reason):
Agent: "Okay, I have the guidelines. Now I will draft the plan 
       for the mobile app launch."

Step 4 (Act):
Agent: "I'll write the plan to 'plans/mobile_launch.md'."
       → Calls 'save_plan' tool

Output: "I have saved the OKRs to plans/mobile_launch.md"
```

### Reasoning vs Simple Prompting

**Simple Prompt:**
```
"Draft OKRs for mobile app launch"
→ LLM generates answer immediately
→ Might miss company specific guidelines
```

**ReAct Agent:**
```
"Draft OKRs for mobile app launch"
→ Agent reasons about approach
→ Uses tools to gather data/rules
→ Uses tools to save output
→ More deliberate, more accurate
```

### In Lab 2
We implement this exact pattern (Reason → Act → Observe) manually to understand how Agents "think" and use tools like `read_file` and `save_plan`.

---

## 8. What is MCP? (Advanced)

### MCP = Model Context Protocol

### The Problem MCP Solves
Integrating tools with LLMs can be messy. OpenAI has one format, Anthropic has another, and local models have others.
- **Function Calling:** Direct integration with one LLM provider.
- **MCP:** A standard way to expose tools that works with any LLM.

### How It Works
MCP is a **standard protocol** for connecting tools to LLMs:
```
Your Tool   ─┐
Database    ─┼─ MCP Server ─ MCP Protocol ─ LLM
External API┘
```

### Why It Matters
While we use direct function calling in **Lab 2** for simplicity, MCP represents the future where:
1.  **MCP Server:** Exposes your tools (e.g., "Get Employee Data", "Save Review").
2.  **MCP Client:** (The LLM) Consumes them using a standardized language.

This allows you to swap LLM providers (e.g., from OpenAI to Anthropic) without rewriting your tool definitions.

---

## Summary & Key Takeaways

### The AI Pipeline
```
Documents → Chunk → Embed → Store (Vector DB)
                                ↓
                User Query → Embed → Search → Retrieve → Augment → LLM → Answer
                                                         (RAG)
```

### Connection to Labs
- **Lab 1 (RAG):** Uses embeddings + vector DB + chunking + retrieval.
- **Lab 2 (Agents):** Uses reasoning + function calling + ReAct loop.

### Questions to Think About
1. **For Lab 1:** What documents would you want searchable?
2. **For Lab 2:** What decisions should your agent make?
3. **About RAG:** When would you use it vs. just prompting?
4. **About Agents:** What tools would make your workflows better?

---

**Next Step:** [Go to Lab 1 Guide](LAB1_RAG.md)
