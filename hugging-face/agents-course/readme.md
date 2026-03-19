# Agents Course - Quick Reference Notes

## Resources
- [Hugging Face - Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction)

## Setup
```sh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install 'smolagents[litellm]'
```

## Unit 0: Running Models Locally with Ollama
- [Running Models Locally with Ollama](https://huggingface.co/learn/agents-course/en/unit0/onboarding#step-5-running-models-locally-with-ollama-in-case-you-run-into-credit-limits)
    - **Install Ollama:**
      `curl -fsSL https://ollama.com/install.sh | sh`
    - **Pull a Model Locally:**
      `ollama pull qwen2:7b`
      [List of available models](https://ollama.com/search)
    - **Start Ollama in the background:**
      `ollama serve` (in a terminal)
        - If you see `listen tcp 127.0.0.1:11434: bind: address already in use`, run `sudo lsof -i :11434` to find the process using the port.
          If the process is `ollama`, the service is already started—no need to start it again.
    - **Install LiteLLMModel support:**
      `pip install 'smolagents[litellm]'`

## Unit 1: Agents and LLMs

### What is an Agent?
- An agent is an AI model capable of reasoning, planning, and interacting with its environment.
- **Components:**
    - *Brain*: The AI model itself
    - *Body*: Capabilities and tools it can use
- **Agent Types:**
    - *Simple processor*: Output does not change program flow
    - *Router*: Output determines basic control flow
    - *Tool caller*: Output decides which function(s) to execute
    - *Multi-step agent*: Controls iteration and continuation
    - *Multi-agent*: One workflow triggers another

### What are LLMs?
- Most LLMs are based on the Transformer architecture.

#### Types of Transformers
- **Encoder**: Processes input data into dense representations (e.g., BERT)
- **Decoder**: Generates output sequences token by token (e.g., Llama)
- **Seq2Seq (Encoder-Decoder)**: Encodes input then decodes to output (e.g., T5, BART)
- LLMs are usually decoder-based and contain billions of parameters.

#### Tokenization
- LLMs operate on *tokens*—subword units, not whole words, for efficiency.
    - Examples: "interest"+"ing" → "interesting", "interest"+"ed" → "interested"

#### Next Token Prediction
- LLMs are *autoregressive*: they predict the next token based on previous tokens until hitting an end-of-sequence (EOS) token.
- [Understanding next token prediction](https://huggingface.co/learn/agents-course/en/unit1/what-are-llms#understanding-next-token-prediction)

#### Attention Mechanism
- Attention is a key part of Transformer models, allowing focus on the most relevant parts of input (e.g., "France" and "capital" in "The capital of France is ...").

#### Context Length
- Max tokens the LLM can process (its "attention span").

### Prompts
- **System Prompt:** Defines model behavior and tool instructions (persistent).
- **User and Assistant Prompts:** Alternating messages in a conversation.

Example prompt conversation for SmolLM:
```python
system_message = {
  "role": "system",
  "content": "You are a helpful AI assistant named SmolLM, trained by Hugging Face."
}
conversation = [
  {"role": "user", "content": "I need help with my order"},
  {"role": "assistant", "content": "I'd be happy to help. Could you provide your order number?"},
  {"role": "user", "content": "It's ORDER-123"},
]

# Concatenated for model input (using special tokens for the model):
<|im_start|>system
You are a helpful AI assistant named SmolLM, trained by Hugging Face<|im_end|>
<|im_start|>user
I need help with my order<|im_end|>
<|im_start|>assistant
I'd be happy to help. Could you provide your order number?<|im_end|>
<|im_start|>user
It's ORDER-123<|im_end|>
<|im_start|>assistant
```
*Note: Each model uses its own special tokens for separating message roles.*

### Tools
- A *tool* is a function given to the LLM (e.g., web search, API call).
- LLMs cannot call tools themselves—agents enable tool use by:
    - Describing tools in system prompts
    - Appending tool responses as new messages before re-prompting the LLM

### Model Context Protocol (MCP)
- MCP is an open protocol that standardizes tool provision for LLMs.

### AI Agent Workflow: Thought-Action-Observation

#### Thought
- The LLM decides next steps (planning, reasoning, reflection, decision).
- *Chain-of-Thought (CoT)*: Prompt that guides step-by-step reasoning (no tool use), e.g., "Let's think step by step."
- *ReAct (Reasoning + Acting)*: Alternates reasoning steps with actions/tools (e.g., ReAct pattern).

| Type                | Example                                                                              |
|---------------------|--------------------------------------------------------------------------------------|
| Planning            | Break into steps: 1) gather data, 2) analyze trends, 3) make report                  |
| Analysis            | "Based on the error message, the issue is with the DB connection params"             |
| Decision Making     | "User has budget limits. Recommend mid-tier option."                                 |
| Problem Solving     | "Should profile code to find bottlenecks."                                           |
| Memory Integration  | "User prefers Python, use Python examples."                                          |
| Self-Reflection     | "Last approach failed, try a new one."                                               |
| Goal Setting        | "Set acceptance criteria before starting."                                           |
| Prioritization      | "Fix security issues before new features."                                           |

#### Action
- The agent takes actions by invoking tools (API calls, information gathering, environment interaction, communication).

| Action Type              | Description                                   |
|--------------------------|-----------------------------------------------|
| Information Gathering    | Searches, DB queries, retrieve documents      |
| Tool Usage               | API calls, computations, code execution       |
| Environment Interaction  | Digital/physical device manipulation          |
| Communication            | Chats with users or agents                    |

- *Stop and Parse Approach*: LLM Agents can use text/JSON for actions, or provide code snippets as actions.
  [See documentation](https://huggingface.co/learn/agents-course/en/unit1/actions#the-stop-and-parse-approach)

#### Observation
- The agent processes results from tool calls (appended to prompt as new "observation" messages).

| Observation Type     | Example                                         |
|---------------------|-------------------------------------------------|
| System Feedback     | Errors, success notifications, status codes      |
| Data Changes        | DB/file/system state updates                     |
| Environmental Data  | Sensor readings, metrics, system stats           |
| Response Analysis   | API results, query or computation outputs        |
| Time-based Events   | Scheduled/deadline-related occurrences           |

**Summary:**
- Tools and the Thought-Action-Observation cycle are defined in system prompts.
- Agents extend LLMs with planning, tool use, and environment interaction via standardized workflows.
