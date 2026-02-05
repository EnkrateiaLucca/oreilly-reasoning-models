# Multi-Step Planning Agent

A Streamlit app that uses OpenAI's reasoning models to generate structured plans with AI-powered self-critique.

## Features

- **Two-Pass Generation**: First generates a structured plan, then critically reviews it
- **Dependency Tracking**: Steps include dependencies visualized in a Mermaid flowchart
- **Chain-of-Thought**: View the model's reasoning process for both planning and critique
- **Preset Examples**: Quick-start with common planning scenarios
- **Export Options**: Download plans as Markdown or JSON

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy the environment template and add your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select a preset goal from the sidebar or enter a custom goal
2. Adjust the reasoning effort level (higher = more thorough)
3. Click "Generate Plan" to create the plan
4. Review the plan, critique, and dependency graph in the tabs
5. Export the results as Markdown or JSON

## Files

- `app.py` - Main Streamlit application
- `schemas.py` - Pydantic models for Plan, Step, and Critique
- `prompts.py` - System prompts for planner and critic
- `requirements.txt` - Python dependencies
