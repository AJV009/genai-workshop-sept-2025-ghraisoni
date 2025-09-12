# RAG Chatbot - OpenAI Compatible API

A simple RAG (Retrieval-Augmented Generation) chatbot with OpenAI-compatible API using FastAPI, Pinecone, and Gradio.

## Setup

1. Install uv from https://docs.astral.sh/uv/
2. Copy `.env.example` to `.env` and add your API keys:
   - OpenAI API key
   - Pinecone API key and index name  
   - Gemini API key
3. Install dependencies:

```bash
uv sync
```

4. Index the tech news data:

```bash
uv run python index.py
```

## Running Locally

### Option 1: Full Setup (API + UI)
```bash
# Terminal 1: Start the API server
uv run python api.py

# Terminal 2: Start the Gradio UI
uv run python main.py
```
- API runs at http://localhost:8000
- Gradio UI opens at http://localhost:7860

### Option 2: Just the API
```bash
uv run python api.py
```
Then connect using any OpenAI-compatible client.

## Sharing Your Bot

1. Start the API server:
```bash
uv run python api.py
```

2. Share via ngrok:
```bash
ngrok http 8000
```

3. Share the https URL with friends (e.g., `https://abc123.ngrok.io`)

4. Friends update their `.env` file:
```bash
API_BASE_URL=https://abc123.ngrok.io/v1
```

5. Friends can run their own UI or use any OpenAI client:
```python
from openai import OpenAI

client = OpenAI(
    api_key="anything", 
    base_url="https://abc123.ngrok.io/v1"
)

response = client.chat.completions.create(
    model="tech-news-bot",
    messages=[{"role": "user", "content": "What's new in AI?"}],
    stream=True
)
```

## What it does

- **api.py**: OpenAI-compatible FastAPI server with RAG functionality
- **main.py**: Gradio UI that connects to the API server
- **index.py**: Loads text files from `source_text/` folder, splits them into chunks, and stores in Pinecone
- **embedding.py**: Google Gemini embedding service
- **source_text/**: Contains 5 recent tech news articles about AI developments