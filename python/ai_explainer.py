import os
import json

class AIConceptExplainer:
    """
    AI / Pedagogical Explanation Engine for CodeBreak.
    Generates beginner-friendly explanations, corrected code, example snippets,
    practice questions, and safe guidance without overriding ML predictions.
    """

    CONCEPT_KNOWLEDGE_BASE = {
        "List Indexing": {
            "what_happened": "Your code tried to access an element at an index position that does not exist in the list.",
            "why_it_happened": "In Python, list indexes start at 0. If a list has 3 items, valid indexes are 0, 1, and 2. Accessing index 3 triggers an `IndexError`.",
            "why_mistake_made": "You may have forgotten that Python uses 0-based indexing or mistakenly passed the list length `len(lst)` as an index.",
            "corrected_code": "items = [10, 20, 30]\n# Correct: Last element is at index len(items) - 1\nprint(items[2])  # Prints 30",
            "simple_example": "fruits = ['apple', 'banana']\nprint(fruits[0]) # 'apple'\nprint(fruits[1]) # 'banana'",
            "practice_questions": [
                "1. If a list has 5 elements, what is the valid range of positive index numbers?",
                "2. Fix the error: `colors = ['red', 'blue']; print(colors[2])`",
                "3. How do you safely check if an index exists before accessing a list?",
                "4. What index number retrieves the last element of any non-empty list in Python?"
            ],
            "recommendation": "Review 0-based indexing and boundary conditions when accessing list items in loops."
        },
        "Dictionary Lookup": {
            "what_happened": "Your code attempted to look up a key in a dictionary that does not exist.",
            "why_it_happened": "When accessing `dict[key]`, Python expects `key` to already be stored in the dictionary. If missing, it raises a `KeyError`.",
            "why_mistake_made": "You might have misspelled the key name, assumed a default value existed, or forgotten to check if the key was present.",
            "corrected_code": "person = {'name': 'Alice'}\n# Safe lookup using .get()\nprint(person.get('age', 'Not Specified'))",
            "simple_example": "student = {'id': 101, 'grade': 'A'}\nprint(student['id'])  # 101\nprint(student.get('name')) # None (No KeyError)",
            "practice_questions": [
                "1. What is the difference between `d['key']` and `d.get('key')` in Python?",
                "2. Fix the error: `user = {'name': 'Bob'}; print(user['email'])`",
                "3. Write code using the `in` operator to check if `'score'` exists in dictionary `data`.",
                "4. How do you provide a default value when a dictionary key is missing?"
            ],
            "recommendation": "Use `.get(key, default)` or `if key in dict:` to safely retrieve dictionary values."
        },
        "Type Compatibility & Casting": {
            "what_happened": "An operation was attempted between incompatible data types (e.g. adding integer to string).",
            "why_it_happened": "Python is strongly typed and will not automatically convert text strings into numbers during arithmetic operations or string concatenation.",
            "why_mistake_made": "You may have combined user input (which returns strings) with numbers without explicit conversion using `int()` or `str()`.",
            "corrected_code": "age = 20\n# Convert number to string for concatenation or use f-strings\nmsg = 'I am ' + str(age)\n# Or better:\nmsg = f'I am {age}'",
            "simple_example": "x = '10'\ny = 5\ntotal = int(x) + y # 15",
            "practice_questions": [
                "1. Why does `'5' + 5` cause a `TypeError` in Python?",
                "2. Fix the error: `score = 95; print('Score: ' + score)`",
                "3. How do you convert user input from `input()` into a float number?",
                "4. Rewrite `print('Age: ' + str(25))` using an f-string."
            ],
            "recommendation": "Practice using f-strings (`f'{variable}'`) or explicit type casting functions `int()`, `float()`, `str()`."
        },
        "Variable Scope & Naming": {
            "what_happened": "Your code tried to use a variable or function name that has not been defined or is out of scope.",
            "why_it_happened": "Python could not find a local or global variable with that exact identifier name in the current execution scope.",
            "why_mistake_made": "You may have misspelled the variable name (Python is case-sensitive), declared it inside a function body, or forgotten an import statement.",
            "corrected_code": "total_score = 100\n# Ensure variable name spelling matches exactly\nprint(total_score)",
            "simple_example": "def calculate():\n    val = 50\n    return val\nresult = calculate()\nprint(result)",
            "practice_questions": [
                "1. Is `UserName` considered the same variable as `user_name` in Python?",
                "2. Why can't a variable declared inside a function be accessed outside that function by default?",
                "3. Fix the error: `import math\nprint(sqrt(16))`",
                "4. How do you fix a `NameError` caused by a missing variable assignment?"
            ],
            "recommendation": "Check variable name spelling carefully and verify that variables are defined before they are used."
        },
        "Value & Argument Constraints": {
            "what_happened": "A function received an argument that had the right type, but an invalid value (e.g. `int('abc')`).",
            "why_it_happened": "The function expected data formatted in a specific range or structure, but received unusable input values.",
            "why_mistake_made": "You may have passed non-numeric text to `int()`, attempted to remove an item not in a list, or unpacked the wrong number of items.",
            "corrected_code": "text = '123'\nif text.isdigit():\n    num = int(text)\nelse:\n    num = 0",
            "simple_example": "items = ['a', 'b']\nif 'c' in items:\n    items.remove('c')",
            "practice_questions": [
                "1. What string values can be safely converted using `int()`?",
                "2. Fix the error: `items = ['x']; items.remove('y')`",
                "3. How do you prevent a `ValueError` when unpacking a tuple of unknown size?",
                "4. Write code that validates user input before calling `int()`."
            ],
            "recommendation": "Validate inputs with conditional checks (`.isdigit()`, `if item in list`) before calling conversion methods."
        },
        "Syntax & Formatting Rules": {
            "what_happened": "Your code contains invalid Python syntax structure (missing colon, unmatched parentheses, quote mismatch).",
            "why_it_happened": "Python parser encountered a token that violates Python language syntax rules.",
            "why_mistake_made": "Common syntax oversights include omitting the `:` at the end of `if`/`for`/`def` statements or leaving quotes unclosed.",
            "corrected_code": "# Include colon at the end of conditional header\nif x == 5:\n    print('x is 5')",
            "simple_example": "for i in range(3):\n    print(i)",
            "practice_questions": [
                "1. What symbol must end every `if`, `for`, `while`, and `def` header line in Python?",
                "2. Fix the error: `def greet()\n    print('Hello')`",
                "3. How do you fix an 'EOL while scanning string literal' error?",
                "4. Explain why `5 = x` is invalid syntax in Python."
            ],
            "recommendation": "Pay attention to line endings, closing brackets, and matching quotation marks."
        },
        "Code Block Indentation": {
            "what_happened": "Your code has incorrect tab or space alignment inside a block (e.g. function, loop, or conditional).",
            "why_it_happened": "Python uses indentation (4 spaces) rather than curly braces `{}` to define code blocks.",
            "why_mistake_made": "You may have mixed tabs and spaces, or forgotten to indent statements following an `if`, `for`, `while`, or `def` line.",
            "corrected_code": "def my_func():\n    # Indented 4 spaces inside function block\n    print('Inside function')",
            "simple_example": "if True:\n    print('Indented correctly')",
            "practice_questions": [
                "1. How many spaces are standard for one level of Python indentation?",
                "2. Fix the error: `if True:\nprint('hello')`",
                "3. What happens when you mix tabs and spaces in the same Python file?",
                "4. How do you indent multiple lines in VS Code / Python IDEs?"
            ],
            "recommendation": "Ensure consistent 4-space indentation for every code block."
        },
        "Object Attributes & Methods": {
            "what_happened": "Your code called a method or attribute that does not exist on the target object (e.g., calling `.append()` on a string).",
            "why_it_happened": "Different data types support different built-in methods. Calling a list method on a string or `NoneType` causes an `AttributeError`.",
            "why_mistake_made": "You may have confused string and list methods, or forgotten that a function returned `None` instead of an object.",
            "corrected_code": "text = 'hello'\n# Strings are immutable; concatenation creates a new string\ntext = text + '!'",
            "simple_example": "numbers = [1, 2]\nnumbers.append(3) # Lists support .append()",
            "practice_questions": [
                "1. Can you use `.append()` on a string in Python? What should you use instead?",
                "2. Fix the error: `res = None; res.strip()`",
                "3. How can you inspect all valid methods on an object using `dir()`?",
                "4. What method splits a string into a list of words?"
            ],
            "recommendation": "Check object types using `type(obj)` and verify supported methods in Python documentation."
        },
        "Arithmetic Operations": {
            "what_happened": "Your code attempted division or modulo by zero (`/ 0`, `% 0`).",
            "why_it_happened": "Division by zero is mathematically undefined and raises a `ZeroDivisionError` in Python.",
            "why_mistake_made": "You may have passed an empty list to `sum(lst)/len(lst)` where `len()` evaluated to 0, or calculated a variable that became 0.",
            "corrected_code": "counts = []\nif len(counts) > 0:\n    avg = sum(counts) / len(counts)\nelse:\n    avg = 0.0",
            "simple_example": "divisor = 0\nresult = 10 / divisor if divisor != 0 else 0",
            "practice_questions": [
                "1. Why does `10 / 0` raise an exception in Python?",
                "2. Fix the error: `def mean(vals): return sum(vals) / len(vals); mean([])`",
                "3. How can a conditional ternary operator prevent zero division?",
                "4. What does `10 % 0` evaluate to?"
            ],
            "recommendation": "Always check if the denominator variable is non-zero before dividing."
        },
        "File Handling & Paths": {
            "what_happened": "Python could not find the specified file at the given filepath.",
            "why_it_happened": "The file does not exist in the working directory, or the relative path is specified incorrectly.",
            "why_mistake_made": "You may have misspelled the filename, assumed the script runs from a different folder, or forgotten to create the file first.",
            "corrected_code": "import os\nfilename = 'data.txt'\nif os.path.exists(filename):\n    with open(filename, 'r') as f:\n        content = f.read()\nelse:\n    print(f'File {filename} not found.')",
            "simple_example": "with open('example.txt', 'w') as f:\n    f.write('Hello')",
            "practice_questions": [
                "1. What is the difference between a relative path and an absolute path?",
                "2. How do you check if a file exists before calling `open()`?",
                "3. Fix the error: `f = open('nonexistent.txt', 'r')`",
                "4. Why is using the `with open(...) as f:` syntax recommended?"
            ],
            "recommendation": "Use `os.path.exists()` or absolute paths, and use `with open(...)` statements to manage file resources."
        }
    }

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")

    def generate_explanation(self, prediction_result: dict) -> dict:
        """
        Main entry point for generating AI pedagogical guidance.
        """
        predicted_concept = prediction_result.get("predicted_concept", "List Indexing")
        confidence = prediction_result.get("confidence", 85.0)
        is_uncertain = prediction_result.get("is_uncertain", False)
        student_id = prediction_result.get("student_id", "S001")
        error_type = prediction_result.get("error_type", "IndexError")
        code_snippet = prediction_result.get("code_snippet", "")
        error_message = prediction_result.get("error_message", "")
        signals = prediction_result.get("signals", [])

        # Fetch knowledge base fallback
        kb = self.CONCEPT_KNOWLEDGE_BASE.get(predicted_concept, self.CONCEPT_KNOWLEDGE_BASE["List Indexing"])

        # Base explanation payload
        explanation_payload = {
            "predicted_concept": predicted_concept,
            "confidence": confidence,
            "safety_disclaimer": "Prediction estimated by Machine Learning model.",
            "status_label": "Prediction uncertain – please review multiple possible concepts." if is_uncertain else "High Confidence",
            "what_happened": kb["what_happened"],
            "why_it_happened": kb["why_it_happened"],
            "why_mistake_made": kb["why_mistake_made"],
            "corrected_code": kb["corrected_code"],
            "simple_example": kb["simple_example"],
            "practice_questions": kb["practice_questions"],
            "learning_recommendation": f"You may need more practice with {predicted_concept}. {kb['recommendation']}",
            "signals": signals
        }

        return explanation_payload


if __name__ == "__main__":
    explainer = AIConceptExplainer()
    test_result = {
        "predicted_concept": "List Indexing",
        "confidence": 88.5,
        "is_uncertain": False,
        "student_id": "S001",
        "error_type": "IndexError",
        "code_snippet": "arr = [1, 2]\nprint(arr[5])",
        "error_message": "IndexError: list index out of range",
        "signals": ["Error Type: IndexError", "Bracket Indexing Operator `[]` detected"]
    }
    exp = explainer.generate_explanation(test_result)
    print("\nGenerated AI Explanation:")
    print("Concept:", exp["predicted_concept"])
    print("Recommendation:", exp["learning_recommendation"])
    print("Practice Questions:", len(exp["practice_questions"]))
