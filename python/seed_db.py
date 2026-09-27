import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from python.database import StudentDatabase
from python.r_runner import RRunner

db = StudentDatabase("codebreak.db")

attempts_data = [
    ("S001", "arr = [10, 20]\nprint(arr[5])", "IndexError", "IndexError: list index out of range", "List Indexing", 95.0, "Index error; bracket"),
    ("S001", "user = {'name': 'Alice'}\nprint(user['age'])", "KeyError", "KeyError: 'age'", "Dictionary Lookup", 92.0, "Key error; dictionary"),
    ("S001", "age = 20\nmsg = 'I am ' + age", "TypeError", "TypeError: can only concatenate str (not \"int\") to str", "Type Compatibility & Casting", 96.5, "Type mismatch; string concat"),
    ("S001", "val = 10 / 0", "ZeroDivisionError", "ZeroDivisionError: division by zero", "Arithmetic Operations", 99.0, "Zero division"),
    ("S001", "def greet():\nprint('hi')", "IndentationError", "IndentationError: expected an indented block", "Code Block Indentation", 98.0, "Indentation error"),
    ("S001", "print(total_cost)", "NameError", "NameError: name 'total_cost' is not defined", "Variable Scope & Naming", 97.0, "Undefined variable"),
    ("S001", "f = open('missing.txt', 'r')", "FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'", "File Handling & Paths", 99.5, "File missing"),
    ("S001", "num = int('abc')", "ValueError", "ValueError: invalid literal for int() with base 10: 'abc'", "Value & Argument Constraints", 94.0, "Invalid int literal"),
    ("S001", "lst = []\nlst.strip()", "AttributeError", "AttributeError: 'list' object has no attribute 'strip'", "Object Attributes & Methods", 96.0, "Attribute error"),
]

for student_id, code, err_type, err_msg, concept, conf, sigs in attempts_data:
    db.log_attempt(student_id, code, err_type, err_msg, concept, conf, sigs)

csv_path = db.export_all_history_csv()
print(f"Exported database attempts to {csv_path}")

runner = RRunner()
res = runner.run_analysis(csv_path)
print("RRunner Status:", res["status"])
