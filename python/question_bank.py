"""
Question Bank for CodeBreak:
Contains coding questions categorized into Easy, Medium, and Hard difficulty levels.
"""

QUESTIONS = [
    # ==========================================
    # 🟢 EASY LEVEL QUESTIONS
    # ==========================================
    {
        "id": "E1",
        "difficulty": "Easy",
        "title": "E1: Sum of Two Numbers",
        "category": "Syntax & Basics",
        "description": "Write a function `add_numbers(a, b)` that takes two numbers and returns their sum. Execute to test your solution.",
        "starter_code": "def add_numbers(a, b):\n    # Return the sum of a and b\n    return a + b\n\nprint(add_numbers(15, 27))",
        "expected_output": "42",
        "hint": "Use the `+` arithmetic operator and `return a + b` inside the function.",
        "concept": "Syntax & Basics",
        "xp": 50
    },
    {
        "id": "E2",
        "difficulty": "Easy",
        "title": "E2: Check Even or Odd",
        "category": "Arithmetic Operations",
        "description": "Write a function `is_even(n)` that returns `True` if `n` is an even number, otherwise `False`.",
        "starter_code": "def is_even(n):\n    return n % 2 == 0\n\nprint(is_even(14))",
        "expected_output": "True",
        "hint": "Use the modulo operator `%` to check if `n % 2 == 0`.",
        "concept": "Arithmetic Operations",
        "xp": 50
    },
    {
        "id": "E3",
        "difficulty": "Easy",
        "title": "E3: Fix Missing Colon Syntax",
        "category": "Syntax & Formatting Rules",
        "description": "Fix the `SyntaxError` in the conditional header line so that it prints `'Number is greater than 10'`.",
        "starter_code": "num = 25\nif num > 10\n    print('Number is greater than 10')",
        "expected_output": "Number is greater than 10",
        "hint": "Add a colon `:` at the end of `if num > 10`.",
        "concept": "Syntax & Formatting Rules",
        "xp": 50
    },
    {
        "id": "E4",
        "difficulty": "Easy",
        "title": "E4: Access First Item of List",
        "category": "List Indexing",
        "description": "Fix the code so it prints the very first item (`'apple'`) from the list.",
        "starter_code": "fruits = ['apple', 'banana', 'cherry']\n# Python lists use 0-based indexing\nprint(fruits[1])",
        "expected_output": "apple",
        "hint": "In Python, the first element is at index `0` (`fruits[0]`).",
        "concept": "List Indexing",
        "xp": 50
    },
    {
        "id": "E5",
        "difficulty": "Easy",
        "title": "E5: String & Number Formatting",
        "category": "Type Compatibility & Casting",
        "description": "Combine the player name and score into the string `'Player Alex scored 100 points'`.",
        "starter_code": "name = 'Alex'\nscore = 100\nprint(f'Player {name} scored {score} points')",
        "expected_output": "Player Alex scored 100 points",
        "hint": "Use an f-string `f'Player {name} scored {score} points'` or `str(score)`.",
        "concept": "Type Compatibility & Casting",
        "xp": 50
    },
    {
        "id": "E6",
        "difficulty": "Easy",
        "title": "E6: Count Positive Numbers",
        "category": "Loops & Logic",
        "description": "Count how many positive numbers (greater than 0) are in the list `[5, -3, 12, -8, 7, 0]`.",
        "starter_code": "numbers = [5, -3, 12, -8, 7, 0]\npositives = [x for x in numbers if x > 0]\nprint(len(positives))",
        "expected_output": "3",
        "hint": "Filter items with `x > 0` and print `len(positives)`.",
        "concept": "Loops & Logic",
        "xp": 50
    },

    # ==========================================
    # 🟡 MEDIUM LEVEL QUESTIONS
    # ==========================================
    {
        "id": "M1",
        "difficulty": "Medium",
        "title": "M1: Safe Dictionary Lookup",
        "category": "Dictionary Lookup",
        "description": "Use dictionary `.get()` to look up `'country'` safely, returning `'Not Specified'` if missing.",
        "starter_code": "profile = {'name': 'Sara', 'city': 'Tokyo'}\n# Avoid KeyError by using .get()\nprint(profile.get('country', 'Not Specified'))",
        "expected_output": "Not Specified",
        "hint": "Use `dict.get('country', 'Not Specified')` instead of bracket indexing.",
        "concept": "Dictionary Lookup",
        "xp": 100
    },
    {
        "id": "M2",
        "difficulty": "Medium",
        "title": "M2: Empty List Average Guard",
        "category": "Arithmetic Operations",
        "description": "Prevent `ZeroDivisionError` when computing average of an empty list by returning `0.0`.",
        "starter_code": "def calculate_average(values):\n    if not values:\n        return 0.0\n    return sum(values) / len(values)\n\nprint(calculate_average([]))",
        "expected_output": "0.0",
        "hint": "Add a check `if not values: return 0.0` before dividing by `len(values)`.",
        "concept": "Arithmetic Operations",
        "xp": 100
    },
    {
        "id": "M3",
        "difficulty": "Medium",
        "title": "M3: Reverse a String",
        "category": "String Manipulation",
        "description": "Write a function `reverse_string(text)` that returns the reversed text string.",
        "starter_code": "def reverse_string(text):\n    return text[::-1]\n\nprint(reverse_string('codebreak'))",
        "expected_output": "kaerbedoc",
        "hint": "Use string slicing `text[::-1]` to reverse a string.",
        "concept": "String Manipulation",
        "xp": 100
    },
    {
        "id": "M4",
        "difficulty": "Medium",
        "title": "M4: Remove Duplicates from List",
        "category": "Data Structures",
        "description": "Remove duplicates from `[10, 20, 20, 30, 10, 40]` while maintaining original order.",
        "starter_code": "raw_items = [10, 20, 20, 30, 10, 40]\nunique_items = list(dict.fromkeys(raw_items))\nprint(unique_items)",
        "expected_output": "[10, 20, 30, 40]",
        "hint": "Use `list(dict.fromkeys(raw_items))` to preserve original order.",
        "concept": "Data Structures",
        "xp": 100
    },
    {
        "id": "M5",
        "difficulty": "Medium",
        "title": "M5: Find Maximum in Numeric List",
        "category": "List Processing",
        "description": "Find and print the highest test score in the list `[88, 95, 72, 100, 64]`.",
        "starter_code": "scores = [88, 95, 72, 100, 64]\nprint(max(scores))",
        "expected_output": "100",
        "hint": "Use Python's built-in `max()` function.",
        "concept": "List Processing",
        "xp": 100
    },
    {
        "id": "M6",
        "difficulty": "Medium",
        "title": "M6: Clean String Whitespace in List",
        "category": "Object Attributes & Methods",
        "description": "Strip leading/trailing spaces from each string in `['  python ', '  java  ', ' c++  ']`.",
        "starter_code": "raw_words = ['  python ', '  java  ', ' c++  ']\ncleaned = [w.strip() for w in raw_words]\nprint(cleaned)",
        "expected_output": "['python', 'java', 'c++']",
        "hint": "Use list comprehension `[w.strip() for w in raw_words]`.",
        "concept": "Object Attributes & Methods",
        "xp": 100
    },

    # ==========================================
    # 🔴 HARD LEVEL QUESTIONS
    # ==========================================
    {
        "id": "H1",
        "difficulty": "Hard",
        "title": "H1: Safe File Access with Try-Except",
        "category": "File Handling & Paths",
        "description": "Catch `FileNotFoundError` when trying to open a non-existent file and print `'File missing'`.",
        "starter_code": "try:\n    with open('non_existent_file.txt', 'r') as f:\n        data = f.read()\nexcept FileNotFoundError:\n    data = 'File missing'\nprint(data)",
        "expected_output": "File missing",
        "hint": "Use a `try-except FileNotFoundError:` block to catch missing file errors.",
        "concept": "File Handling & Paths",
        "xp": 150
    },
    {
        "id": "H2",
        "difficulty": "Hard",
        "title": "H2: Recursive Factorial Function",
        "category": "Recursion & Scope",
        "description": "Write a recursive function `factorial(n)` returning `n!` for `n = 6` (expected output: `720`).",
        "starter_code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(6))",
        "expected_output": "720",
        "hint": "Base case: `if n <= 1: return 1`, recursive step: `return n * factorial(n - 1)`.",
        "concept": "Recursion & Scope",
        "xp": 150
    },
    {
        "id": "H3",
        "difficulty": "Hard",
        "title": "H3: Palindrome Verification",
        "category": "String Algorithms",
        "description": "Write `is_palindrome(s)` returning `True` for `'Race car'` (ignoring spaces and letter case).",
        "starter_code": "def is_palindrome(s):\n    clean = ''.join(c.lower() for c in s if c.isalnum())\n    return clean == clean[::-1]\n\nprint(is_palindrome('Race car'))",
        "expected_output": "True",
        "hint": "Clean text with `c.lower()` and `c.isalnum()` then compare with reversed slice `[::-1]`.",
        "concept": "String Algorithms",
        "xp": 150
    },
    {
        "id": "H4",
        "difficulty": "Hard",
        "title": "H4: Character Frequency Counter",
        "category": "Dictionary & Counting",
        "description": "Count how many times character `'a'` occurs in string `'banana'`.",
        "starter_code": "def count_char(text, target):\n    return text.count(target)\n\nprint(count_char('banana', 'a'))",
        "expected_output": "3",
        "hint": "Use `text.count(target)` or loop with a counter.",
        "concept": "Dictionary & Counting",
        "xp": 150
    },
    {
        "id": "H5",
        "difficulty": "Hard",
        "title": "H5: Safe Grid Matrix Sum",
        "category": "Nested Iteration & Indexing",
        "description": "Sum all numbers in 2D matrix `[[10, 20], [30, 40]]` without triggering index errors.",
        "starter_code": "matrix = [[10, 20], [30, 40]]\ntotal = sum(sum(row) for row in matrix)\nprint(total)",
        "expected_output": "100",
        "hint": "Use nested generator `sum(sum(row) for row in matrix)` or double loops.",
        "concept": "Nested Iteration & Indexing",
        "xp": 150
    },
    {
        "id": "H6",
        "difficulty": "Hard",
        "title": "H6: Flatten Nested List",
        "category": "List Comprehensions",
        "description": "Flatten nested list `[[1, 2], [3, 4], [5]]` into a single list `[1, 2, 3, 4, 5]`.",
        "starter_code": "nested = [[1, 2], [3, 4], [5]]\nflat = [item for sublist in nested for item in sublist]\nprint(flat)",
        "expected_output": "[1, 2, 3, 4, 5]",
        "hint": "Use list comprehension `[item for sublist in nested for item in sublist]`.",
        "concept": "List Comprehensions",
        "xp": 150
    }
]

def get_questions_by_difficulty(difficulty: str) -> list:
    """
    Returns list of questions filtered by difficulty (Easy, Medium, Hard).
    """
    if not difficulty or difficulty.lower() == "all":
        return QUESTIONS
    return [q for q in QUESTIONS if q["difficulty"].lower() == difficulty.lower()]

def get_question_by_id(question_id: str) -> dict:
    """
    Finds and returns a question dict by ID.
    """
    for q in QUESTIONS:
        if q["id"] == question_id:
            return q
    return None
