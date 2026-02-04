#!/bin/bash
set -e

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create virtual environment and install dependencies
uv venv .venv
uv pip install -r requirements/requirements.txt

# Install Jupyter kernel
uv run ipython kernel install --user --env VIRTUAL_ENV "$(pwd)/.venv" --name=oreilly-reasoning

echo "Codespace ready! Open any .ipynb file from the notebooks/ folder to get started."
