import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("../.env.secret")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

def chat(message, history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    messages.append({"role": "user", "content": message})
    
    stream = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=messages,
        stream=True
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            yield response

demo = gr.ChatInterface(chat, title="Simple Chatbot with History")
demo.launch(share=True)