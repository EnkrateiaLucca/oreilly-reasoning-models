"""
Pre-loaded example math problems for the comparator app.
Each problem includes the question, expected answer, and difficulty level.
"""

MATH_PROBLEMS = [
    # ===== EASY (Single-step arithmetic) =====
    {
        "question": "What is 847 + 256?",
        "answer": "1103",
        "difficulty": "easy"
    },
    {
        "question": "Calculate 15 × 24.",
        "answer": "360",
        "difficulty": "easy"
    },
    {
        "question": "What is 1000 - 347?",
        "answer": "653",
        "difficulty": "easy"
    },
    {
        "question": "Divide 144 by 12.",
        "answer": "12",
        "difficulty": "easy"
    },
    {
        "question": "What is 25% of 200?",
        "answer": "50",
        "difficulty": "easy"
    },

    # ===== MEDIUM (Multi-step word problems) =====
    {
        "question": "A store sells apples for $2 each and oranges for $3 each. If Sarah buys 5 apples and 4 oranges, and pays with a $50 bill, how much change does she receive?",
        "answer": "28",
        "difficulty": "medium"
    },
    {
        "question": "A train travels at 60 mph for 2 hours, then at 80 mph for 3 hours. What is the total distance traveled?",
        "answer": "360",
        "difficulty": "medium"
    },
    {
        "question": "If a rectangle has a perimeter of 56 cm and its length is 4 cm more than its width, what is the area of the rectangle in square centimeters?",
        "answer": "192",
        "difficulty": "medium"
    },
    {
        "question": "John has 3 times as many marbles as Mike. Together they have 48 marbles. How many marbles does John have?",
        "answer": "36",
        "difficulty": "medium"
    },
    {
        "question": "A jar contains red and blue marbles. The ratio of red to blue marbles is 3:5. If there are 24 red marbles, how many marbles are in the jar in total?",
        "answer": "64",
        "difficulty": "medium"
    },

    # ===== HARD (Competition-math/AIME-style) =====
    {
        "question": "Find the sum of all positive integers n such that n^2 + 12n - 2007 is a perfect square.",
        "answer": "80",
        "difficulty": "hard"
    },
    {
        "question": "How many ways can you arrange the letters in the word MISSISSIPPI?",
        "answer": "34650",
        "difficulty": "hard"
    },
    {
        "question": "In a right triangle, the legs have lengths 5 and 12. A circle is inscribed in the triangle. What is the radius of the inscribed circle?",
        "answer": "2",
        "difficulty": "hard"
    },
    {
        "question": "Find the remainder when 7^2023 is divided by 100.",
        "answer": "43",
        "difficulty": "hard"
    },
    {
        "question": "The sequence 1, 2, 3, 5, 8, 13, 21, ... follows the Fibonacci pattern. What is the units digit of the 100th Fibonacci number?",
        "answer": "5",
        "difficulty": "hard"
    },
]


def get_problems_by_difficulty(difficulty: str = None) -> list:
    """
    Get problems filtered by difficulty level.

    Args:
        difficulty: 'easy', 'medium', 'hard', or None for all problems

    Returns:
        List of problem dictionaries
    """
    if difficulty is None or difficulty.lower() == "all":
        return MATH_PROBLEMS
    return [p for p in MATH_PROBLEMS if p["difficulty"] == difficulty.lower()]


def get_difficulty_levels() -> list:
    """Return available difficulty levels."""
    return ["all", "easy", "medium", "hard"]


def format_problem_for_display(problem: dict) -> str:
    """Format a problem for display in a selectbox."""
    diff_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    emoji = diff_emoji.get(problem["difficulty"], "⚪")
    # Truncate long questions for display
    question = problem["question"]
    if len(question) > 60:
        question = question[:57] + "..."
    return f"{emoji} {question}"
