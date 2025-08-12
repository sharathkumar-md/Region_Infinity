# JEE Math Solver

A comprehensive, unified package for solving JEE-level mathematics problems with AI reasoning and mathematical verification.

## Features

- **Gemini AI Integration**: Advanced reasoning engine for complex problem solving
- **SymPy CAS Verification**: Automatic mathematical validation prevents hallucinations  
- **Structured Explanations**: Step-by-step approach with critical thinking insights
- **JEE-Optimized**: Specialized prompts for Indian competitive mathematics
- **Dual Interface**: Both CLI and web API for different use cases
- **Self-Correction**: Multi-round LLM refinement with verification feedback
- **Batch Processing**: Solve multiple problems efficiently

## Architecture

```
jee_math_solver/
├── __init__.py          # Package initialization
├── cli.py               # Enhanced CLI interface  
├── app.py               # FastAPI web service
├── controller.py        # Unified solving logic with LLM + CAS loop
├── llm_client.py        # Multi-provider LLM client (Gemini primary)
├── cas_verifier.py      # Advanced SymPy verification engine
├── prompts.py           # Optimized prompt templates
└── requirements.txt     # Dependencies
```

## Installation & Setup

```powershell
# 1. Install dependencies
pip install -r .\jee_math_solver\requirements.txt

# 2. Set up Gemini API key
$env:GEMINI_API_KEY = "your_api_key_here"
```

## 💻 CLI Usage

```powershell
# Basic problem solving
python -m jee_math_solver.cli "What is sin(30°)?"

# Complex problems  
python -m jee_math_solver.cli "Solve x² + 5x + 6 = 0"
python -m jee_math_solver.cli "Find the derivative of sin(x)cos(x)"
```

### CLI Output Example
```
Solving: What is sin(30°)?
==================================================

=== Final Answer ===
1/2

=== Mathematical Verification ===
✓ Answer is mathematically valid
Simplified form: 1/2
Numerical value confirmed
Simple expression

=== Approach ===
1. Recognize 30° as a standard trigonometric angle
2. Recall exact value from unit circle: sin(30°) = 1/2
3. Verify using 30-60-90 triangle ratios

=== Critical Thinking ===
Standard angle - should be memorized. Common mistake: 
using decimal 0.5 instead of exact fraction 1/2.
Related: cos(60°) = 1/2, part of fundamental trig identities.

==================================================
Solution complete!
```

## Web API Usage

```powershell
# Start the API server
python -m uvicorn jee_math_solver.app:app --reload
```

### API Endpoints

**Health Check**
```http
GET /health
```

**Solve Single Problem**  
```http
POST /solve
Content-Type: application/json

{
  "problem": "What is sin(30°)?",
  "max_rounds": 3,
  "structured": false
}
```

**Solve with Detailed Steps**
```http
POST /solve/steps
Content-Type: application/json

{
  "problem": "Solve x² + 5x + 6 = 0",
  "max_rounds": 3
}
```

**Batch Solving**
```http
POST /solve/batch
Content-Type: application/json

{
  "problems": ["What is sin(30°)?", "Solve x² + 5x + 6 = 0"],
  "max_rounds": 3,
  "structured": false
}
```

**Example Problems**
```http
GET /examples
```

## 🧪 Key Capabilities

### Mathematical Verification
- Symbolic algebra validation using SymPy
- LaTeX expression parsing  
- Automatic answer simplification
- Complex number and real number detection
- Expression complexity analysis

### AI Reasoning  
- Multi-round problem solving with self-correction
- Structured step-by-step explanations
- Critical thinking and common pitfall analysis
- Method selection reasoning
- JSON response validation and repair

### Robustness
- Graceful error handling and fallbacks
- Multiple verification strategies  
- Provider-agnostic LLM client design
- Comprehensive logging and debugging info

## Supported Problem Types

- **Trigonometry**: Standard angles, identities, equations
- **Algebra**: Polynomial equations, systems, factoring  
- **Calculus**: Derivatives, integrals, limits
- **Complex Numbers**: Roots, operations, polar form
- **Number Theory**: Proofs, divisibility, modular arithmetic
- **Geometry**: Coordinate geometry, analytical solutions

## Advanced Usage

### Programmatic Access
```python
from jee_math_solver import solve, verify_mathematical_answer

# Solve a problem
result = solve("What is sin(30°)?")
print(result["final_answer"])  # "1/2"

# Verify an answer
verification = verify_mathematical_answer("1/2")
print(verification["is_valid"])  # True
```

### Custom LLM Configuration
```python
from jee_math_solver.llm_client import create_llm_client

# Create custom client (future: OpenAI, Claude, etc.)
client = create_llm_client("gemini", api_key_env="CUSTOM_API_KEY")
```

## What Makes This Special

1. **Real Mathematical Verification**: Unlike pure LLM solutions, this prevents mathematical hallucinations through SymPy validation

2. **Self-Correcting AI**: Multi-round refinement where verification failures trigger LLM corrections  

3. **JEE-Specialized**: Prompts and examples optimized for Indian competitive mathematics

4. **Production Ready**: Comprehensive error handling, logging, and robust JSON parsing

5. **Extensible Architecture**: Modular design supports multiple LLM providers and verification strategies

## 🎓 Perfect For

- **Students**: Get step-by-step solutions with explanations
- **Teachers**: Generate verified problem solutions and explanations  
- **Developers**: Integrate mathematical reasoning into applications
- **Researchers**: Baseline for mathematical AI evaluation

---

**Made with ❤️ for the JEE mathematics community**
