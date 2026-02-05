"""
Multi-Step Planning Agent with Self-Critique

A Streamlit app that uses OpenAI's reasoning models to:
1. Generate structured plans from goals
2. Critically review plans and suggest improvements
3. Visualize dependencies with Mermaid flowcharts
"""

import json
import os
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from schemas import Plan, Critique, Step
from prompts import get_planner_prompt, get_critic_prompt, PRESET_GOALS

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Step Planning Agent",
    page_icon="📋",
    layout="wide"
)

# Initialize OpenAI client
@st.cache_resource
def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_plan_schema_json() -> str:
    """Get the Plan schema as formatted JSON string."""
    return json.dumps(Plan.model_json_schema(), indent=2)


def get_critique_schema_json() -> str:
    """Get the Critique schema as formatted JSON string."""
    return json.dumps(Critique.model_json_schema(), indent=2)


def generate_plan(client: OpenAI, goal: str, model: str, effort: str) -> tuple[Optional[Plan], str, str]:
    """
    Generate a structured plan for the given goal using GPT-5.2 with reasoning.

    Returns:
        Tuple of (Plan object or None, raw response, thinking content)
    """
    schema_json = get_plan_schema_json()
    system_prompt = get_planner_prompt(schema_json)

    try:
        response = client.responses.create(
            model=model,
            reasoning={"effort": effort, "summary": "auto"},
            input=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": f"Create a detailed plan for this goal: {goal}"}
            ]
        )

        # Extract thinking from reasoning items
        thinking_content = ""
        for item in response.output:
            if item.type == "reasoning" and hasattr(item, 'summary') and item.summary:
                thinking_content = "\n".join(
                    s.text for s in item.summary if hasattr(s, 'text')
                )
                break

        # Get the response content using the helper
        response_content = response.output_text

        # Parse the JSON response
        try:
            # Clean up response if needed
            json_str = response_content.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()

            plan_data = json.loads(json_str)
            plan = Plan.model_validate(plan_data)
            return plan, response_content, thinking_content
        except (json.JSONDecodeError, ValidationError) as e:
            st.error(f"Failed to parse plan: {e}")
            return None, response_content, thinking_content

    except Exception as e:
        st.error(f"API error: {e}")
        return None, "", ""


def generate_critique(client: OpenAI, plan: Plan, model: str, effort: str) -> tuple[Optional[Critique], str, str]:
    """
    Generate a critique of the given plan using GPT-5.2 with reasoning.

    Returns:
        Tuple of (Critique object or None, raw response, thinking content)
    """
    plan_json = plan.model_dump_json(indent=2)
    critique_schema = get_critique_schema_json()
    system_prompt = get_critic_prompt(plan_json, critique_schema)

    try:
        response = client.responses.create(
            model=model,
            reasoning={"effort": effort, "summary": "auto"},
            input=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": "Please review this plan and provide your critique."}
            ]
        )

        # Extract thinking from reasoning items
        thinking_content = ""
        for item in response.output:
            if item.type == "reasoning" and hasattr(item, 'summary') and item.summary:
                thinking_content = "\n".join(
                    s.text for s in item.summary if hasattr(s, 'text')
                )
                break

        # Get the response content using the helper
        response_content = response.output_text

        # Parse the JSON response
        try:
            json_str = response_content.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()

            critique_data = json.loads(json_str)
            critique = Critique.model_validate(critique_data)
            return critique, response_content, thinking_content
        except (json.JSONDecodeError, ValidationError) as e:
            st.error(f"Failed to parse critique: {e}")
            return None, response_content, thinking_content

    except Exception as e:
        st.error(f"API error: {e}")
        return None, "", ""


