"""
Constraint-checking logic for verifying puzzle solutions.
Supports both rule-based verification (for structured puzzles) and LLM-based verification.
"""

import json
from typing import Any
from openai import OpenAI
from pydantic import BaseModel


class ClueVerification(BaseModel):
    """Result of verifying a single clue."""

    clue: str
    passed: bool
    explanation: str


class VerificationResult(BaseModel):
    """Complete verification result for a puzzle."""

    total_clues: int
    passed_clues: int
    failed_clues: int
    all_passed: bool
    details: list[ClueVerification]


def verify_with_llm(
    solution: dict[str, Any],
    clues: list[str],
    puzzle_description: str,
    client: OpenAI,
) -> VerificationResult:
    """
    Use an LLM to verify each clue against the solution.
    This is the most flexible approach and works for any puzzle type.
    """
    details = []

    for clue in clues:
        prompt = f"""You are a logic puzzle verifier. Given a solution and a clue, determine if the solution satisfies the clue.

Puzzle Description: {puzzle_description}

Solution (as JSON):
{json.dumps(solution, indent=2)}

Clue to verify: "{clue}"

Analyze whether this specific clue is satisfied by the solution. Consider:
1. Does the solution explicitly or implicitly satisfy this constraint?
2. Is there any contradiction?

Respond with a JSON object:
{{"passed": true/false, "explanation": "Brief explanation of why it passes or fails"}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
        )

        result = json.loads(response.choices[0].message.content)
        details.append(
            ClueVerification(
                clue=clue,
                passed=result.get("passed", False),
                explanation=result.get("explanation", "No explanation provided"),
            )
        )

    passed_count = sum(1 for d in details if d.passed)
    return VerificationResult(
        total_clues=len(clues),
        passed_clues=passed_count,
        failed_clues=len(clues) - passed_count,
        all_passed=passed_count == len(clues),
        details=details,
    )


def verify_ordering_puzzle(
    solution: dict[str, str],
    clues: list[str],
    client: OpenAI,
    puzzle_description: str,
) -> VerificationResult:
    """
    Verify an ordering puzzle (e.g., race positions).
    Falls back to LLM verification for complex clues.
    """
    # For ordering puzzles, we use LLM verification as clues can be complex
    return verify_with_llm(solution, clues, puzzle_description, client)


def verify_grid_puzzle(
    solution: dict[str, Any],
    clues: list[str],
    client: OpenAI,
    puzzle_description: str,
) -> VerificationResult:
    """
    Verify a grid puzzle (matching entities to attributes).
    Falls back to LLM verification for complex clues.
    """
    return verify_with_llm(solution, clues, puzzle_description, client)


def verify_einstein_puzzle(
    solution: dict[str, Any],
    clues: list[str],
    client: OpenAI,
    puzzle_description: str,
) -> VerificationResult:
    """
    Verify an Einstein-style puzzle with multiple attributes per entity.
    Uses LLM verification due to complexity.
    """
    return verify_with_llm(solution, clues, puzzle_description, client)


def verify(
    solution: dict[str, Any],
    clues: list[str],
    puzzle_type: str,
    puzzle_description: str,
    client: OpenAI,
) -> VerificationResult:
    """
    Main verification function that routes to the appropriate verifier.

    Args:
        solution: The solution to verify (dict mapping entities to attributes)
        clues: List of clue strings
        puzzle_type: Type of puzzle ("ordering", "grid", "einstein")
        puzzle_description: Description of the puzzle for context
        client: OpenAI client for LLM-based verification

    Returns:
        VerificationResult with pass/fail status for each clue
    """
    if puzzle_type == "ordering":
        return verify_ordering_puzzle(solution, clues, client, puzzle_description)
    elif puzzle_type == "grid":
        return verify_grid_puzzle(solution, clues, client, puzzle_description)
    elif puzzle_type == "einstein":
        return verify_einstein_puzzle(solution, clues, client, puzzle_description)
    else:
        # Default to LLM verification
        return verify_with_llm(solution, clues, puzzle_description, client)


def compare_with_expected(
    solution: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[bool, str]:
    """
    Compare the model's solution with the expected solution.

    Returns:
        Tuple of (matches: bool, explanation: str)
    """

    def normalize(obj: Any) -> Any:
        """Normalize an object for comparison."""
        if isinstance(obj, dict):
            return {k.lower().strip(): normalize(v) for k, v in obj.items()}
        elif isinstance(obj, str):
            return obj.lower().strip()
        elif isinstance(obj, list):
            return [normalize(item) for item in obj]
        return obj

    norm_solution = normalize(solution)
    norm_expected = normalize(expected)

    if norm_solution == norm_expected:
        return True, "Solution matches expected answer exactly."

    # Check for structural similarity
    if set(norm_solution.keys()) != set(norm_expected.keys()):
        missing = set(norm_expected.keys()) - set(norm_solution.keys())
        extra = set(norm_solution.keys()) - set(norm_expected.keys())
        explanation = []
        if missing:
            explanation.append(f"Missing keys: {missing}")
        if extra:
            explanation.append(f"Extra keys: {extra}")
        return False, " ".join(explanation)

    # Find specific differences
    differences = []
    for key in norm_expected:
        if norm_solution.get(key) != norm_expected.get(key):
            differences.append(
                f"{key}: got '{norm_solution.get(key)}', expected '{norm_expected.get(key)}'"
            )

    if differences:
        return False, "Differences found: " + "; ".join(differences)

    return True, "Solutions are equivalent."
