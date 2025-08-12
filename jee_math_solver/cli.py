# cli.py
"""
Enhanced CLI interface for the unified JEE Math Solver.
"""

import sys
from typing import NoReturn

from .llm_client import solve_question
from .cas_verifier import verify_mathematical_answer, extract_numerical_answer


def main() -> NoReturn:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("JEE Math Solver CLI")
        print("=" * 50)
        print("Usage: python -m jee_math_solver.cli '<your question here>'")
        print("\nExamples:")
        print("  python -m jee_math_solver.cli \"What is sin(30°)?\"")
        print("  python -m jee_math_solver.cli \"Solve x² + 5x + 6 = 0\"")
        print("  python -m jee_math_solver.cli \"Find the derivative of sin(x)cos(x)\"")
        print("\nRequirements:")
        print("  - Set GEMINI_API_KEY environment variable")
        print("  - Install dependencies: pip install -r requirements.txt")
        sys.exit(1)

    question = sys.argv[1]
    print(f"Solving: {question}")
    print("=" * 50)
    
    # Get LLM response
    result = solve_question(question)

    if "error" in result:
        print("❌ Error:", result["error"]) 
        raw = result.get("raw")
        if raw:
            print("\n📄 Raw output:")
            print(raw)
        sys.exit(2)

    # Display structured results
    print("\n=== Final Answer ===")
    final_answer = result.get("final_answer", "<missing>")
    print(final_answer)
    
    # Verify the answer using SymPy
    print("\n=== Mathematical Verification ===")
    verification = verify_mathematical_answer(final_answer, question)
    
    if verification["is_valid"]:
        print("✓ Answer is mathematically valid")
        simplified = verification["simplified_answer"]
        if simplified and simplified != final_answer.strip():
            print(f"Simplified form: {simplified}")
        
        # Show verification details
        details = verification["verification_details"]
        if details and details.get("is_numeric"):
            print(f"Numerical value confirmed")
            
        # Show complexity measure
        if details and details.get("complexity"):
            complexity = details["complexity"]
            if complexity < 10:
                print("Simple expression")
            elif complexity < 50:
                print("Moderate complexity")
            else:
                print("Complex expression")
    else:
        print("Warning: Could not verify answer mathematically")
        if verification["error"]:
            print(f"   Reason: {verification['error']}")
        
        # Try to extract numerical answer as fallback
        numerical = extract_numerical_answer(final_answer)
        if numerical:
            print(f"Extracted numerical value: {numerical}")
            num_verification = verify_mathematical_answer(numerical)
            if num_verification["is_valid"]:
                print(f"✓ Numerical answer verified: {num_verification['simplified_answer']}")

    print("\n=== Approach ===")
    approach = result.get("approach", "<missing>")
    print(approach)
    
    print("\n=== Critical Thinking ===")
    critical_thinking = result.get("critical_thinking", "<missing>")
    print(critical_thinking)
    
    # Show additional insights if verification provided them
    if verification.get("verification_details"):
        details = verification["verification_details"]
        if details.get("is_real") is True:
            print("\nAdditional insights: Answer is a real number")
        elif details.get("is_real") is False:
            print("\nAdditional insights: Answer involves complex numbers")
    
    print("\n" + "=" * 50)
    print("Solution complete!")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