def render_plan(plan: Plan):
    """Render the plan as a numbered list with dependency badges."""
    st.subheader(f"Plan: {plan.goal}")
    st.caption(f"Total estimated time: {plan.total_estimated_minutes} minutes")

    # Category colors
    category_colors = {
        "research": "blue",
        "execution": "green",
        "review": "orange"
    }

    for step in plan.steps:
        col1, col2 = st.columns([4, 1])

        with col1:
            # Step title and description
            st.markdown(f"**{step.number}. {step.title}**")
            st.markdown(f"_{step.description}_")

            # Dependency badges
            badges = []
            if step.depends_on:
                deps = ", ".join(f"Step {d}" for d in step.depends_on)
                badges.append(f"Depends on: {deps}")

            # Category badge
            color = category_colors.get(step.category, "gray")
            badges.append(f":{color}[{step.category.upper()}]")

            st.markdown(" | ".join(badges))

        with col2:
            st.metric("Time", f"{step.estimated_minutes} min")

        st.divider()


def render_critique(critique: Critique):
    """Render the critique as warning/info callouts."""
    st.subheader("Plan Critique")

    # Gaps
    if critique.gaps:
        st.warning("**Identified Gaps**")
        for gap in critique.gaps:
            st.markdown(f"- {gap}")

    # Risks
    if critique.risks:
        st.error("**Potential Risks**")
        for risk in critique.risks:
            st.markdown(f"- {risk}")

    # Improvements
    if critique.suggested_improvements:
        st.info("**Suggested Improvements**")
        for improvement in critique.suggested_improvements:
            st.markdown(f"- {improvement}")


def generate_mermaid_flowchart(plan: Plan) -> str:
    """Generate a Mermaid flowchart showing step dependencies."""
    lines = ["graph TD"]

    # Define nodes
    for step in plan.steps:
        # Truncate title if too long
        title = step.title[:30] + "..." if len(step.title) > 30 else step.title
        lines.append(f"    S{step.number}[{step.number}. {title}]")

    # Define edges based on dependencies
    for step in plan.steps:
        if step.depends_on:
            for dep in step.depends_on:
                lines.append(f"    S{dep} --> S{step.number}")
        elif step.number > 1:
            # If no explicit dependencies, check if it should follow the previous step
            # Only add implicit edge if previous step isn't already a dependency
            pass  # Let dependencies be explicit only

    # Style by category
    category_styles = {
        "research": "fill:#e3f2fd,stroke:#1976d2",
        "execution": "fill:#e8f5e9,stroke:#388e3c",
        "review": "fill:#fff3e0,stroke:#f57c00"
    }

    for step in plan.steps:
        style = category_styles.get(step.category, "fill:#f5f5f5,stroke:#9e9e9e")
        lines.append(f"    style S{step.number} {style}")

    return "\n".join(lines)


def export_as_markdown(plan: Plan, critique: Optional[Critique] = None) -> str:
    """Export the plan (and optionally critique) as Markdown."""
    md = f"# Plan: {plan.goal}\n\n"
    md += f"**Total Estimated Time:** {plan.total_estimated_minutes} minutes\n\n"
    md += "## Steps\n\n"

    for step in plan.steps:
        md += f"### {step.number}. {step.title}\n\n"
        md += f"{step.description}\n\n"
        md += f"- **Category:** {step.category}\n"
        md += f"- **Estimated Time:** {step.estimated_minutes} minutes\n"
        if step.depends_on:
            deps = ", ".join(str(d) for d in step.depends_on)
            md += f"- **Depends On:** Steps {deps}\n"
        md += "\n"

    if critique:
        md += "## Critique\n\n"
        if critique.gaps:
            md += "### Gaps\n\n"
            for gap in critique.gaps:
                md += f"- {gap}\n"
            md += "\n"
        if critique.risks:
            md += "### Risks\n\n"
            for risk in critique.risks:
                md += f"- {risk}\n"
            md += "\n"
        if critique.suggested_improvements:
            md += "### Suggested Improvements\n\n"
            for improvement in critique.suggested_improvements:
                md += f"- {improvement}\n"
            md += "\n"

    return md


def export_as_json(plan: Plan, critique: Optional[Critique] = None) -> str:
    """Export the plan (and optionally critique) as JSON."""
    data = {"plan": plan.model_dump()}
    if critique:
        data["critique"] = critique.model_dump()
    return json.dumps(data, indent=2)


