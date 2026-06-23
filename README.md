# O'Reilly Live Training: Working with OpenAI and Anthropic Reasoning Models

This repository contains materials for the O'Reilly live training course on reasoning capabilities of modern LLMs.

## Course Information

**Link**: [Working with OpenAI and Anthropic Reasoning Models](https://www.oreilly.com/live-events/working-with-o1-deepseek-and-gemini-20-reasoning-capabilities/0642572015593/)

This course explores how modern reasoning models (OpenAI o-series, DeepSeek R1, Claude extended thinking) actually work — by building the R1-style training pipeline from scratch and walking through the DeepSeek R1 paper.

### Key Concepts Covered

- What defines a reasoning/thinking model and how chain-of-thought emerges
- The five-stage R1 recipe: pretraining → cold-start SFT → RL (GRPO) → rejection-sampling SFT → distillation
- GRPO (Group Relative Policy Optimization) implemented from scratch
- When to use reasoning models vs. traditional LLMs
- Hands-on with the DeepSeek R1 mechanism (the from-scratch pipeline) and OpenAI reasoning-model demo apps; Anthropic/Claude extended thinking is covered conceptually in the slides

## Repository Structure

```
notebooks/      # Hands-on notebooks building the R1 training pipeline from scratch
presentation/   # Slide decks (markdown sources + rendered PDFs)
scripts/        # Demo apps showcasing reasoning-model use cases
requirements/   # Python dependencies
```

> **Quick reference:** A one-page cheatsheet is available at [`oreilly-reasoning-models-cheatsheet.html`](oreilly-reasoning-models-cheatsheet.html) (or the print-ready [`.pdf`](oreilly-reasoning-models-cheatsheet.pdf)).

### Notebooks (`notebooks/`)

Walks through the full R1-style reasoning-model training pipeline. The five-stage recipe is
consolidated into **three runnable, CPU-friendly notebooks**, each carrying one metric — the task
**pass-rate** on a toy 1-digit-addition task — so you watch the same number climb the whole way:

- `00_setup_check.ipynb` — verify environment and API keys
- `01_foundations_reasoning_and_cot.ipynb` — what a reasoning LLM is, CoT as test-time compute, and the capstone experiment: a scratchpad beats answering directly (measured locally)
- `02_rl_core_coldstart_sft_and_grpo.ipynb` — cold-start SFT (teach the `<think>`/`<answer>` format) then GRPO from scratch (no critic, no human labels)
- `03_amplify_and_compress_rejection_sft_and_distillation.ipynb` — rejection-sampling SFT (self-generated data) then distillation into a ~7× smaller student
- `07_picking_a_reasoning_model_for_an_application.ipynb` — a multi-provider model bake-off with an LLM judge
- `08_reproducibility_cheap_vs_flagship.ipynb` — fix a seed and show a cheaper model (DeepSeek V4 Pro) can match a flagship at a fraction of the cost (runs in mock mode without API keys)

Shared machinery lives in `r1_toy.py`. The original five single-stage notebooks are preserved under
`notebooks/archive/`.

### Presentation (`presentation/`)

Three decks (markdown source + PDF):

- `01-intro-reasoning-llms` — intro to reasoning LLMs and the landscape
- `02-deepseek-r1-paper-walkthrough` — guided walkthrough of the DeepSeek R1 paper
- `03-r1-recipe-five-stages` — the five-stage R1 recipe mapped onto the three technical notebooks

### Scripts (`scripts/`)

- `app1_math_comparator/`, `app2_logic_solver/`, `app3_planning_agent/` — demo apps showcasing reasoning-model use cases
- `reasoning_model_selector.py` — a runnable decision aid for *choosing* a current reasoning model (gpt-5.5, the o-series, Claude extended thinking, DeepSeek R1). Prints a comparison + recommends one from a task profile; `--weights` ranks the models by a score you control (reasoning/speed/cost); `--chart` saves the comparison image to `presentation/assets/` (alongside the deck images). Pairs with the deck-01 "When to reach for a reasoning model" flowchart.

  ```bash
  python scripts/reasoning_model_selector.py                       # comparison + sample picks
  python scripts/reasoning_model_selector.py --weights 0.5,0.3,0.2 # weighted ranking: reasoning,speed,cost
  python scripts/reasoning_model_selector.py --chart               # also save the chart PNG
  ```

## Getting Started

### Prerequisites

- OpenAI API key (required — used by the notebooks and demo apps)
- Anthropic / Google / DeepSeek API keys (optional — the model bake-off notebooks `07` and `08` use whichever keys are present; `08` also runs fully in mock mode with no keys)
- Python 3.11 or higher (for local setup only)

### Option 1: GitHub Codespaces (Recommended)

GitHub Codespaces provides a ready-to-use development environment in your browser. No local installation required.

#### Step 1: Launch the Codespace

1. Click the green **Code** button at the top of this repository
2. Select the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait for the environment to build

#### Step 2: Set Up Your API Keys

You'll need an OpenAI API key to run the core notebooks and demo apps. Anthropic / Google / DeepSeek keys are optional — the bake-off notebooks `07` and `08` use whichever are present. Choose one of the following options:

**Option A: GitHub Secrets (Recommended)**

This method securely stores your keys and auto-injects them into every Codespace you create.

1. Go to [github.com](https://github.com) → Click your profile picture → **Settings**
2. In the left sidebar, click **Codespaces**
3. Under **Codespaces secrets**, click **New secret**
4. Add your first secret:
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key
   - Click **Add secret**
5. **Important: Grant repository access**
   - After creating the secret, click the secret name to edit it
   - Under "Repository access", select this repository (`oreilly-reasoning-models`)
   - Without this step, the secret won't be available in your Codespace
6. (Optional) Repeat steps 4-5 for `ANTHROPIC_API_KEY` if you want to experiment with Claude on your own

After adding secrets with repository access, restart your Codespace for them to take effect.

**Option B: Environment File**

If you prefer not to use GitHub secrets, you can create a local `.env` file:

1. In the Codespace terminal, run:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and replace the placeholder values with your actual API keys
3. The `.env` file is git-ignored, so your keys won't be accidentally committed

#### Step 3: Open the Notebooks

Once your Codespace is ready and API keys are configured, open any `.ipynb` file from the `notebooks/` folder in the file explorer. VS Code has built-in Jupyter support and will run the notebooks directly.

#### Select the Correct Kernel (Important!)

When you open a notebook, VS Code will prompt you to select a kernel:

1. Click the kernel selector in the top-right corner of the notebook
2. Select **oreilly-reasoning** from the list
3. If you don't see it, click "Select Another Kernel..." → "Python Environments..." → select the `.venv` from this project

**Note**: If you have multiple Codespaces or projects, make sure you're using the kernel for *this* project. Using a kernel from a different project will cause `ModuleNotFoundError` for packages specific to this course.

### Option 2: Local Setup

If you prefer to run locally instead of using GitHub Codespaces:

#### Installation

1. Install uv (fast Python package manager):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/EnkrateiaLucca/oreilly-reasoning-models.git
   cd oreilly-reasoning-models
   ```

3. Create virtual environment and install dependencies:
   ```bash
   uv venv .venv
   uv pip install -r requirements/requirements.txt
   ```

4. Set up your API keys (choose one method):

   **Option A: Environment variables**
   ```bash
   export OPENAI_API_KEY='your-openai-key-here'
   export ANTHROPIC_API_KEY='your-anthropic-key-here'  # optional
   ```

   **Option B: Environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. Install the Jupyter kernel for this project:
   ```bash
   source .venv/bin/activate
   python -m ipykernel install --user --name=oreilly-reasoning --display-name "O'Reilly Reasoning Models"
   ```

6. Open the notebooks in VS Code:
   ```bash
   code .
   ```

   Then open any `.ipynb` file from the `notebooks/` folder.

#### Step 7: Select the Correct Kernel (Important!)

**This step is critical** - you must select the kernel for this specific project:

1. Open any `.ipynb` notebook file
2. Click the kernel selector in the top-right corner of the notebook (it may show "Select Kernel" or another kernel name)
3. Select **"O'Reilly Reasoning Models"** (or `oreilly-reasoning`) from the list
4. If you don't see it, click "Select Another Kernel..." → "Python Environments..." → look for the one pointing to this project's `.venv`

**Why this matters**: Each Python project has its own virtual environment with its own packages. If you select a kernel from a different project, you'll get `ModuleNotFoundError` for packages that are installed in this project but not in the other one.
