# Math Reasoning Comparator

A Streamlit app that compares low vs high reasoning effort on math problems side-by-side.

## Features

- Dual-panel display comparing GPT-5.5 with reasoning effort `none` (fast, standard) vs GPT-5.5 with reasoning effort `high` (thorough, chain-of-thought)
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

Both panels use **GPT-5.5** via the Responses API, differing only in reasoning effort:

- **Standard (fast)**: GPT-5.5 with `reasoning.effort = none` - no chain-of-thought, pattern-based answer
- **Reasoning (thorough)**: GPT-5.5 with `reasoning.effort = high` - explicit chain-of-thought thinking process