def main():
    st.title("Multi-Step Planning Agent")
    st.markdown("Generate structured plans with AI-powered self-critique")

    client = get_client()

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")

        # Model selector (GPT-5.2 only for reasoning)
        model = st.selectbox(
            "Model",
            ["gpt-5.2"],
            index=0,
            help="GPT-5.2 with adaptive reasoning"
        )

        # Reasoning effort
        effort = st.select_slider(
            "Reasoning Effort",
            options=["none", "low", "medium", "high", "xhigh"],
            value="medium",
            help="Controls how much 'thinking' the model does (none=fastest, xhigh=most thorough)"
        )

        st.divider()

        # Preset examples
        st.header("Preset Examples")
        selected_preset = st.selectbox(
            "Choose a preset goal",
            ["Custom"] + list(PRESET_GOALS.keys())
        )

        if selected_preset != "Custom":
            st.info(PRESET_GOALS[selected_preset])

    # Main area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Goal input
        if selected_preset != "Custom":
            default_goal = PRESET_GOALS[selected_preset]
        else:
            default_goal = ""

        goal = st.text_area(
            "Enter your goal",
            value=default_goal,
            height=100,
            placeholder="Describe what you want to plan..."
        )

    with col2:
        st.markdown("###")  # Spacing
        generate_button = st.button(
            "Generate Plan",
            type="primary",
            use_container_width=True,
            disabled=not goal.strip()
        )

    # Generate plan and critique
    if generate_button and goal.strip():
        # Initialize session state for results
        st.session_state.plan = None
        st.session_state.critique = None
        st.session_state.plan_thinking = ""
        st.session_state.critique_thinking = ""

        # Pass 1: Generate Plan
        with st.spinner("Generating plan..."):
            plan, plan_raw, plan_thinking = generate_plan(client, goal, model, effort)
            if plan:
                st.session_state.plan = plan
                st.session_state.plan_thinking = plan_thinking

        # Pass 2: Generate Critique (if plan succeeded)
        if st.session_state.plan:
            with st.spinner("Analyzing plan..."):
                critique, critique_raw, critique_thinking = generate_critique(
                    client, st.session_state.plan, model, effort
                )
                if critique:
                    st.session_state.critique = critique
                    st.session_state.critique_thinking = critique_thinking

    # Display results if available
    if hasattr(st.session_state, 'plan') and st.session_state.plan:
        plan = st.session_state.plan
        critique = getattr(st.session_state, 'critique', None)

        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs([
            "Plan", "Critique", "Dependency Graph", "Export"
        ])

        with tab1:
            render_plan(plan)

            # Chain-of-thought for planning
            if st.session_state.plan_thinking:
                with st.expander("View Planning Chain-of-Thought"):
                    st.markdown(st.session_state.plan_thinking)

        with tab2:
            if critique:
                render_critique(critique)

                # Chain-of-thought for critique
                if st.session_state.critique_thinking:
                    with st.expander("View Critique Chain-of-Thought"):
                        st.markdown(st.session_state.critique_thinking)
            else:
                st.info("No critique available")

        with tab3:
            st.subheader("Dependency Flowchart")
            mermaid_code = generate_mermaid_flowchart(plan)

            # Display Mermaid diagram using st.markdown with mermaid code block
            st.markdown(f"""
```mermaid
{mermaid_code}
```
            """)

            # Also show the raw Mermaid code
            with st.expander("View Mermaid Code"):
                st.code(mermaid_code, language="mermaid")

        with tab4:
            st.subheader("Export Plan")

            col1, col2 = st.columns(2)

            with col1:
                md_content = export_as_markdown(plan, critique)
                st.download_button(
                    "Download as Markdown",
                    md_content,
                    file_name="plan.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                with st.expander("Preview Markdown"):
                    st.code(md_content, language="markdown")

            with col2:
                json_content = export_as_json(plan, critique)
                st.download_button(
                    "Download as JSON",
                    json_content,
                    file_name="plan.json",
                    mime="application/json",
                    use_container_width=True
                )
                with st.expander("Preview JSON"):
                    st.code(json_content, language="json")


if __name__ == "__main__":
    main()
