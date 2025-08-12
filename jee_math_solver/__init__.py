"""
JEE Math Solver - A comprehensive package for solving JEE-level mathematics problems.

This package provides:
- CLI interface for direct problem solving
- FastAPI web service for programmatic access  
- Advanced CAS verification using SymPy
- Gemini AI integration for mathematical reasoning
"""

__version__ = "1.0.0"
__author__ = "Sharath Kumar MD"

from .cas_verifier import verify_equality, simplify_expr, verify_mathematical_answer
from .llm_client import LLMClient, solve_question
from .prompts import SYSTEM_PROMPT, format_user_prompt, build_user_prompt

__all__ = [
    "verify_equality",
    "simplify_expr", 
    "verify_mathematical_answer",
    "LLMClient",
    "solve_question",
    "SYSTEM_PROMPT",
    "format_user_prompt",
    "build_user_prompt"
]
