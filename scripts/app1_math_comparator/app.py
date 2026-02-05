"""
Math Reasoning Comparator - Side-by-side comparison of standard vs reasoning LLMs.

Compares GPT-5.2 with reasoning=none (standard) against GPT-5.2 with reasoning=high,
showing the thinking process and performance metrics.

Uses the OpenAI Responses API for optimal reasoning model performance.
"""

import time
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from problems import (
    get_problems_by_difficulty,
    get_difficulty_levels,
    format_problem_for_display,
    MATH_PROBLEMS,
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Math Reasoning Comparator",
    page_icon="🧮",
    layout="wide",
)

# Custom CSS for clean UI
st.markdown("""
<style>
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .success-badge {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: bold;
    }
    .error-badge {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: bold;
    }
    div[data-testid="stHorizontalBlock"] > div {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)


def init_client():
    """Initialize OpenAI client."""
    return OpenAI()


def call_standard_model(client: OpenAI, problem: str) -> dict:
    """
    Call GPT-5.2 with reasoning effort=none (fast, pattern-based response).

    Uses the Responses API for consistency with the reasoning model.
    Returns dict with: answer, tokens, latency, thinking
    """
    start_time = time.time()

    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": "none"},
        input=[
            {
                "role": "developer",
                "content": "You are a math tutor. Solve the problem and provide your final answer clearly. Format your final answer as 'Final Answer: [number]'"
            },
            {
                "role": "user",
                "content": f"Solve this math problem and give the final answer.\n\nProblem: {problem}"
            }
        ],
    )

    latency = time.time() - start_time

    return {
        "answer": response.output_text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        "latency": latency,
        "thinking": None,  # No reasoning with effort=none
    }


def call_reasoning_model(client: OpenAI, problem: str, effort: str = "high") -> dict:
    """
    Call GPT-5.2 with reasoning effort enabled (slower, with chain-of-thought).

    Uses the Responses API with reasoning summary to expose the thinking process.
    Reasoning models perform better without "think step by step" instructions.

    Returns dict with: answer, tokens, latency, thinking, reasoning_tokens
    """
    start_time = time.time()

    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": effort, "summary": "auto"},
        input=[
            {
                "role": "user",
                "content": f"Solve this math problem. Provide your final answer as 'Final Answer: [number]'\n\nProblem: {problem}"
            }
        ],
    )

    latency = time.time() - start_time

    # Extract reasoning summary from response.output
    thinking = None
    for item in response.output:
        if item.type == "reasoning" and hasattr(item, "summary") and item.summary:
            thinking = "\n".join(s.text for s in item.summary if hasattr(s, "text"))
            break

    # Get reasoning tokens if available
    reasoning_tokens = 0
    if hasattr(response.usage, "output_tokens_details") and response.usage.output_tokens_details:
        reasoning_tokens = getattr(response.usage.output_tokens_details, "reasoning_tokens", 0)

    return {
        "answer": response.output_text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "latency": latency,
        "thinking": thinking,
    }


def extract_final_answer(response_text: str) -> str:
    """Extract the final numerical answer from model response."""
    import re

    # Try to find "Final Answer: X" pattern
    match = re.search(r'Final Answer:\s*[\$]?([+-]?\d+(?:,\d{3})*(?:\.\d+)?)', response_text, re.IGNORECASE)
    if match:
        return match.group(1).replace(',', '')

    # Try to find boxed answer (common in math)
    match = re.search(r'\\boxed\{([^}]+)\}', response_text)
    if match:
        return match.group(1).strip()

    # Try to find the last number in the response
    numbers = re.findall(r'[\$]?([+-]?\d+(?:,\d{3})*(?:\.\d+)?)', response_text)
    if numbers:
        return numbers[-1].replace(',', '')

    return "N/A"


def check_correctness(model_answer: str, expected_answer: str) -> bool:
    """Check if the model's answer matches the expected answer."""
    try:
        # Normalize both answers
        model_num = float(model_answer.replace(',', '').strip())
        expected_num = float(expected_answer.replace(',', '').strip())
        return abs(model_num - expected_num) < 0.001
    except (ValueError, AttributeError):
        # Fall back to string comparison
        return model_answer.strip().lower() == expected_answer.strip().lower()


def run_comparison(client: OpenAI, problem: str, reasoning_effort: str = "high") -> tuple:
    """Run both models in parallel using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        standard_future = executor.submit(call_standard_model, client, problem)
        reasoning_future = executor.submit(call_reasoning_model, client, problem, reasoning_effort)

        standard_result = standard_future.result()
        reasoning_result = reasoning_future.result()

    return standard_result, reasoning_result


def display_result_panel(title: str, result: dict, expected_answer: str, show_thinking: bool = False):
    """Display a result panel with metrics and correctness badge."""
    st.subheader(title)

    # Display the answer
    st.markdown("**Response:**")
    st.markdown(result["answer"])

    # Show thinking process if available
    if show_thinking and result.get("thinking"):
        with st.expander("Show Reasoning Process", expanded=False):
            st.markdown(result["thinking"])
    elif show_thinking and not result.get("thinking"):
        with st.expander("Show Reasoning Process", expanded=False):
            st.info("Reasoning trace not available for this model/response.")

    # Extract and check answer
    extracted = extract_final_answer(result["answer"])
    is_correct = check_correctness(extracted, expected_answer)

    st.markdown("---")

    # Metrics row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Latency", f"{result['latency']:.2f}s")

    with col2:
        st.metric("Total Tokens", result['total_tokens'])

    with col3:
        if is_correct:
            st.success(f"Correct")
        else:
            st.error(f"Incorrect")

    # Show extracted answer
    st.caption(f"Extracted answer: {extracted} | Expected: {expected_answer}")


def main():
    st.title("Math Reasoning Comparator")
    st.markdown("Compare how standard and reasoning LLMs approach math problems side-by-side.")

    # Initialize client
    try:
        client = init_client()
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client. Make sure OPENAI_API_KEY is set in your .env file.")
        st.stop()

    # Sidebar
    st.sidebar.header("Settings")

    # Model info
    st.sidebar.markdown("**Model:** `gpt-5.2`")
    st.sidebar.markdown("**Comparison:**")
    st.sidebar.markdown("- Standard: `reasoning.effort=none`")
    st.sidebar.markdown("- Reasoning: `reasoning.effort=high`")
    st.sidebar.markdown("---")

    # Reasoning effort selector for the reasoning model
    reasoning_effort = st.sidebar.select_slider(
        "Reasoning Effort",
        options=["low", "medium", "high", "xhigh"],
        value="high",
        help="Controls how much 'thinking' the reasoning model does"
    )
    st.sidebar.markdown("---")

    # Difficulty filter
    difficulty = st.sidebar.selectbox(
        "Filter by Difficulty",
        options=get_difficulty_levels(),
        index=0,
        help="Filter preset problems by difficulty level"
    )

    # Get filtered problems
    filtered_problems = get_problems_by_difficulty(difficulty)

    # Problem selection
    st.markdown("### Select or Enter a Problem")

    input_method = st.radio(
        "Input method:",
        ["Select preset problem", "Enter custom problem"],
        horizontal=True
    )

    problem_text = ""
    expected_answer = ""

    if input_method == "Select preset problem":
        # Create options for selectbox
        problem_options = {format_problem_for_display(p): p for p in filtered_problems}

        selected_display = st.selectbox(
            "Choose a problem:",
            options=list(problem_options.keys()),
        )

        if selected_display:
            selected_problem = problem_options[selected_display]
            problem_text = selected_problem["question"]
            expected_answer = selected_problem["answer"]

            # Show full problem text
            st.info(f"**Problem:** {problem_text}")
            st.caption(f"Difficulty: {selected_problem['difficulty'].title()} | Expected answer: {expected_answer}")

    else:
        problem_text = st.text_area(
            "Enter your math problem:",
            height=100,
            placeholder="e.g., What is the sum of all prime numbers less than 20?"
        )
        expected_answer = st.text_input(
            "Expected answer (for correctness check):",
            placeholder="e.g., 77"
        )

    # Compare button
    if st.button("Compare Models", type="primary", disabled=not problem_text):
        if not problem_text:
            st.warning("Please enter or select a problem first.")
            return

        with st.spinner(f"Running both models in parallel (reasoning effort: {reasoning_effort})..."):
            try:
                standard_result, reasoning_result = run_comparison(client, problem_text, reasoning_effort)
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
                return

        # Display results side by side
        st.markdown("---")
        st.markdown("### Results")

        col1, col2 = st.columns(2)

        with col1:
            display_result_panel(
                "Standard Mode (effort=none)",
                standard_result,
                expected_answer,
                show_thinking=False
            )

        with col2:
            display_result_panel(
                f"Reasoning Mode (effort={reasoning_effort})",
                reasoning_result,
                expected_answer,
                show_thinking=True
            )

        # Summary comparison
        st.markdown("---")
        st.markdown("### Performance Comparison")

        comparison_data = {
            "Metric": ["Latency (s)", "Input Tokens", "Output Tokens", "Reasoning Tokens", "Total Tokens"],
            "Standard (effort=none)": [
                f"{standard_result['latency']:.2f}",
                standard_result['input_tokens'],
                standard_result['output_tokens'],
                "N/A",
                standard_result['total_tokens'],
            ],
            f"Reasoning (effort={reasoning_effort})": [
                f"{reasoning_result['latency']:.2f}",
                reasoning_result['input_tokens'],
                reasoning_result['output_tokens'],
                reasoning_result.get('reasoning_tokens', 'N/A'),
                reasoning_result['total_tokens'],
            ],
        }

        st.table(comparison_data)

    # Footer
    st.markdown("---")
    st.caption("Built for O'Reilly Reasoning Models Course | Comparing standard vs reasoning LLM approaches")


if __name__ == "__main__":
    main()
