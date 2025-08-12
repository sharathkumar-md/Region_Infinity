# app.py
"""
Unified FastAPI application with enhanced features.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .controller import solve, solve_with_steps, batch_solve


class SolveRequest(BaseModel):
    problem: str = Field(..., description="The mathematical problem to solve")
    max_rounds: int = Field(3, description="Maximum LLM correction rounds")
    structured: bool = Field(False, description="Use structured step-by-step format")


class BatchSolveRequest(BaseModel):
    problems: List[str] = Field(..., description="List of mathematical problems")
    max_rounds: int = Field(3, description="Maximum LLM correction rounds")
    structured: bool = Field(False, description="Use structured step-by-step format")


class HealthResponse(BaseModel):
    status: str
    version: str
    features: List[str]


# Create FastAPI app
app = FastAPI(
    title="JEE Math Solver API", 
    description="Advanced API for solving JEE-level mathematics problems with AI + CAS verification",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint with system information."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        features=[
            "Gemini AI integration",
            "SymPy CAS verification", 
            "Step-by-step solving",
            "Batch processing",
            "Mathematical validation"
        ]
    )


@app.post("/solve")
def solve_problem(req: SolveRequest):
    """
    Solve a single mathematical problem.
    
    Returns structured solution with verification details.
    """
    try:
        result = solve(
            req.problem, 
            max_rounds=req.max_rounds, 
            structured=req.structured
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/solve/steps")
def solve_with_detailed_steps(req: SolveRequest):
    """
    Solve with detailed step-by-step verification.
    
    Returns enhanced solution with step verification.
    """
    try:
        result = solve_with_steps(req.problem, max_rounds=req.max_rounds)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/solve/batch")
def solve_multiple_problems(req: BatchSolveRequest):
    """
    Solve multiple problems in batch.
    
    Returns list of solutions with individual verification.
    """
    try:
        results = batch_solve(
            req.problems,
            max_rounds=req.max_rounds,
            structured=req.structured
        )
        return {"results": results, "count": len(results)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/examples")
def get_example_problems():
    """Get example problems for testing."""
    return {
        "basic": [
            "What is sin(30°)?",
            "Solve x² + 5x + 6 = 0",
            "Find the derivative of sin(x)cos(x)"
        ],
        "intermediate": [
            "Evaluate the integral ∫(2x + 3)dx from 0 to 5",
            "Find the limit of (sin(x)/x) as x approaches 0",
            "Solve the system: 2x + 3y = 7, x - y = 1"
        ],
        "advanced": [
            "Find the period of F(x)+F(x+T)=F(x+2)+F(x+T+6)",
            "Prove that √2 is irrational",
            "Find the complex roots of z³ - 8 = 0"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("jee_math_solver.app:app", host="0.0.0.0", port=8000, reload=True)
