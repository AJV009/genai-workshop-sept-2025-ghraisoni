"""
MAIN.PY - Gradio UI for RAG Chatbot

What it does:
- Creates a web-based chatbot interface using Gradio
- Connects to your local FastAPI server (or a shared one via ngrok)
- Provides a clean UI for chatting with your RAG-enhanced bot

How it works:
1. User types a message in the Gradio interface
2. Sends the message to the API server (local or shared)
3. The API server handles RAG and returns streaming responses
4. Displays the response in real-time in the chat interface

Usage scenarios:
- Local: API_BASE_URL=http://localhost:8000/v1 (default)
- Shared: API_BASE_URL=https://your-friend.ngrok.io/v1
"""

import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("../.env.secret")

# Initialize client to connect to local API server (or shared via ngrok)
api_client = OpenAI(
    api_key="local-api-key",  # Not validated by our simple API
    base_url=os.getenv("API_BASE_URL", "http://localhost:8000/v1")
)

def chat(message, history):
    # Build messages from conversation history
    messages = []
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    messages.append({"role": "user", "content": message})
    
    # Send to API server (handles RAG, context injection, and OpenAI calls)
    stream = api_client.chat.completions.create(
        model="tech-news-bot",  # Custom model name for our RAG bot
        messages=messages,
        stream=True
    )
    
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            yield response

demo = gr.ChatInterface(chat, title="RAG Chatbot - Tech News Assistant")
demo.launch()