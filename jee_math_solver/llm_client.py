# llm_client.py
"""
Unified LLM client supporting both Gemini (CLI) and extensible providers (API).
"""

from __future__ import annotations

import os
import json
from typing import List, Dict, Any, Optional

import google.generativeai as genai
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT, build_user_prompt

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class LLMClient:
    """Extensible LLM client for different providers."""
    
    def __init__(self, provider: str = "gemini", api_key_env: str = "GEMINI_API_KEY") -> None:
        self.provider = provider
        self.api_key_env = api_key_env
        
        if provider == "gemini":
            genai.configure(api_key=os.getenv(api_key_env))
        elif provider == "openai":
            # Future: OpenAI integration
            pass

    async def chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Async chat method for API usage."""
        if self.provider == "gemini":
            return await self._chat_gemini_async(messages)
        else:
            # Placeholder for other providers
            return {"content": "{\"final_answer\": null}"}

    def chat_sync(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Synchronous chat method."""
        if self.provider == "gemini":
            return self._chat_gemini_sync(messages)
        else:
            # Placeholder for other providers
            return {"content": "{\"final_answer\": null}"}
    
    def _chat_gemini_sync(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Synchronous Gemini chat implementation."""
        # Combine system and user messages
        full_prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                full_prompt += msg["content"] + "\n\n"
            elif msg["role"] == "user":
                full_prompt += msg["content"]
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        
        return {"content": response.text.strip()}
    
    async def _chat_gemini_async(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Async wrapper for Gemini (currently delegates to sync)."""
        return self._chat_gemini_sync(messages)


def solve_question(question: str) -> Dict[str, Any]:
    """
    Direct function for CLI usage with Gemini.
    Maintains backward compatibility with existing CLI code.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = SYSTEM_PROMPT + "\n\n" + build_user_prompt(question)
        
        response = model.generate_content(full_prompt)
        content = response.text.strip()
        
        # Try to parse JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract and repair
            return _repair_json_response(content)
            
    except Exception as e:
        return {"error": f"LLM API error: {str(e)}", "raw": None}


def _repair_json_response(content: str) -> Dict[str, Any]:
    """Attempt to repair malformed JSON responses from LLM."""
    # Look for JSON-like content between braces
    import re
    
    # Try to find JSON block
    json_pattern = r'\{.*\}'
    match = re.search(json_pattern, content, re.DOTALL)
    
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # If all else fails, return error with raw content
    return {
        "error": "Failed to parse JSON", 
        "raw": content,
        "final_answer": "Parse error - see raw output",
        "approach": "Could not extract structured response",
        "critical_thinking": "LLM returned malformed JSON"
    }


# Factory function for creating LLM clients
def create_llm_client(provider: str = "gemini", **kwargs) -> LLMClient:
    """Factory function to create LLM clients."""
    return LLMClient(provider=provider, **kwargs)
