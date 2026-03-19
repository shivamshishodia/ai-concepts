# Resources
- Course: [Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction)

# Setup
- python3 -m venv venv
- source venv/bin/activate
- python3 -m pip install 'smolagents[litellm]'

# Unit 0
- [Running Models Locally with Ollama](https://huggingface.co/learn/agents-course/en/unit0/onboarding#step-5-running-models-locally-with-ollama-in-case-you-run-into-credit-limits)
  - Install Ollama        : curl -fsSL https://ollama.com/install.sh | sh
  - Pull a model Locally  : ollama pull qwen2:7b
    Full list of available models can be found [here](https://ollama.com/search)
  - Start Ollama in the background (In one terminal)  : ollama serve
    If you run into the error "listen tcp 127.0.0.1:11434: bind: address already in use", you can use command sudo lsof -i :11434 to identify the process ID (PID) that is currently using this port. If the process is ollama, it is likely that the installation script above has started ollama service, so you can skip this command to start Ollama.
  - Use LiteLLMModel      : pip install 'smolagents[litellm]'

# Unit 1
- [What is an Agent?](https://huggingface.co/learn/agents-course/en/unit1/what-are-agents)
  Agent is an AI model capable of reasoning, planning, and interacting with its environment
    - The Brain (AI Model)
    - The Body (Capabilities and Tools)
  Types:
    - Simple processor  : Agent output has no impact on program flow
    - Router            : Agent output determines basic control flow
    - Tool caller       : Agent output determines function execution
    - Multi-step Agent  : Agent output controls iteration and program continuation
    - Multi-Agent       : One agentic workflow can start another agentic workflow
  Models:
    - Large Language Model (LLM)
    - Vision Language Model (VLM)
- [What are LLMs?](https://huggingface.co/learn/agents-course/en/unit1/what-are-llms)
  Most LLMs nowadays are built on the Transformer architecture
  3 Types of Transformers:
    - Encoders
      An encoder-based Transformer takes text (or other data) as input and outputs a dense representation (or embedding) of that text.
      Example: BERT from Google
    - Decoders
      A decoder-based Transformer focuses on generating new tokens to complete a sequence, one token at a time.
      Example: Llama from Meta
    - Seq2Seq (Encoder–Decoder)
      A sequence-to-sequence Transformer combines an encoder and a decoder. The encoder first processes the input sequence into a context representation, then the decoder generates an output sequence.
      Example: T5, BART
  LLMs are typically decoder-based models with billions of parameters
  LLM's objective is to predict the next token, given a sequence of previous tokens
  Tokens:
    -  A token is the unit of information an LLM works with
    - You can think of a token as if it was a word, but for efficiency reasons LLMs don’t use whole words.
    - For instance, the tokens "interest" and "ing" can be combined to form "interesting", or "ed" can be appended to form "interested"
  [Next Token Prediction](https://huggingface.co/learn/agents-course/en/unit1/what-are-llms#understanding-next-token-prediction)
    LLMs are said to be autoregressive, meaning that the output from one pass becomes the input for the next one. This loop continues until the model predicts the next token to be the EOS token, at which point the model can stop.
  Attention
    Attention is key aspect of the Transformer architecture
    When predicting the next word, not every word in a sentence is equally important;
    Words like "France" and "capital" in the sentence "The capital of France is …" carry the most meaning.
  Context Length
    The maximum number of tokens the LLM can process; the maximum attention span it has
  System Prompt
    Define how the model should behave. They serve as persistent instructions, guiding every subsequent interaction.
    They also give information about the available tools, provides instructions to the model on how to format the actions to take, and includes guidelines on how the thought process should be segmented
  User and Assistant Prompts
    A conversation consists of alternating messages between a Human (user) and an LLM (assistant).

  ```
    system_message = {
      "role": "system",
      "content": "You are a helpful AI assistant named SmolLM, trained by Hugging Face."
    }
    conversation = [
      {"role": "user", "content": "I need help with my order"},
      {"role": "assistant", "content": "I'd be happy to help. Could you provide your order number?"},
      {"role": "user", "content": "It's ORDER-123"},
    ]

    The above conversation is converted into the below rendered prompt before it can be passed to the model.
    Note that each model will have it's own tokenizer type and special tokens (example <|im_start|> is for SmolLM2-135M-Instruct)
    We always concatenate "all" the messages in the conversation and pass it to the LLM as a single stand-alone sequence.

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

  Tools
    Tool is a function given to the LLM. This function should fulfill a clear objective. Example: Web Search, API Interface
    LLMs can only receive text inputs and generate text outputs. They have no way to call tools on their own.
    Agents teach the LLM about the existence of these tools
    The Agent appends tool responses as a new message before passing the updated conversation to the LLM again.
    System prompts provide textual descriptions of available tools to the model
  Model Context Protocol (MCP)
    Open protocol that standardizes how applications provide tools to LLMs
  AI Agent Workflow (Thought-Action-Observation)
    Thought: The LLM part of the Agent decides what the next step should be.
      | Type of Thought	    | Example                                                                                           |
      |---------------------|---------------------------------------------------------------------------------------------------|
      | Planning            | I need to break this task into three steps: 1) gather data, 2) analyze trends, 3) generate report |
      | Analysis            | Based on the error message, the issue appears to be with the database connection parameters       |
      | Decision Making     | Given the user’s budget constraints, I should recommend the mid-tier option                       |
      | Problem Solving     | To optimize this code, I should first profile it to identify bottlenecks                          |
      | Memory Integration  | The user mentioned their preference for Python earlier, so I’ll provide examples in Python        |
      | Self-Reflection     | My last approach didn’t work well, I should try a different strategy                              |
      | Goal Setting        | To complete this task, I need to first establish the acceptance criteria                          |
      | Prioritization      | The security vulnerability should be addressed before adding new features                         |

      - Chain-of-Thought (CoT) is a prompting technique that guides a model to think through a problem step-by-step before producing a final answer. It does not use tools. Example: "Let's think step by step"
      - ReAct (Reasoning + Acting): ReAct is a prompting technique that encourages the model to think step-by-step and interleave actions (like using tools) between reasoning steps (Thought-Action-Observation).

    Action: The agent takes an action by calling the tools with the associated arguments.
      | Type of Action           | Description                                                                              |
      |--------------------------|------------------------------------------------------------------------------------------|
      | Information Gathering    | Performing web searches, querying databases, or retrieving documents.                    |
      | Tool Usage               | Making API calls, running calculations, and executing code.                              |
      | Environment Interaction  | Manipulating digital interfaces or controlling physical devices.                         |
      | Communication            | Engaging with users via chat or collaborating with other agents.                         |

      - [The Stop and Parse Approach](https://huggingface.co/learn/agents-course/en/unit1/actions#the-stop-and-parse-approach)
      LLM Agents can use Text/JSON in actions or Code Snippets as Actions

    Observation: The model reflects on the response from the tool.
      The response from tools are appended into agent's memory at the end of the prompt

      | Type of Observation | Example                                                                   |
      |---------------------|---------------------------------------------------------------------------|
      | System Feedback     | Error messages, success notifications, status codes                       |
      | Data Changes        | Database updates, file system modifications, state changes                |
      | Environmental Data  | Sensor readings, system metrics, resource usage                           |
      | Response Analysis   | API responses, query results, computation outputs                         |
      | Time-based Events   | Deadlines reached, scheduled tasks completed                              |

  Tools and Thought-Action-Observation cycle is specified in the system prompts




