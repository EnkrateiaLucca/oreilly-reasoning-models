"""
Logic Puzzle Solver & Explainer
A Streamlit app that solves logic puzzles with visible chain-of-thought reasoning.
Uses OpenAI's GPT-5.2 with reasoning effort via the Responses API.
"""

import json
import time
import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

from puzzles import PUZZLES, get_puzzle, list_puzzles
from verifier import verify, compare_with_expected, VerificationResult

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Logic Puzzle Solver",
    page_icon="🧩",
    layout="wide",
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI()


class PuzzleSolution(BaseModel):
    """Structured output for puzzle solutions."""

    reasoning_steps: list[str]
    solution: dict
    confidence: str  # "high", "medium", "low"


def create_system_prompt() -> str:
    """Create the system prompt for the reasoning model."""
    return """You are an expert logic puzzle solver. Your task is to solve logic puzzles by carefully analyzing each clue and making deductions.

APPROACH:
1. Read all clues carefully first
2. Identify what entities and attributes need to be matched
3. Start with the most constraining clues (those that directly assign values)
4. Use process of elimination
5. Track your deductions at each step
6. Verify your solution against all clues before finalizing

OUTPUT FORMAT:
You must respond with a valid JSON object containing:
{
    "reasoning_steps": [
        "Step 1: <your first deduction>",
        "Step 2: <your second deduction>",
        ...
    ],
    "solution": {
        // The solution mapping entities to their attributes
        // Format depends on puzzle type
    },
    "confidence": "high" | "medium" | "low"
}

Be thorough in your reasoning. Show your work at each step."""


def create_user_prompt(puzzle: dict) -> str:
    """Create the user prompt with the puzzle details."""
    clues_text = "\n".join([f"{i+1}. {clue}" for i, clue in enumerate(puzzle["clues"])])

    return f"""Please solve the following logic puzzle:

**{puzzle['title']}**

{puzzle['description']}

**Clues:**
{clues_text}

Solve this puzzle step by step, showing your reasoning for each deduction. Then provide your final solution as a JSON object."""


def solve_puzzle(puzzle: dict, reasoning_effort: str = "high") -> tuple[dict, str, float, dict]:
    """
    Solve a puzzle using GPT-5.2 with reasoning effort.

    Returns:
        Tuple of (solution_dict, reasoning_text, solve_time, usage_info)
    """
    client = get_openai_client()

    system_prompt = create_system_prompt()
    user_prompt = create_user_prompt(puzzle)

    start_time = time.time()

    # Use GPT-5.2 with reasoning effort and summary
    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": reasoning_effort, "summary": "auto"},
        input=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    )

    solve_time = time.time() - start_time

    # Extract reasoning summary from response.output
    reasoning_text = ""
    for item in response.output:
        if item.type == "reasoning" and hasattr(item, "summary") and item.summary:
            reasoning_text = "\n".join(s.text for s in item.summary if hasattr(s, "text"))
            break

    # Get the output text using the helper
    output_text = response.output_text

    # Parse the JSON response
    try:
        # Try to extract JSON from the response
        json_start = output_text.find("{")
        json_end = output_text.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            json_str = output_text[json_start:json_end]
            result = json.loads(json_str)
        else:
            result = {"solution": {}, "reasoning_steps": [], "confidence": "low"}
    except json.JSONDecodeError:
        result = {"solution": {}, "reasoning_steps": ["Failed to parse response"], "confidence": "low"}

    # Build usage info
    reasoning_tokens = 0
    if hasattr(response.usage, "output_tokens_details") and response.usage.output_tokens_details:
        reasoning_tokens = getattr(response.usage.output_tokens_details, "reasoning_tokens", 0)

    usage_info = {
        "input_tokens": response.usage.input_tokens if response.usage else 0,
        "output_tokens": response.usage.output_tokens if response.usage else 0,
        "reasoning_tokens": reasoning_tokens,
    }

    return result, reasoning_text, solve_time, usage_info


def display_verification_results(verification: VerificationResult):
    """Display verification results with checkmarks."""
    st.subheader("Constraint Verification")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clues", verification.total_clues)
    with col2:
        st.metric("Passed", verification.passed_clues, delta=None)
    with col3:
        if verification.all_passed:
            st.success("All Constraints Satisfied!")
        else:
            st.error(f"{verification.failed_clues} constraint(s) failed")

    # Detailed results
    st.write("---")
    for detail in verification.details:
        icon = "✅" if detail.passed else "❌"
        with st.expander(f"{icon} {detail.clue}", expanded=not detail.passed):
            st.write(detail.explanation)


