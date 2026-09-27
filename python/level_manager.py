import os
import sqlite3
import pandas as pd
from typing import List, Dict, Any

LEVELS_DATA = [
    {
        "level": 1,
        "level_title": "Level 1: Syntax & Variable Foundations",
        "challenges": [
            {
                "id": "L1_C1",
                "title": "Challenge 1.1: The Missing Colon",
                "description": "Fix the syntax error in the conditional statement. The code should check if `temperature` is above 30 and print `'It is hot outside!'`.",
                "starter_code": "temperature = 35\nif temperature > 30\n    print('It is hot outside!')",
                "expected_output": "It is hot outside!",
                "hint": "Python conditional statements (`if`, `else`, `elif`) must end with a colon `:`.",
                "target_concept": "Syntax & Formatting Rules",
                "xp": 100
            },
            {
                "id": "L1_C2",
                "title": "Challenge 1.2: Misaligned Indentation",
                "description": "Fix the indentation error inside the function definition. The print statement must be properly indented by 4 spaces.",
                "starter_code": "def calculate_discount(price):\nfinal_price = price * 0.9\nprint(f'Discounted price: ${final_price:.2f}')\n\ncalculate_discount(100)",
                "expected_output": "Discounted price: $90.00",
                "hint": "Python uses 4-space indentation to define code blocks inside functions.",
                "target_concept": "Code Block Indentation",
                "xp": 100
            },
            {
                "id": "L1_C3",
                "title": "Challenge 1.3: Undefined Variable Scope",
                "description": "The program tries to calculate a total bill, but references a variable that hasn't been defined yet. Fix the variable name or assignment.",
                "starter_code": "item_price = 45.0\ntax = 5.0\ntotal_bill = item_price + tax_rate\nprint(f'Total bill: ${total_bill:.2f}')",
                "expected_output": "Total bill: $50.00",
                "hint": "Check the exact spelling of `tax` vs `tax_rate`.",
                "target_concept": "Variable Scope & Naming",
                "xp": 100
            }
        ]
    },
    {
        "level": 2,
        "level_title": "Level 2: Data Structures & Indexing Mastery",
        "challenges": [
            {
                "id": "L2_C1",
                "title": "Challenge 2.1: List Index Out of Range",
                "description": "The code attempts to fetch the 4th item from a 3-item list. Fix the index so it prints the last fruit in the list (`'cherry'`).",
                "starter_code": "fruits = ['apple', 'banana', 'cherry']\nprint(fruits[3])",
                "expected_output": "cherry",
                "hint": "Python uses 0-based indexing! A list of length 3 has indexes 0, 1, and 2.",
                "target_concept": "List Indexing",
                "xp": 150
            },
            {
                "id": "L2_C2",
                "title": "Challenge 2.2: Missing Dictionary Key",
                "description": "The user lookup code crashes because `'email'` does not exist in the dictionary. Fix it to safely look up `'email'` using `.get()` with a default value of `'Not Provided'`.",
                "starter_code": "user = {'id': 101, 'name': 'Sarah'}\nprint(user['email'])",
                "expected_output": "Not Provided",
                "hint": "Use `dict.get(key, default)` instead of bracket indexing `dict[key]`.",
                "target_concept": "Dictionary Lookup",
                "xp": 150
            },
            {
                "id": "L2_C3",
                "title": "Challenge 2.3: Modifying Immutable Sequences",
                "description": "Tuples cannot be changed after creation. Modify the code to use a list instead of a tuple so the element at index 0 can be updated to `'blue'`. Print the updated collection.",
                "starter_code": "colors = ('red', 'green')\ncolors[0] = 'blue'\nprint(colors)",
                "expected_output": "['blue', 'green']",
                "hint": "Use square brackets `[]` to create a mutable list instead of parentheses `()`.",
                "target_concept": "Type Compatibility & Casting",
                "xp": 150
            }
        ]
    },
    {
        "level": 3,
        "level_title": "Level 3: Type Systems & Value Constraints",
        "challenges": [
            {
                "id": "L3_C1",
                "title": "Challenge 3.1: String & Number Concatenation",
                "description": "Fix the type error when concatenating a string with an integer. Use string conversion or f-strings to print `'User score: 95'`.",
                "starter_code": "score = 95\nmessage = 'User score: ' + score\nprint(message)",
                "expected_output": "User score: 95",
                "hint": "Convert `score` using `str(score)` or use an f-string `f'User score: {score}'`.",
                "target_concept": "Type Compatibility & Casting",
                "xp": 200
            },
            {
                "id": "L3_C2",
                "title": "Challenge 3.2: Invalid Integer Conversion",
                "description": "Converting text with letters into an integer raises a `ValueError`. Add a check or fix the input string `'100'` so `int()` succeeds.",
                "starter_code": "raw_input = '$100'\nclean_number = int(raw_input)\nprint(clean_number * 2)",
                "expected_output": "200",
                "hint": "Remove the non-numeric character `$` using `.replace('$', '')` before converting to int.",
                "target_concept": "Value & Argument Constraints",
                "xp": 200
            },
            {
                "id": "L3_C3",
                "title": "Challenge 3.3: Invalid Method on Data Type",
                "description": "Lists do not have a `.strip()` method (which is a string method). Fix the code so it strips whitespace from the string before appending to the list.",
                "starter_code": "data = ['  hello  ', '  world  ']\ncleaned = data.strip()\nprint(cleaned)",
                "expected_output": "['hello', 'world']",
                "hint": "Use a list comprehension or loop: `[item.strip() for item in data]`.",
                "target_concept": "Object Attributes & Methods",
                "xp": 200
            }
        ]
    },
    {
        "level": 4,
        "level_title": "Level 4: Control Flow, Functions & Arithmetic",
        "challenges": [
            {
                "id": "L4_C1",
                "title": "Challenge 4.1: Safe Division Guard",
                "description": "Calculating the average of an empty list leads to `ZeroDivisionError`. Add a check to return `0.0` if the list is empty, otherwise calculate the average.",
                "starter_code": "def get_average(numbers):\n    return sum(numbers) / len(numbers)\n\nscores = []\nprint(get_average(scores))",
                "expected_output": "0.0",
                "hint": "Check `if not numbers:` or `if len(numbers) == 0:` before dividing.",
                "target_concept": "Arithmetic Operations",
                "xp": 250
            },
            {
                "id": "L4_C2",
                "title": "Challenge 4.2: Function Return & Scope",
                "description": "The function calculates `result`, but doesn't return it, causing `print(multiply(4, 5))` to print `None`. Fix the function to return the result.",
                "starter_code": "def multiply(a, b):\n    res = a * b\n\nans = multiply(4, 5)\nprint(ans)",
                "expected_output": "20",
                "hint": "Use the `return` statement inside the function.",
                "target_concept": "Variable Scope & Naming",
                "xp": 250
            }
        ]
    },
    {
        "level": 5,
        "level_title": "Level 5: Advanced & Real-World Debugging",
        "challenges": [
            {
                "id": "L5_C1",
                "title": "Challenge 5.1: File Handling & Exception Safety",
                "description": "Opening a non-existent file causes `FileNotFoundError`. Implement a `try-except` block to catch `FileNotFoundError` and print `'File missing'`.",
                "starter_code": "try:\n    f = open('config_data.txt', 'r')\n    print(f.read())\nexcept:\n    pass",
                "expected_output": "File missing",
                "hint": "Catch `FileNotFoundError` explicitly and print `'File missing'`.",
                "target_concept": "File Handling & Paths",
                "xp": 300
            },
            {
                "id": "L5_C2",
                "title": "Challenge 5.2: Safe Loop Bounds & Accumulation",
                "description": "Sum the elements of `vals = [10, 20, 30]` using a `range(len(vals))` loop without going out of bounds. Print the final total.",
                "starter_code": "vals = [10, 20, 30]\ntotal = 0\nfor i in range(len(vals) + 1):\n    total += vals[i]\nprint(total)",
                "expected_output": "60",
                "hint": "`range(len(vals))` goes from 0 up to `len(vals) - 1`. Do not add `+ 1` to `len(vals)`.",
                "target_concept": "List Indexing",
                "xp": 300
            }
        ]
    }
]

