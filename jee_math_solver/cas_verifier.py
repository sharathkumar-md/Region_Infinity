# cas_verifier.py
"""
Unified CAS (Computer Algebra System) verifier combining the best features from both implementations.
"""

from __future__ import annotations

import re
import sympy as sp
from typing import Dict, Any, Optional


# Pre-configured symbols and functions for mathematical parsing
SYMBOL_NAMES = ["x", "y", "z", "t", "u", "v", "n", "m", "k", "T"]
FUNC_NAMES = ["F", "G", "H", "f", "g", "h"]

LOCALS: Dict[str, Any] = {name: sp.symbols(name) for name in SYMBOL_NAMES}
LOCALS.update({name: sp.Function(name) for name in FUNC_NAMES})

# Optional LaTeX parsing support
try:
    from sympy.parsing.latex import parse_latex  # type: ignore
except Exception:
    parse_latex = None  # type: ignore


def _looks_like_latex(s: str) -> bool:
    """Check if a string looks like LaTeX notation."""
    s = s.strip()
    if not s:
        return False
    latex_markers = ["\\frac", "\\sqrt", "\\left", "\\right", "^{", "_{", "\\sin", "\\cos"]
    return any(m in s for m in latex_markers) or (s.startswith("$") and s.endswith("$"))


def _parse(expr: str) -> sp.Expr:
    """Parse expression with LaTeX support fallback to SymPy."""
    expr = expr.strip()
    if not expr:
        raise ValueError("empty expression")
    
    # Strip dollar signs if LaTeX math mode
    if expr.startswith("$") and expr.endswith("$"):
        expr = expr[1:-1]
    
    # Try LaTeX first if it looks like LaTeX and parser is available
    if parse_latex and _looks_like_latex(expr):
        try:
            return parse_latex(expr)
        except Exception:
            pass
    
    # Fallback: sympify with predefined locals
    return sp.sympify(expr, locals=LOCALS)


def clean_expression(expr: str) -> str:
    """Clean and normalize mathematical expressions for SymPy parsing."""
    original_expr = expr.strip()
    
    # Handle function notation like "f'(x) = ..." - extract just the expression part
    if "=" in original_expr and ("f'" in original_expr or "d/dx" in original_expr or "derivative" in original_expr.lower()):
        parts = original_expr.split('=')
        if len(parts) == 2:
            expr = parts[1].strip()
    
    # Handle equation format like "x = 2" or "answer = 3" 
    # Extract the right-hand side (the actual value/expression)
    elif '=' in original_expr:
        # Split on '=' and take the right side (the answer)
        parts = original_expr.split('=')
        if len(parts) == 2:
            # Check if left side looks like a variable assignment (x =, y =, answer =, etc.)
            left = parts[0].strip()
            right = parts[1].strip()
            
            # Common patterns for variable assignment
            var_patterns = [r'^[a-zA-Z]\s*$', r'^answer\s*$', r'^solution\s*$', r'^result\s*$']
            
            if any(re.match(pattern, left, re.IGNORECASE) for pattern in var_patterns):
                # This looks like "x = value", so use the value part
                expr = right
            else:
                # This might be an equation like "2x + 1 = 5", keep as is for now
                expr = original_expr
        else:
            # Multiple = signs, remove common text patterns
            expr = re.sub(r'\b(answer|is|equals?)\s*=\s*', '', expr, flags=re.IGNORECASE)
    
    # Replace Unicode mathematical symbols with ASCII equivalents
    unicode_replacements = {
        '²': '**2',
        '³': '**3', 
        '⁴': '**4',
        '⁵': '**5',
        '⁶': '**6',
        '⁷': '**7',
        '⁸': '**8',
        '⁹': '**9',
        '¹': '**1',
        '⁰': '**0',
        '°': '*pi/180',  # degrees to radians
        '√': 'sqrt',
        '∞': 'oo',
        'π': 'pi',
        'ln': 'log',
        '×': '*',
        '·': '*',
        '÷': '/',
    }
    
    for old, new in unicode_replacements.items():
        expr = expr.replace(old, new)
    
    # Remove other common text patterns (but not = if it's part of an equation)
    if '=' not in expr:
        expr = re.sub(r'\b(answer|is|equals?)\b', '', expr, flags=re.IGNORECASE)
    
    # Replace common mathematical notation
    replacements = {
        'sin': 'sin',  # SymPy understands these
        'cos': 'cos',
        'tan': 'tan',
        'exp': 'exp',
        'log': 'log',
    }
    
    # Clean whitespace and common prefixes
    expr = expr.strip()
    expr = re.sub(r'^(the\s+)?(answer\s+is\s+)?', '', expr, flags=re.IGNORECASE)
    
    return expr


