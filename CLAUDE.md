# O'Reilly Reasoning Models Course

Course on reasoning models: building the DeepSeek R1-style training pipeline from scratch, plus OpenAI reasoning-model demo apps. Anthropic Claude extended thinking is covered conceptually in the slides.

## Structure

```
notebooks/           # Jupyter notebooks — the R1-style pipeline, built from scratch
├── 00_setup_check.ipynb                                          # Verify environment and API keys
├── 01_foundations_reasoning_and_cot.ipynb                        # What a reasoning LLM is, CoT as test-time compute
├── 02_rl_core_coldstart_sft_and_grpo.ipynb                       # Cold-start SFT + GRPO from scratch
├── 03_amplify_and_compress_rejection_sft_and_distillation.ipynb  # Rejection-sampling SFT + distillation
├── 04_picking_a_reasoning_model_for_an_application.ipynb         # Multi-provider model bake-off with an LLM judge
├── 05_reproducibility_cheap_vs_flagship.ipynb                    # Cheap vs. flagship cost/reproducibility experiment
├── provider_anthropic_extended_thinking.ipynb                    # Provider deep-dive: Claude extended thinking, hands-on
└── provider_openai_thinking_parameters.ipynb                     # Provider deep-dive: OpenAI reasoning-effort parameters, hands-on
# Checkpoints (written by the notebooks, not committed): nb2_cold_start.pt, nb2_after_grpo.pt, nb3_after_reject_sft.pt
# Original five single-stage notebooks preserved under notebooks/archive/

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
    output_config={"effort": "medium"},
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
