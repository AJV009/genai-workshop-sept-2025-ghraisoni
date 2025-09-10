#!/usr/bin/env python3
"""
Session 02: Simple Chatbot Implementation
"""

import json
from typing import List, Dict

class SimpleChatbot:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model = model_name
        self.conversation_history: List[Dict] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_response(self, user_input: str) -> str:
        """Generate a response (mock implementation)"""
        self.add_message("user", user_input)
        
        # Mock response - in real implementation, call API here
        response = f"Echo: {user_input}"
        self.add_message("assistant", response)
        
        return response
    
    def save_conversation(self, filename: str):
        """Save conversation to file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)

if __name__ == "__main__":
    bot = SimpleChatbot()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        response = bot.get_response(user_input)
        print(f"Bot: {response}")
    
    bot.save_conversation("conversation.json")