def simplify_expr(expr: str) -> str:
    """Return a simplified string form of an expression."""
    try:
        e = _parse(expr)
        s = sp.simplify(e)
        return str(s)
    except Exception as exc:
        return f"<parse_error: {exc}>"


def verify_equality(lhs: str, rhs: str) -> Dict[str, Optional[str]]:
    """
    Verify whether lhs == rhs using symbolic simplification.
    
    Returns a dict with keys:
      - ok: bool result in string form for JSON-friendliness
      - diff_simplified: str representation of simplify(lhs - rhs)
      - error: optional error message
    """
    try:
        l = _parse(lhs)
        r = _parse(rhs)
        diff = sp.simplify(l - r)
        ok = bool(diff == 0)
        return {
            "ok": str(ok),
            "diff_simplified": str(diff),
            "error": None,
        }
    except Exception as exc:
        return {
            "ok": "False",
            "diff_simplified": None,
            "error": str(exc),
        }


def verify_mathematical_answer(expression: str, context: str = "") -> Dict[str, Any]:
    """
    Verify if a mathematical expression/answer is valid using SymPy.
    Enhanced version with detailed verification information.
    """
    try:
        # Clean the expression
        cleaned_expr = clean_expression(expression)
        
        # Try to parse with SymPy
        parsed = _parse(cleaned_expr)
        
        # Simplify the expression
        simplified = sp.simplify(parsed)
        
        # Check if it's a valid mathematical object
        is_valid = True
        error_msg = None
        
        # Additional verification details
        verification_details = {
            "original": expression,
            "cleaned": cleaned_expr,
            "parsed": str(parsed),
            "simplified": str(simplified),
            "is_numeric": parsed.is_number if hasattr(parsed, 'is_number') else None,
            "is_real": parsed.is_real if hasattr(parsed, 'is_real') else None,
            "complexity": len(str(simplified))
        }
        
        return {
            "is_valid": is_valid,
            "simplified_answer": str(simplified),
            "verification_details": verification_details,
            "error": error_msg
        }
        
    except Exception as e:
        return {
            "is_valid": False,
            "simplified_answer": None,
            "verification_details": None,
            "error": f"SymPy parsing error: {str(e)}"
        }


def extract_numerical_answer(text: str) -> Optional[str]:
    """Extract numerical answers from text responses."""
    # Handle case where text might be a number already
    if isinstance(text, (int, float)):
        return str(text)
    
    # Ensure we have a string
    if not isinstance(text, str):
        text = str(text)
    
    # Look for common answer patterns
    patterns = [
        r'(?:answer|result|solution)\s*(?:is|=|:)\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)',
        r'([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)\s*(?:degrees?|radians?|units?)?$',
        r'=\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


if __name__ == "__main__":
    # Test the unified verifier
    test_cases = [
        ("x + 2", "2 + x", True),
        ("sin(x)**2 + cos(x)**2", "1", True),
        ("sqrt(2)**2", "2", True),
        ("0.5", None, True),
        ("sin(30°)", None, True),
        ("pi/6", None, True),
    ]
    
    print("Testing verify_equality:")
    for lhs, rhs, expected in test_cases:
        if rhs:
            result = verify_equality(lhs, rhs)
            status = "✓" if (result["ok"] == "True") == expected else "✗"
            print(f"{status} {lhs} == {rhs}: {result['ok']}")
    
    print("\nTesting verify_mathematical_answer:")
    for expr, _, _ in test_cases:
        if expr:
            result = verify_mathematical_answer(expr)
            status = "✓" if result["is_valid"] else "✗"
            print(f"{status} '{expr}' -> {result['simplified_answer']}")
