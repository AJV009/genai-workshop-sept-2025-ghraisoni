"""
API.PY - OpenAI-Compatible FastAPI Server

What it does:
- Creates an OpenAI-compatible API server that other people can connect to
- Implements RAG by adding context to user messages before sending to OpenAI
- Supports both streaming and non-streaming responses
- Can be shared via ngrok so friends can use your custom chatbot

How it works:
1. Receives requests at /v1/chat/completions (standard OpenAI endpoint)
2. Takes the last user message and searches Pinecone for relevant context
3. Adds the context to the user message (not system message)
4. Sends enhanced message to OpenAI and returns response in OpenAI format
5. Supports streaming responses using Server-Sent Events

Usage:
- Run: python api.py
- Share via ngrok: ngrok http 8000
- Others can connect using standard OpenAI client library
"""

import os
import json
import time
import uuid
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
from embedding import get_embedding

load_dotenv("../.env.secret")

app = FastAPI(title="OpenAI-Compatible RAG API")

# Initialize clients
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def search_knowledge(query, top_k=3):
    """Search Pinecone for relevant chunks"""
    query_embedding = get_embedding(query)
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    context = []
    for match in results['matches']:
        context.append(match['metadata']['text'])
    
    return "\n\n".join(context)

@app.post("/v1/chat/completions")
async def chat_completions(request: dict):
    """OpenAI-compatible chat completions endpoint"""
    
    # Extract request data
    messages = request.get("messages", [])
    stream = request.get("stream", False)
    model = request.get("model", "gpt-3.5-turbo")
    
    # Get the last user message for RAG
    last_user_message = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break
    
    # Search for relevant context
    if last_user_message:
        context = search_knowledge(last_user_message)
        # Add context to the last user message
        enhanced_message = f"Provided Context:\n{context}\n\n User query: {last_user_message}"
        
        # Update the last user message with context
        for i in reversed(range(len(messages))):
            if messages[i]["role"] == "user":
                messages[i]["content"] = enhanced_message
                break
    
    # Add system message and few-shot examples
    system_message = "You are a helpful AI assistant with access to recent tech news. Answer based on the provided context when relevant, but you can also use your general knowledge for other questions."
    
    fewshot_examples = [
        {"role": "user", "content": "What's the weather like today?"},
        {"role": "assistant", "content": "BREAKING NEWS from the weather desk! *shuffles meteorological reports frantically* This correspondent is tracking a HIGH-PRESSURE situation developing over the region as we speak! Sources from the National Weather Service are telling us - and folks, you'll want to hear this - conditions are OPTIMAL for outdoor activities. I'm getting real-time updates here... *touches earpiece* ...visibility is UNLIMITED, humidity levels are, and I quote, 'absolutely perfect.' But wait, there's more! Our atmospheric experts predict this pattern will hold for the next 48 hours. We'll continue monitoring this developing weather story. Back to you in the studio!"},
        {"role": "user", "content": "How do I make pasta?"},
        {"role": "assistant", "content": "THIS JUST IN from our culinary correspondent! *dramatic kitchen backdrop* We have a DEVELOPING SITUATION in kitchens across the nation - pasta preparation is UNDERWAY! I'm receiving step-by-step reports from the field: FIRST, we're seeing massive water mobilization - 4 to 6 quarts heading to HIGH HEAT positions! Sources confirm salt deployment is CRITICAL - we're talking one tablespoon per gallon, people! *papers rustling* BREAKING: Pasta insertion should occur ONLY when bubbles reach maximum velocity! Our Italian sources emphasize - and this is CRUCIAL - al dente status typically achieved at 8-10 minutes! TASTE TESTING is being advised by experts on the ground! This has been your emergency pasta bulletin. We now return to regular programming!"}
    ]
    
    # Build final messages array
    final_messages = [{"role": "system", "content": system_message}] + fewshot_examples + messages
    
    # Generate unique ID for this request
    completion_id = f"chatcmpl-{str(uuid.uuid4())[:12]}"
    created_time = int(time.time())
    
    if stream:
        # Streaming response
        async def generate_stream():
            stream_response = openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=final_messages,
                stream=True
            )
            
            for chunk in stream_response:
                if chunk.choices[0].delta.content:
                    chunk_data = {
                        "id": completion_id,
                        "object": "chat.completion.chunk",
                        "created": created_time,
                        "model": model,
                        "choices": [{
                            "index": 0,
                            "delta": {"content": chunk.choices[0].delta.content},
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
            
            # Final chunk
            final_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_time,
                "model": model,
                "choices": [{
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate_stream(), media_type="text/event-stream")
    
    else:
        # Non-streaming response
        response = openai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=final_messages
        )
        
        # Format response to match OpenAI API
        return {
            "id": completion_id,
            "object": "chat.completion",
            "created": created_time,
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                },
                "finish_reason": "stop"
            }]
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting OpenAI-Compatible RAG API server...")
    print("📡 Server will run at: http://localhost:8000")
    print("🔗 API endpoint: http://localhost:8000/v1/chat/completions")
    print("🌐 Share via ngrok: ngrok http 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)