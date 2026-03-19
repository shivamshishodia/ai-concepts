# Minimal LiteLLMModel connectivity test for local Ollama server
# Setup: Ensure you have followed the instructions in readme.md (venv, dependencies, and Ollama server running with required model pulled)

from smolagents import LiteLLMModel

# Instantiate model for Ollama server (adjust model_id/api_base as needed)
model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)

# Send a basic prompt in required message schema, print response
# 'content' must be a list of dicts, each with 'type': 'text' and 'text' fields
print(model([{"role": "user", "content": [{"type": "text", "text": "Hello! What is 2 + 2?"}]}]))