class LevelManager:
    """
    Manages user level progression, challenge completion tracking, XP, and badges.
    """

    def __init__(self, db_path: str = "codebreak.db"):
        self.db_path = db_path
        self._init_level_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_level_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(user_progress)")
            cols = [info[1] for info in cursor.fetchall()]
            if cols and "username" not in cols:
                cursor.execute("DROP TABLE user_progress")
                conn.commit()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    username TEXT PRIMARY KEY,
                    xp INTEGER DEFAULT 0,
                    easy_completed INTEGER DEFAULT 0,
                    medium_completed INTEGER DEFAULT 0,
                    hard_completed INTEGER DEFAULT 0,
                    total_completed INTEGER DEFAULT 0,
                    streak INTEGER DEFAULT 1,
                    current_level INTEGER DEFAULT 1,
                    completed_challenges TEXT DEFAULT '',
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def get_user_progress(self, student_id: str) -> Dict[str, Any]:
        student_id = student_id.strip().lower() if student_id else "anonymous"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT current_level, xp, completed_challenges FROM user_progress WHERE username = ?",
                (student_id,)
            )
            row = cursor.fetchone()
            if not row:
                cursor.execute(
                    "INSERT INTO user_progress (username, current_level, xp, completed_challenges) VALUES (?, 1, 0, '')",
                    (student_id,)
                )
                conn.commit()
                return {"student_id": student_id, "current_level": 1, "xp": 0, "completed": []}
            
            completed_str = row[2] if row[2] else ""
            completed_list = [c.strip() for c in completed_str.split(",") if c.strip()]
            return {
                "student_id": student_id,
                "current_level": row[0],
                "xp": row[1],
                "completed": completed_list
            }

    def mark_challenge_completed(self, student_id: str, challenge_id: str, xp_earned: int) -> Dict[str, Any]:
        progress = self.get_user_progress(student_id)
        completed = set(progress["completed"])
        
        is_new = challenge_id not in completed
        if is_new:
            completed.add(challenge_id)
            new_xp = progress["xp"] + xp_earned
            completed_str = ",".join(completed)
            
            count_completed = len(completed)
            new_level = max(1, min(5, (count_completed // 2) + 1))
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE user_progress
                    SET current_level = ?, xp = ?, completed_challenges = ?, last_active = CURRENT_TIMESTAMP
                    WHERE username = ?
                """, (new_level, new_xp, completed_str, student_id))
                conn.commit()

            return {
                "new_xp": new_xp,
                "new_level": new_level,
                "xp_earned": xp_earned,
                "is_level_up": new_level > progress["current_level"],
                "completed_count": len(completed)
            }
        
        return {
            "new_xp": progress["xp"],
            "new_level": progress["current_level"],
            "xp_earned": 0,
            "is_level_up": False,
            "completed_count": len(completed)
        }

    def get_all_levels(self) -> List[Dict[str, Any]]:
        return LEVELS_DATA

    def get_challenge_by_id(self, challenge_id: str) -> Dict[str, Any]:
        for lvl in LEVELS_DATA:
            for ch in lvl["challenges"]:
                if ch["id"] == challenge_id:
                    return ch
        return None
