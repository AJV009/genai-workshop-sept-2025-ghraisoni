#!/usr/bin/env python3
"""
Session 03: Prompt Templates and Engineering
"""

from string import Template
from typing import Dict, List

class PromptTemplate:
    def __init__(self, template: str, description: str = ""):
        self.template = Template(template)
        self.description = description
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables"""
        return self.template.safe_substitute(**kwargs)

class PromptLibrary:
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default prompt templates"""
        self.templates = {
            "summarize": PromptTemplate(
                "Summarize the following text in $length words:\n\n$text",
                "Text summarization with length control"
            ),
            "explain": PromptTemplate(
                "Explain $concept to a $audience in simple terms:\n\n$context",
                "Concept explanation for different audiences"
            ),
            "code_review": PromptTemplate(
                "Review this $language code and provide feedback:\n\n```$language\n$code\n```\n\nFocus on: $focus_areas",
                "Code review with specific focus areas"
            ),
            "creative_writing": PromptTemplate(
                "Write a $genre story about $topic. Style: $style. Length: $length words.",
                "Creative writing with genre and style control"
            )
        }
    
    def get_template(self, name: str) -> PromptTemplate:
        """Get a template by name"""
        return self.templates.get(name)
    
    def add_template(self, name: str, template: PromptTemplate):
        """Add a new template"""
        self.templates[name] = template
    
    def list_templates(self) -> List[str]:
        """List all available templates"""
        return list(self.templates.keys())

# Example usage
if __name__ == "__main__":
    library = PromptLibrary()
    
    # Use summarize template
    summarize_prompt = library.get_template("summarize")
    formatted = summarize_prompt.format(
        length="50",
        text="Artificial Intelligence is transforming industries..."
    )
    print("Summarize Prompt:")
    print(formatted)
    print("\n" + "="*50 + "\n")
    
    # Use code review template
    review_prompt = library.get_template("code_review")
    formatted = review_prompt.format(
        language="python",
        code="def hello():\n    print('world')",
        focus_areas="performance, readability, best practices"
    )
    print("Code Review Prompt:")
    print(formatted)