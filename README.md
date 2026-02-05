# O'Reilly Live Training: Working with OpenAI and Anthropic Reasoning Models

This repository contains materials for the O'Reilly live training course on reasoning capabilities of modern LLMs.

## Course Information

**Link**: [Working with OpenAI and Anthropic Reasoning Models](https://www.oreilly.com/live-events/working-with-o1-deepseek-and-gemini-20-reasoning-capabilities/0642572015593/)

This course explores the reasoning capabilities of OpenAI's GPT-5.2 and Anthropic's Claude models. Learn how to effectively leverage these models' advanced reasoning abilities for your applications.

### Key Concepts Covered

- What defines a reasoning/thinking model
- When to use reasoning models vs. traditional LLMs
- How to choose the right reasoning effort level
- Best practices for prompting reasoning models
- Cost and performance optimization strategies
- Integration patterns for production workflows

## Repository Structure

- `notebooks/`: Jupyter notebooks for hands-on exercises
  - `analytical-framework.ipynb`: LLM-as-a-Judge framework for evaluating model performance
  - `openai-thinking-parameters.ipynb`: Comprehensive guide to OpenAI's GPT-5.2 with the Responses API
  - `anthropic-extended-thinking.ipynb`: Guide to Anthropic's Claude extended thinking capabilities
  - `assets-resources/`: Additional resources and reference materials
- `presentation/`: Slides and presentation materials
- `project-notes.md`: Notes and resources for the live course

### Notebook Descriptions

#### 1. Analytical Framework (`analytical-framework.ipynb`)
A practical framework for evaluating LLM performance using LLM-as-a-Judge methodology:
- Compare model outputs across GPT-4o, GPT-5.2, and Claude Sonnet 4.5
- Structured evaluation with Pydantic models
- Cost analysis with real 2026 pricing
- PDF-to-markdown conversion for document analysis

#### 2. OpenAI Thinking Parameters (`openai-thinking-parameters.ipynb`)
A hands-on guide to OpenAI's GPT-5.2 reasoning capabilities:
- **Responses API**: New API designed for reasoning models
- **Reasoning Effort Levels**: none, low, medium, high, xhigh
- **Verbosity Control**: Independent output length control
- **Tool Use**: Function calling and web search integration
- **Structured Outputs**: Pydantic models for typed responses
- **Best Practices**: Write briefs, focus on WHAT not HOW

#### 3. Anthropic Extended Thinking (`anthropic-extended-thinking.ipynb`)
A comprehensive tutorial on Claude's extended thinking feature:
- **Budget Tokens**: Control reasoning depth (1K-32K+ tokens)
- **Streaming**: Required for large outputs, improves UX
- **Tool Use**: Integration with tool_choice: auto
- **Interleaved Thinking**: Beta feature for Claude 4 models
- **Summarized Thinking**: Claude 4+ returns summaries, billed for full tokens
- **Best Practices**: Start minimal, don't say "think step by step"

## Getting Started

### Prerequisites

- OpenAI API key
- Anthropic API key
- Python 3.11 or higher (for local setup only)

### Option 1: GitHub Codespaces (Recommended)

GitHub Codespaces provides a ready-to-use development environment in your browser. No local installation required.

#### Step 1: Launch the Codespace

1. Click the green **Code** button at the top of this repository
2. Select the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait for the environment to build

#### Step 2: Set Up Your API Keys

You'll need API keys from OpenAI and Anthropic to run the notebooks. Choose one of the following options:

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
6. Repeat steps 4-5 for `ANTHROPIC_API_KEY`

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
   export ANTHROPIC_API_KEY='your-anthropic-key-here'
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
