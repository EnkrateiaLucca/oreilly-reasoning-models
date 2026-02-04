# O'Reilly Live Training: Working with o1, DeepSeek, and Gemini 2.5 Pro Reasoning Capabilities

This repository contains materials for the O'Reilly live training course on reasoning capabilities of modern LLMs.

## Course Information

Link: [Working with o1, DeepSeek, and Gemini 2.5 Reasoning Capabilities](https://www.oreilly.com/live-events/working-with-o1-deepseek-and-gemini-20-reasoning-capabilities/0642572015593/)

## Getting Started with GitHub Codespaces

GitHub Codespaces provides a ready-to-use development environment in your browser. No local installation required.

### Step 1: Launch the Codespace

1. Click the green **Code** button at the top of this repository
2. Select the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait for the environment to build (approximately 2-3 minutes on first launch)

### Step 2: Set Up Your API Keys

You'll need API keys from OpenAI and Anthropic to run the notebooks. Choose one of the following options:

#### Option A: GitHub Secrets (Recommended)

This method securely stores your keys and auto-injects them into every Codespace you create.

1. Go to [github.com](https://github.com) → Click your profile picture → **Settings**
2. In the left sidebar, click **Codespaces**
3. Under **Codespaces secrets**, click **New secret**
4. Add your first secret:
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key
   - Click **Add secret**
   - Select this repository to grant access
5. Repeat for `ANTHROPIC_API_KEY`

After adding secrets, restart your Codespace for them to take effect.

#### Option B: Environment File

If you prefer not to use GitHub secrets, you can create a local `.env` file:

1. In the Codespace terminal, run:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and replace the placeholder values with your actual API keys
3. The `.env` file is git-ignored, so your keys won't be accidentally committed

### Step 3: Start Jupyter Lab

Once your Codespace is ready and API keys are configured, run:

```bash
uv run --with jupyter jupyter lab
```

A notification will appear with a link to open Jupyter Lab. Click it, or go to the **Ports** tab and click the forwarded port (8888).

## Repository Structure

- `notebooks/`: Jupyter notebooks for hands-on exercises
  - `gpt5-reasoning-demo.ipynb`: **New!** Comprehensive guide to OpenAI's GPT-5 reasoning models with the Responses API
  - `introduction-to-reasoning-models.ipynb`: Introduction to reasoning model concepts
  - `assets-resources/`: Additional resources and reference materials
- `presentation/`: Slides and presentation materials
- `project-notes.md`: Notes and resources for the live course

## Notebooks

### GPT-5 Reasoning Demo (`gpt5-reasoning-demo.ipynb`)

A practical, hands-on guide to OpenAI's GPT-5 reasoning capabilities featuring:

- **Reasoning Effort Levels**: Compare minimal, medium, and high reasoning efforts with real examples
- **Verbosity Control**: Learn how to control output length independently from reasoning depth
- **Practical Use Cases**:
  - Simple classification with minimal reasoning
  - Code generation with medium reasoning
  - Complex algorithm design with high reasoning
  - Bug detection and code review
- **Best Practices**: Based on OpenAI's latest guidelines for optimal performance
- **Token Usage Analysis**: See how different settings affect cost and performance

All examples are designed to run quickly and demonstrate clear, practical applications.

## Local Setup (Alternative to Codespaces)

If you prefer to run locally instead of using GitHub Codespaces:

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Anthropic API key

### Installation

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

5. Start Jupyter Lab:
   ```bash
   uv run --with jupyter jupyter lab
   ```

## About This Course

This course explores the reasoning capabilities of the latest AI models including OpenAI's GPT-5, o-series models, DeepSeek, and Google's Gemini 2.0. Learn how to effectively leverage these models' advanced reasoning abilities for your applications.

## Key Concepts Covered

- What defines a reasoning/thinking model
- When to use reasoning models vs. traditional LLMs
- How to choose the right reasoning effort level
- Best practices for prompting reasoning models
- Cost and performance optimization strategies
- Integration patterns for production workflows