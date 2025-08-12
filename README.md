# Regioninfinity

## JEE Math Solver

A comprehensive AI-powered mathematics solver for JEE-level problems with advanced CAS verification.

### Features

- **AI Integration**: Advanced reasoning for complex problem solving with Gemini
- **CAS Verification**: SymPy verification prevents mathematical hallucinations  
- **Structured Explanations**: Step-by-step approach with critical thinking
- **Dual Interface**: CLI and web API
- **Self-Correction**: Multi-round LLM refinement with verification

### Quick Start

```powershell
# Install dependencies
pip install -r .\jee_math_solver\requirements.txt

# Set API key
$env:GEMINI_API_KEY = "your_api_key_here"

# CLI usage
python -m jee_math_solver.cli "your question"

# API usage  
python -m uvicorn jee_math_solver.app:app --reload
```

See `jee_math_solver/README.md` for complete documentation.