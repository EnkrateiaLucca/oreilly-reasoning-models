# Logic Puzzle Solver & Explainer

A Streamlit application that solves logic puzzles using OpenAI's o3-mini reasoning model with visible chain-of-thought reasoning.

## Features

- **Pre-loaded Puzzle Library**: Easy, medium, and hard difficulty puzzles including Einstein-style riddles
- **Custom Puzzle Mode**: Enter your own logic puzzles to solve
- **Visible Reasoning**: See the model's step-by-step deductions
- **Constraint Verification**: Each clue is verified against the solution with pass/fail status
- **Performance Metrics**: Token usage and solve time tracking
- **Difficulty Visualization**: Radar chart showing puzzle complexity profile

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select a pre-loaded puzzle from the sidebar or switch to "Custom Puzzle" mode
2. Adjust the reasoning effort level (low/medium/high) based on puzzle complexity
3. Click "Solve Puzzle" to see the solution and reasoning
4. Review the chain-of-thought in the expandable sections
5. Check the constraint verification to see if all clues are satisfied

## Puzzle Types

- **Ordering**: Determine the order of entities (e.g., race positions)
- **Grid**: Match entities to attributes (e.g., person to pet)
- **Einstein**: Complex multi-attribute puzzles with multiple categories

## API Usage

This app uses:
- **o3-mini**: For puzzle solving with reasoning capabilities
- **gpt-4o-mini**: For constraint verification (lightweight checks)

## File Structure

```
app2_logic_solver/
├── app.py           # Main Streamlit application
├── puzzles.py       # Pre-loaded puzzle library
├── verifier.py      # Constraint verification logic
├── requirements.txt # Python dependencies
├── .env.example     # Environment variable template
└── README.md        # This file
```
