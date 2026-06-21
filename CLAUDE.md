# O'Reilly Reasoning Models Course

Course on reasoning models: building the DeepSeek R1-style training pipeline from scratch, plus OpenAI reasoning-model demo apps. Anthropic Claude extended thinking is covered conceptually in the slides.

## Structure

```
notebooks/           # Jupyter notebooks — the R1-style pipeline, built from scratch
├── 00_setup_check.ipynb                  # Verify environment and API keys
├── 01_chain_of_thought_intuition.ipynb   # What CoT is and why it works
├── 02_stage1_pretraining.ipynb           # Stage 1: base-model pretraining
├── 03_stage2_cold_start_sft.ipynb        # Stage 2: cold-start supervised fine-tuning
├── 04_stage3_rl_grpo_from_scratch.ipynb  # Stage 3: GRPO RL implemented from scratch
├── 05_stage4_rejection_sampling_sft.ipynb # Stage 4: rejection-sampling SFT
└── 06_stage5_distillation.ipynb          # Stage 5: distillation into smaller students
# Checkpoints: cold_start.pt, after_grpo.pt, after_reject_sft.pt

presentation/        # Slide decks (markdown sources + rendered PDFs)
scripts/             # Demo apps (app1_math_comparator, app2_logic_solver, app3_planning_agent) + reasoning_model_selector.py
requirements/        # Dependencies
```

## Key APIs

**OpenAI (Responses API)**
```python
client.responses.create(
    model="gpt-5.5",
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
