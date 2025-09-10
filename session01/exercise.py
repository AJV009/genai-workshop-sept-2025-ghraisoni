#!/usr/bin/env python3
"""
Session 01 Exercise: Basic GenAI Setup
"""

import os
from datetime import datetime

def setup_environment():
    """Initialize the GenAI development environment"""
    print("Setting up GenAI environment...")
    print(f"Timestamp: {datetime.now()}")
    
    # Check Python version
    import sys
    print(f"Python version: {sys.version}")
    
    # Environment check
    required_vars = ['OPENAI_API_KEY', 'HF_TOKEN']
    for var in required_vars:
        status = "✓ Set" if os.getenv(var) else "✗ Missing"
        print(f"{var}: {status}")

if __name__ == "__main__":
    setup_environment()