def display_difficulty_chart(puzzle: dict, solve_time: float, usage_info: dict):
    """Display a difficulty scaling visualization."""
    import plotly.graph_objects as go

    # Difficulty metrics
    difficulty_scores = {"easy": 1, "medium": 2, "hard": 3}
    clue_count = len(puzzle["clues"])

    # Create radar chart
    categories = ["Difficulty", "Clue Count", "Solve Time (s)", "Reasoning Tokens (k)"]

    # Normalize values for visualization
    values = [
        difficulty_scores.get(puzzle["difficulty"], 1) / 3 * 100,
        min(clue_count / 15 * 100, 100),
        min(solve_time / 60 * 100, 100),
        min(usage_info.get("reasoning_tokens", 0) / 10000 * 100, 100),
    ]
    values.append(values[0])  # Close the polygon
    categories.append(categories[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Puzzle Complexity'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title="Puzzle Complexity Profile",
        height=300,
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("Logic Puzzle Solver & Explainer")
    st.markdown("*Powered by OpenAI GPT-5.2 with reasoning capabilities*")

    # Sidebar
    st.sidebar.header("Puzzle Selection")

    # Mode selection
    mode = st.sidebar.radio("Mode", ["Pre-loaded Puzzles", "Custom Puzzle"])

    # Reasoning effort selector
    reasoning_effort = st.sidebar.select_slider(
        "Reasoning Effort",
        options=["none", "low", "medium", "high", "xhigh"],
        value="high",
        help="Controls how much 'thinking' GPT-5.2 does (none=fastest, xhigh=most thorough)"
    )

    puzzle = None

    if mode == "Pre-loaded Puzzles":
        # Group puzzles by difficulty
        st.sidebar.subheader("Select a Puzzle")

        difficulty_filter = st.sidebar.selectbox(
            "Filter by Difficulty",
            ["All", "Easy", "Medium", "Hard"]
        )

        puzzle_list = list_puzzles()
        if difficulty_filter != "All":
            puzzle_list = [p for p in puzzle_list if p["difficulty"] == difficulty_filter.lower()]

        puzzle_options = {f"{p['title']} ({p['difficulty']}, {p['clue_count']} clues)": p['id'] for p in puzzle_list}

        if puzzle_options:
            selected = st.sidebar.selectbox("Choose puzzle", list(puzzle_options.keys()))
            puzzle_id = puzzle_options[selected]
            puzzle = get_puzzle(puzzle_id)
        else:
            st.sidebar.warning("No puzzles match the filter.")

    else:  # Custom Puzzle mode
        st.sidebar.subheader("Enter Custom Puzzle")

        custom_title = st.sidebar.text_input("Puzzle Title", "My Custom Puzzle")
        custom_description = st.sidebar.text_area(
            "Description",
            "Describe what needs to be solved...",
            height=100
        )
        custom_clues = st.sidebar.text_area(
            "Clues (one per line)",
            "Clue 1\nClue 2\nClue 3",
            height=150
        )
        custom_difficulty = st.sidebar.selectbox("Difficulty", ["easy", "medium", "hard"])

        if custom_title and custom_description and custom_clues:
            puzzle = {
                "title": custom_title,
                "description": custom_description,
                "clues": [c.strip() for c in custom_clues.split("\n") if c.strip()],
                "solution": None,  # No expected solution for custom puzzles
                "difficulty": custom_difficulty,
                "puzzle_type": "custom",
            }

    # Main content area
    if puzzle:
        # Display puzzle
        st.header(puzzle["title"])

        # Difficulty badge
        difficulty_colors = {"easy": "green", "medium": "orange", "hard": "red"}
        st.markdown(
            f"**Difficulty:** :{difficulty_colors.get(puzzle['difficulty'], 'blue')}[{puzzle['difficulty'].upper()}] | "
            f"**Clues:** {len(puzzle['clues'])}"
        )

        st.markdown("---")
        st.subheader("Puzzle Description")
        st.write(puzzle["description"])

        st.subheader("Clues")
        for i, clue in enumerate(puzzle["clues"], 1):
            st.write(f"{i}. {clue}")

        st.markdown("---")

        # Solve button
        if st.button("Solve Puzzle", type="primary", use_container_width=True):
            with st.spinner(f"Solving with {reasoning_effort} reasoning effort..."):
                result, reasoning_text, solve_time, usage_info = solve_puzzle(puzzle, reasoning_effort)

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Solution")
                st.json(result.get("solution", {}))

                # Confidence
                confidence = result.get("confidence", "unknown")
                confidence_colors = {"high": "green", "medium": "orange", "low": "red"}
                st.markdown(f"**Model Confidence:** :{confidence_colors.get(confidence, 'blue')}[{confidence.upper()}]")

                # Compare with expected if available
                if puzzle.get("solution"):
                    matches, explanation = compare_with_expected(
                        result.get("solution", {}),
                        puzzle["solution"]
                    )
                    if matches:
                        st.success("Solution matches expected answer!")
                    else:
                        st.warning(f"Solution differs from expected: {explanation}")

            with col2:
                st.subheader("Performance Metrics")
                st.metric("Solve Time", f"{solve_time:.2f}s")
                st.metric("Input Tokens", usage_info.get("input_tokens", 0))
                st.metric("Output Tokens", usage_info.get("output_tokens", 0))
                st.metric("Reasoning Tokens", usage_info.get("reasoning_tokens", 0))

            # Chain of thought reasoning
            st.subheader("Chain-of-Thought Reasoning")

            # Model's reasoning summary
            if reasoning_text:
                with st.expander("Model's Internal Reasoning (Summary)", expanded=False):
                    st.write(reasoning_text)

            # Structured reasoning steps
            with st.expander("Step-by-Step Deductions", expanded=True):
                reasoning_steps = result.get("reasoning_steps", [])
                if reasoning_steps:
                    for step in reasoning_steps:
                        st.write(f"- {step}")
                else:
                    st.write("No structured reasoning steps provided.")

            # Verification
            st.markdown("---")
            with st.spinner("Verifying solution against constraints..."):
                client = get_openai_client()
                verification = verify(
                    result.get("solution", {}),
                    puzzle["clues"],
                    puzzle.get("puzzle_type", "custom"),
                    puzzle["description"],
                    client
                )

            display_verification_results(verification)

            # Difficulty chart
            st.markdown("---")
            try:
                display_difficulty_chart(puzzle, solve_time, usage_info)
            except ImportError:
                st.info("Install plotly for difficulty visualization: pip install plotly")

    else:
        st.info("Select a puzzle from the sidebar or create a custom puzzle to get started.")

    # Footer
    st.markdown("---")
    st.caption(
        "Built with Streamlit and OpenAI GPT-5.2 | "
        "Part of the O'Reilly Reasoning Models Course"
    )


if __name__ == "__main__":
    main()
