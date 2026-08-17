# O'Reilly Reasoning Models Course

Course on reasoning models: building the DeepSeek R1-style training pipeline from scratch, plus OpenAI reasoning-model demo apps. Anthropic Claude extended thinking is covered conceptually in the slides.

## Structure

```
notebooks/           # Jupyter notebooks — the R1-style pipeline + the practical workflow
├── 00_setup_check.ipynb                                          # Verify environment and API keys
├── 01_build_a_reasoning_model_r1_from_scratch.ipynb             # Full R1 pipeline in the paper's sequence: foundations → base → R1-Zero → cold-start SFT → GRPO → rejection-SFT → distillation
├── 02_reproducibility_cheap_vs_flagship.ipynb                   # Practical "working with reasoning models": cheap-vs-flagship + real engineer workflow (mock mode w/o keys)
├── provider_anthropic_extended_thinking.ipynb                    # Provider deep-dive: Claude extended/adaptive thinking, hands-on
└── provider_openai_thinking_parameters.ipynb                     # Provider deep-dive: OpenAI reasoning-effort parameters, hands-on
# Checkpoints (written by nb01, not committed): nb2_r1_zero.pt, nb2_cold_start.pt, nb2_after_grpo.pt, nb3_after_reject_sft.pt, nb3_student.pt
# Earlier single-stage + consolidated notebooks (and the old model bake-off) preserved under notebooks/archive/

guide/               # Interactive HTML artifacts: reasoning-training-guide.html (paper walkthrough), training-overlay.html
research/            # Sourced research notes behind the deck (when-to-use, selection criteria, prompting, practical API workflow)
presentation/        # Remark.js slide deck (presentation.html) + rendered PDF
scripts/             # Demo apps (app1_math_comparator, app2_logic_solver, app3_planning_agent) + reasoning_model_selector.py + reasoning_explorer.py
requirements/        # Dependencies
```

## Key APIs

**OpenAI (Responses API)**
```python
client.responses.create(
    model="gpt-5.6",
    reasoning={"effort": "medium"},  # none/low/medium/high/xhigh
    input=[{"role": "developer", "content": "..."}, {"role": "user", "content": "..."}]
)
```

**Anthropic (Extended Thinking)**
```python
client.messages.create(
    model="claude-opus-5",
    thinking={"type": "adaptive"},        # adaptive thinking (budget_tokens is deprecated on newest models)
    output_config={"effort": "medium"},   # low/medium/high/xhigh/max
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
