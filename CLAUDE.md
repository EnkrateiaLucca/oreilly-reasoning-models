# O'Reilly Reasoning Models Course

Course on OpenAI GPT-5.2 and Anthropic Claude reasoning capabilities.

## Structure

```
notebooks/           # Jupyter notebooks (main content)
├── openai-thinking-parameters.ipynb    # GPT-5.2 Responses API, reasoning effort levels
├── anthropic-extended-thinking.ipynb   # Claude budget_tokens, streaming, interleaved thinking
├── gpt-5.2-prompting-guide.ipynb       # GPT-5.2 prompting techniques (verbosity, scope, extraction)
├── analytical-framework.ipynb          # LLM-as-Judge evaluation framework
└── assets-resources/                   # Reference PDFs, images

presentation/        # Slides
scripts/             # Utility scripts (comparison charts, decision trees)
requirements/        # Dependencies
```

## Key APIs

**OpenAI (Responses API)**
```python
client.responses.create(
    model="gpt-5.2",
    reasoning={"effort": "medium"},  # none/low/medium/high/xhigh
    input=[{"role": "developer", "content": "..."}, {"role": "user", "content": "..."}]
)
```

**Anthropic (Extended Thinking)**
```python
client.messages.create(
    model="claude-sonnet-4-5-20250514",
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[...]
)
```

## Run

```bash
# Setup
uv venv .venv && uv pip install -r requirements/requirements.txt

# API keys in .env
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

## Conventions

- Notebooks use `dotenv` for API keys
- Code cells include print statements with `-` * 60 dividers
- Tables for parameter comparisons
- Pydantic for structured outputs
