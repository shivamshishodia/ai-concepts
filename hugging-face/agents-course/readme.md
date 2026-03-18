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
