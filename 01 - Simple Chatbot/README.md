# Simple Chatbot

Basic chatbots using OpenAI and Gradio.

## Setup

1. Install uv from https://docs.astral.sh/uv/
2. Copy `.env.example` to `.env` and add your API key
3. Run a chatbot:

**Simple chatbot (no history):**
```bash
uv sync
uv run main.py
```

**Simple chatbot with history:**
```bash
uv sync
uv run main_with_history.py
```

The chatbot will open in your browser at http://localhost:7860