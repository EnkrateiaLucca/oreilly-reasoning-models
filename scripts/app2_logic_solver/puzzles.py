"""
Pre-loaded puzzle library for the Logic Puzzle Solver.
Contains easy, medium, and hard difficulty puzzles.
"""

from typing import TypedDict


class Puzzle(TypedDict):
    title: str
    description: str
    clues: list[str]
    solution: dict
    difficulty: str
    puzzle_type: str  # "ordering", "grid", "einstein"


PUZZLES: dict[str, Puzzle] = {
    # =====================================================================
    # EASY PUZZLES (3-5 clues)
    # =====================================================================
    "race_order": {
        "title": "The Race",
        "description": "Three friends - Alice, Bob, and Carol - finished a race. Determine the order they finished in (1st, 2nd, 3rd).",
        "clues": [
            "Alice did not finish last.",
            "Bob finished before Carol.",
            "Carol did not finish first.",
        ],
        "solution": {"1st": "Alice", "2nd": "Bob", "3rd": "Carol"},
        "difficulty": "easy",
        "puzzle_type": "ordering",
    },
    "pet_owners": {
        "title": "Pet Owners",
        "description": "Three neighbors - Dan, Eve, and Frank - each own a different pet: a cat, a dog, and a fish. Match each person to their pet.",
        "clues": [
            "Dan is allergic to fur, so he doesn't own the cat or dog.",
            "Eve's pet barks at Frank's pet.",
            "The cat belongs to someone whose name starts with the same letter as 'feline'.",
        ],
        "solution": {"Dan": "fish", "Eve": "dog", "Frank": "cat"},
        "difficulty": "easy",
        "puzzle_type": "grid",
    },
    "fruit_stand": {
        "title": "Fruit Stand",
        "description": "Three children - Grace, Henry, and Ivy - each bought a different fruit: an apple, a banana, and a cherry. Who bought what?",
        "clues": [
            "Grace didn't buy the banana.",
            "Henry bought a fruit that starts with a vowel.",
            "Ivy bought the banana.",
        ],
        "solution": {"Grace": "cherry", "Henry": "apple", "Ivy": "banana"},
        "difficulty": "easy",
        "puzzle_type": "grid",
    },
    # =====================================================================
    # MEDIUM PUZZLES (5-8 clues)
    # =====================================================================
    "movie_night": {
        "title": "Movie Night",
        "description": "Four friends - Jack, Kate, Leo, and Mia - watched movies on four consecutive nights (Monday through Thursday). Each watched a different genre: Action, Comedy, Drama, and Horror. Determine who watched what and when.",
        "clues": [
            "Jack watched his movie the day after Kate.",
            "The Horror movie was watched on Wednesday.",
            "Leo watched Comedy, but not on Monday.",
            "Mia watched her movie on Monday.",
            "The Drama was watched the day before the Action movie.",
            "Kate didn't watch Horror.",
        ],
        "solution": {
            "Monday": {"person": "Mia", "genre": "Drama"},
            "Tuesday": {"person": "Kate", "genre": "Action"},
            "Wednesday": {"person": "Jack", "genre": "Horror"},
            "Thursday": {"person": "Leo", "genre": "Comedy"},
        },
        "difficulty": "medium",
        "puzzle_type": "grid",
    },
    "office_floors": {
        "title": "Office Building",
        "description": "Four companies - Acme, Beta, Core, and Delta - occupy floors 1-4 of an office building. Each company specializes in a different field: Finance, Tech, Legal, and Marketing. Determine which company is on which floor and their specialty.",
        "clues": [
            "The Tech company is directly above the Finance company.",
            "Acme is on floor 3.",
            "Beta specializes in Legal and is on a higher floor than Core.",
            "Delta is not on floor 1 or floor 4.",
            "The Marketing company is on floor 1.",
            "Core is not the Tech company.",
        ],
        "solution": {
            "floor_1": {"company": "Core", "specialty": "Marketing"},
            "floor_2": {"company": "Delta", "specialty": "Finance"},
            "floor_3": {"company": "Acme", "specialty": "Tech"},
            "floor_4": {"company": "Beta", "specialty": "Legal"},
        },
        "difficulty": "medium",
        "puzzle_type": "grid",
    },
    "dinner_party": {
        "title": "Dinner Party Seating",
        "description": "Five guests - Anna, Ben, Chris, Diana, and Ed - are seated around a circular table. Determine their seating arrangement (positions 1-5, clockwise).",
        "clues": [
            "Anna is seated directly across from Ben (two seats apart).",
            "Chris is seated next to Diana.",
            "Ed is not seated next to Anna.",
            "Ben is seated in position 1.",
            "Diana is seated in an even-numbered position.",
            "Chris is seated between Ed and Diana.",
        ],
        "solution": {
            "position_1": "Ben",
            "position_2": "Diana",
            "position_3": "Chris",
            "position_4": "Ed",
            "position_5": "Anna",
        },
        "difficulty": "medium",
        "puzzle_type": "ordering",
    },
    # =====================================================================
    # HARD PUZZLES (Einstein-style, 10+ clues)
    # =====================================================================
    "einstein_houses": {
        "title": "Einstein's Riddle (Simplified)",
        "description": "Five houses in a row, each painted a different color. Each house is occupied by a person of a different nationality, who drinks a different beverage, smokes a different brand, and keeps a different pet. The question: Who owns the fish?",
        "clues": [
            "The British person lives in the red house.",
            "The Swedish person keeps dogs as pets.",
            "The Danish person drinks tea.",
            "The green house is immediately to the left of the white house.",
            "The owner of the green house drinks coffee.",
            "The person who smokes Pall Mall keeps birds.",
            "The owner of the yellow house smokes Dunhill.",
            "The person living in the center house drinks milk.",
            "The Norwegian lives in the first house.",
            "The person who smokes Blend lives next to the one who keeps cats.",
            "The person who keeps horses lives next to the one who smokes Dunhill.",
            "The person who smokes BlueMaster drinks beer.",
            "The German smokes Prince.",
            "The Norwegian lives next to the blue house.",
            "The person who smokes Blend has a neighbor who drinks water.",
        ],
        "solution": {
            "house_1": {
                "color": "yellow",
                "nationality": "Norwegian",
                "beverage": "water",
                "smoke": "Dunhill",
                "pet": "cats",
            },
            "house_2": {
                "color": "blue",
                "nationality": "Danish",
                "beverage": "tea",
                "smoke": "Blend",
                "pet": "horses",
            },
            "house_3": {
                "color": "red",
                "nationality": "British",
                "beverage": "milk",
                "smoke": "Pall Mall",
                "pet": "birds",
            },
            "house_4": {
                "color": "green",
                "nationality": "German",
                "beverage": "coffee",
                "smoke": "Prince",
                "pet": "fish",
            },
            "house_5": {
                "color": "white",
                "nationality": "Swedish",
                "beverage": "beer",
                "smoke": "BlueMaster",
                "pet": "dogs",
            },
        },
        "difficulty": "hard",
        "puzzle_type": "einstein",
    },
    "detective_mystery": {
        "title": "The Detective's Challenge",
        "description": "Five suspects - Mr. Adams, Ms. Baker, Dr. Clark, Prof. Davis, and Lady Evans - were at a mansion when a theft occurred. Each was in a different room (Library, Kitchen, Garden, Study, Ballroom), wore a different color outfit (Red, Blue, Green, Black, White), and had a different alibi activity (Reading, Cooking, Walking, Writing, Dancing). The thief was in the room adjacent to the Study. Determine who was where, wearing what, and doing what.",
        "clues": [
            "Mr. Adams was wearing black and was not in the Kitchen.",
            "The person in the Library was reading.",
            "Ms. Baker was in the Garden.",
            "Dr. Clark was wearing blue and was in a room adjacent to the Kitchen.",
            "The person cooking was wearing white.",
            "Prof. Davis was not dancing and was not wearing red.",
            "Lady Evans was in the Ballroom dancing.",
            "The person in the Study was writing.",
            "The person wearing green was walking in the Garden.",
            "Mr. Adams was in the Library.",
            "The Kitchen is adjacent to the Library and the Ballroom.",
            "The Study is adjacent to the Library and the Garden.",
            "Prof. Davis was wearing black or blue.",
        ],
        "solution": {
            "Mr. Adams": {
                "room": "Library",
                "color": "black",
                "activity": "reading",
            },
            "Ms. Baker": {"room": "Garden", "color": "green", "activity": "walking"},
            "Dr. Clark": {"room": "Kitchen", "color": "white", "activity": "cooking"},
            "Prof. Davis": {"room": "Study", "color": "blue", "activity": "writing"},
            "Lady Evans": {"room": "Ballroom", "color": "red", "activity": "dancing"},
        },
        "difficulty": "hard",
        "puzzle_type": "einstein",
    },
    "school_schedule": {
        "title": "School Schedule Puzzle",
        "description": "Five students - Amy, Brian, Chloe, David, and Emma - each have a favorite subject (Math, English, Science, History, Art) and attend a club (Chess, Drama, Sports, Music, Debate). They also live on different streets (Oak, Elm, Pine, Maple, Cedar). Match each student with their subject, club, and street.",
        "clues": [
            "Amy lives on Oak Street and doesn't like Math.",
            "The student who likes Science is in the Chess club.",
            "Brian is in the Drama club but doesn't like English.",
            "Chloe lives on Pine Street and is in the Music club.",
            "David likes History and lives next to the student in Sports club.",
            "The student on Elm Street likes Math.",
            "Emma is in the Debate club.",
            "The student who likes Art is in the Music club.",
            "The Sports club member lives on Cedar Street.",
            "Amy likes English.",
            "The student on Maple Street is in the Chess club.",
            "Brian lives on Elm Street.",
            "David is in the Sports club.",
        ],
        "solution": {
            "Amy": {"subject": "English", "club": "Drama", "street": "Oak"},
            "Brian": {"subject": "Math", "club": "Drama", "street": "Elm"},
            "Chloe": {"subject": "Art", "club": "Music", "street": "Pine"},
            "David": {"subject": "History", "club": "Sports", "street": "Cedar"},
            "Emma": {"subject": "Science", "club": "Debate", "street": "Maple"},
        },
        "difficulty": "hard",
        "puzzle_type": "einstein",
    },
}


def get_puzzle(puzzle_id: str) -> Puzzle | None:
    """Get a puzzle by its ID."""
    return PUZZLES.get(puzzle_id)


def get_puzzles_by_difficulty(difficulty: str) -> dict[str, Puzzle]:
    """Get all puzzles of a specific difficulty."""
    return {k: v for k, v in PUZZLES.items() if v["difficulty"] == difficulty}


def list_puzzles() -> list[dict]:
    """List all puzzles with basic info."""
    return [
        {
            "id": k,
            "title": v["title"],
            "difficulty": v["difficulty"],
            "clue_count": len(v["clues"]),
        }
        for k, v in PUZZLES.items()
    ]
