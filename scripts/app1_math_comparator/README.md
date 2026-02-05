# Math Reasoning Comparator

A Streamlit app that compares standard vs reasoning LLMs on math problems side-by-side.

## Features

- Dual-panel display comparing GPT-4o (standard) vs o3-mini (reasoning)
- Pre-loaded math problems across three difficulty levels
- Custom problem input support
- Real-time streaming responses
- Chain-of-thought visualization for reasoning model
- Token count and latency metrics
- Correctness verification

## Setup

1. Create a virtual environment and install dependencies:

```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

2. Copy the example environment file and add your API key:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. Run the app:

```bash
streamlit run app.py
```

## Usage

1. Select difficulty filter in the sidebar (or "all" for all problems)
2. Choose a preset problem from the dropdown OR enter a custom problem
3. Click "Compare Models" to see both models solve the problem
4. Expand "Show Reasoning Process" to see the reasoning model's chain-of-thought
5. Compare token usage, latency, and correctness between models

## Models Used

- **Standard Model**: GPT-4o - Fast, capable general-purpose model
- **Reasoning Model**: o3-mini - Specialized reasoning model with explicit thinking process
