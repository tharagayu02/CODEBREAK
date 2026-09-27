import os
import pandas as pd

def generate_dataset():
    data = [
        # --- List Indexing (IndexError) ---
        ("IndexError", "IndexError: list index out of range", "numbers = [10, 20, 30]\nprint(numbers[3])", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: list index out of range", "items = ['apple', 'banana']\nfirst = items[5]", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: tuple index out of range", "coords = (10, 20)\nprint(coords[2])", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: list index out of range", "data = []\nval = data[0]", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: list assignment index out of range", "lst = [1, 2]\nlst[2] = 3", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: pop from empty list", "arr = []\nelem = arr.pop()", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: string index out of range", "text = 'hello'\nchar = text[10]", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: list index out of range", "scores = [90, 85, 92]\nfor i in range(len(scores) + 1):\n    print(scores[i])", "List Indexing", "Intermediate", "Python"),
        ("IndexError", "IndexError: list index out of range", "grid = [[1, 2], [3, 4]]\nprint(grid[2][0])", "List Indexing", "Intermediate", "Python"),
        ("IndexError", "IndexError: list index out of range", "names = ['Alice', 'Bob']\nlast = names[len(names)]", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: list index out of range", "values = [5, 10]\nidx = 3\nprint(values[idx])", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: string index out of range", "s = 'abc'\nprint(s[-4])", "List Indexing", "Beginner", "Python"),
        ("IndexError", "IndexError: list index out of range", "colors = ['red', 'green', 'blue']\nprint(colors[3])", "List Indexing", "Beginner", "Python"),

        # --- Dictionary Lookup (KeyError) ---
        ("KeyError", "KeyError: 'age'", "person = {'name': 'Alice'}\nprint(person['age'])", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'address'", "user = {'id': 101, 'role': 'admin'}\naddr = user['address']", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 0", "counts = {1: 'one', 2: 'two'}\nprint(counts[0])", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'score'", "student = {'name': 'Bob', 'grade': 'A'}\nval = student['score']", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'email'", "info = {'username': 'john'}\nemail = info.pop('email')", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'total'", "config = {'setting': 'on'}\nx = config['total']", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'gpa'", "records = {'S01': {'name': 'Sam'}}\nprint(records['S01']['gpa'])", "Dictionary Lookup", "Intermediate", "Python"),
        ("KeyError", "KeyError: 'item'", "inventory = {}\nitem_count = inventory['item']", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'key'", "data_dict = {'a': 1, 'b': 2}\nprint(data_dict['key'])", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'price'", "product = {'title': 'Laptop'}\nprice = product['price']", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'count'", "stats = {'clicks': 10}\nprint(stats['count'])", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'id'", "emp = {'name': 'Jane', 'dept': 'Sales'}\nprint(emp['id'])", "Dictionary Lookup", "Beginner", "Python"),
        ("KeyError", "KeyError: 'status'", "response = {'code': 200}\nprint(response['status'])", "Dictionary Lookup", "Beginner", "Python"),

        # --- Type Compatibility & Casting (TypeError) ---
        ("TypeError", "TypeError: can only concatenate str (not \"int\") to str", "age = 20\nmsg = 'I am ' + age", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: unsupported operand type(s) for +: 'int' and 'str'", "x = 5 + '10'", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: 'int' object is not callable", "count = 5\nresult = count()", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: 'list' object is not callable", "nums = [1, 2, 3]\nval = nums(0)", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: 'NoneType' object is not subscriptable", "res = None\nprint(res[0])", "Type Compatibility & Casting", "Intermediate", "Python"),
        ("TypeError", "TypeError: 'str' object cannot be interpreted as an integer", "for i in range('5'):\n    print(i)", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: unsupported operand type(s) for /: 'str' and 'int'", "val = '10' / 2", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: 'float' object is not iterable", "val = 3.14\nfor x in val:\n    print(x)", "Type Compatibility & Casting", "Intermediate", "Python"),
        ("TypeError", "TypeError: len() of unsized object", "x = 100\nprint(len(x))", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: 'tuple' object does not support item assignment", "tup = (1, 2)\ntup[0] = 5", "Type Compatibility & Casting", "Intermediate", "Python"),
        ("TypeError", "TypeError: unhashable type: 'list'", "d = {[1, 2]: 'val'}", "Type Compatibility & Casting", "Intermediate", "Python"),
        ("TypeError", "TypeError: can only concatenate list (not \"int\") to list", "lst = [1, 2]\nres = lst + 3", "Type Compatibility & Casting", "Beginner", "Python"),
        ("TypeError", "TypeError: missing 1 required positional argument", "def add(a, b):\n    return a + b\nadd(5)", "Type Compatibility & Casting", "Beginner", "Python"),

        # --- Variable Scope & Naming (NameError) ---
        ("NameError", "NameError: name 'x' is not defined", "print(x)", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'total_score' is not defined", "score1 = 10\nprint(total_score)", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'my_func' is not defined", "my_func()", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'counter' is not defined", "def inc():\n    counter += 1\ninc()", "Variable Scope & Naming", "Intermediate", "Python"),
        ("NameError", "NameError: name 'True_val' is not defined", "if True_val:\n    print('yes')", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'math' is not defined", "res = math.sqrt(16)", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'pd' is not defined", "df = pd.DataFrame()", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'result' is not defined", "def calc():\n    result = 42\ncalc()\nprint(result)", "Variable Scope & Naming", "Intermediate", "Python"),
        ("NameError", "NameError: name 'length' is not defined", "arr = [1, 2, 3]\nprint(lenght)", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'user_name' is not defined", "user_Name = 'Alice'\nprint(user_name)", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'input_data' is not defined", "data = input_data.strip()", "Variable Scope & Naming", "Beginner", "Python"),
        ("NameError", "NameError: name 'temp' is not defined", "print(temp)", "Variable Scope & Naming", "Beginner", "Python"),

        # --- Value & Argument Constraints (ValueError) ---
        ("ValueError", "ValueError: invalid literal for int() with base 10: 'abc'", "num = int('abc')", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: float() argument must be a string or a real number, not 'list'", "val = float([1, 2])", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: not enough values to unpack (expected 2, got 1)", "a, b = [10]", "Value & Argument Constraints", "Intermediate", "Python"),
        ("ValueError", "ValueError: too many values to unpack (expected 2, got 3)", "x, y = [1, 2, 3]", "Value & Argument Constraints", "Intermediate", "Python"),
        ("ValueError", "ValueError: list.remove(x): x not in list", "items = ['a', 'b']\nitems.remove('c')", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: substring not found", "text = 'hello'\nidx = text.index('z')", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: math domain error", "import math\nmath.sqrt(-1)", "Value & Argument Constraints", "Intermediate", "Python"),
        ("ValueError", "ValueError: invalid literal for int() with base 10: '12.5'", "n = int('12.5')", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: max() arg is an empty sequence", "vals = []\nprint(max(vals))", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: min() arg is an empty sequence", "data = []\nprint(min(data))", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: invalid literal for int() with base 10: ''", "x = int('')", "Value & Argument Constraints", "Beginner", "Python"),
        ("ValueError", "ValueError: dictionary update sequence element #0 has length 1; 2 is required", "d = dict(['a'])", "Value & Argument Constraints", "Intermediate", "Python"),

        # --- Syntax & Formatting Rules (SyntaxError) ---
        ("SyntaxError", "SyntaxError: invalid syntax", "if x == 5\n    print(x)", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: expected ':'", "def greet()\n    print('hi')", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: EOL while scanning string literal", "msg = 'Hello World", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: invalid syntax", "for i in range(5)\n    print(i)", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: unexpected EOF while parsing", "print('hello'", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: cannot assign to literal", "5 = x", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: invalid syntax", "while x < 10\n    x += 1", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: unmatched ')'", "res = (1 + 2))", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: closing parenthesis ']' does not match opening parenthesis '('", "arr = (1, 2, 3]", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: invalid syntax", "class Person\n    def __init__(self):\n        pass", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: invalid syntax", "try\n    x = 1\nexcept:\n    pass", "Syntax & Formatting Rules", "Beginner", "Python"),
        ("SyntaxError", "SyntaxError: invalid syntax", "return 5", "Syntax & Formatting Rules", "Beginner", "Python"),

        # --- Code Block Indentation (IndentationError) ---
        ("IndentationError", "IndentationError: expected an indented block", "def test():\nprint('hello')", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: unexpected indent", "x = 5\n  y = 10", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: unindent does not match any outer indentation level", "if True:\n    x = 1\n  y = 2", "Code Block Indentation", "Intermediate", "Python"),
        ("IndentationError", "IndentationError: expected an indented block after 'if' statement", "if x > 0:\nprint('pos')", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: expected an indented block after 'for' statement", "for i in range(3):\nprint(i)", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: expected an indented block after 'while' statement", "while count > 0:\ncount -= 1", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: unexpected indent", "  print('start')", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: expected an indented block after 'def' statement", "def foo():\npass", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: unindent does not match any outer indentation level", "for x in data:\n    if x:\n        print(x)\n      else:\n        pass", "Code Block Indentation", "Intermediate", "Python"),
        ("IndentationError", "IndentationError: expected an indented block after 'except' statement", "try:\n    x = 1\nexcept Exception:\nprint('err')", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: expected an indented block", "class Student:\npass", "Code Block Indentation", "Beginner", "Python"),
        ("IndentationError", "IndentationError: unexpected indent", "a = 1\n    b = 2", "Code Block Indentation", "Beginner", "Python"),

        # --- Object Attributes & Methods (AttributeError) ---
        ("AttributeError", "AttributeError: 'list' object has no attribute 'append_all'", "lst = [1, 2]\nlst.append_all([3, 4])", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'str' object has no attribute 'append'", "text = 'hello'\ntext.append('!')", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'NoneType' object has no attribute 'strip'", "val = None\nclean = val.strip()", "Object Attributes & Methods", "Intermediate", "Python"),
        ("AttributeError", "AttributeError: 'dict' object has no attribute 'add'", "d = {'a': 1}\nd.add('b')", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'int' object has no attribute 'lower'", "num = 42\nnum.lower()", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'Person' object has no attribute 'age'", "class Person:\n    def __init__(self, name):\n        self.name = name\np = Person('Alice')\nprint(p.age)", "Object Attributes & Methods", "Intermediate", "Python"),
        ("AttributeError", "AttributeError: 'tuple' object has no attribute 'sort'", "t = (3, 1, 2)\nt.sort()", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'module' object has no attribute 'sqr'", "import math\nmath.sqr(9)", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'list' object has no attribute 'split'", "words = ['a', 'b']\nwords.split(',')", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'NoneType' object has no attribute 'group'", "import re\nm = re.match('a', 'b')\nprint(m.group())", "Object Attributes & Methods", "Intermediate", "Python"),
        ("AttributeError", "AttributeError: 'set' object has no attribute 'append'", "s = {1, 2}\ns.append(3)", "Object Attributes & Methods", "Beginner", "Python"),
        ("AttributeError", "AttributeError: 'float' object has no attribute 'upper'", "f = 3.14\nf.upper()", "Object Attributes & Methods", "Beginner", "Python"),

        # --- Arithmetic Operations (ZeroDivisionError) ---
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "res = 10 / 0", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: integer division or modulo by zero", "val = 5 // 0", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: float division by zero", "val = 4.5 / 0.0", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: integer division or modulo by zero", "mod = 10 % 0", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "def avg(lst):\n    return sum(lst) / len(lst)\navg([])", "Arithmetic Operations", "Intermediate", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "x = 5\ny = 5\nprint(10 / (x - y))", "Arithmetic Operations", "Intermediate", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "rate = total / count\n# where count is 0", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "speed = dist / time\nprint(speed)", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "a = 0\nb = 100 / a", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "n = 0\nans = 1 % n", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "score = points / attempts\n# attempts = 0", "Arithmetic Operations", "Beginner", "Python"),
        ("ZeroDivisionError", "ZeroDivisionError: division by zero", "ratio = count1 / count2", "Arithmetic Operations", "Beginner", "Python"),

        # --- File Handling & Paths (FileNotFoundError) ---
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'", "f = open('data.txt', 'r')", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'config.json'", "with open('config.json') as f:\n    data = f.read()", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'missing.csv'", "import pandas as pd\ndf = pd.read_csv('missing.csv')", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: '/invalid/path/file.txt'", "f = open('/invalid/path/file.txt')", "File Handling & Paths", "Intermediate", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'output/log.txt'", "f = open('output/log.txt', 'r')", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'users.db'", "import sqlite3\nconn = sqlite3.connect('file:users.db?mode=ro', uri=True)", "File Handling & Paths", "Intermediate", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'notes.txt'", "open('notes.txt').readlines()", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'images/pic.png'", "from PIL import Image\nim = Image.open('images/pic.png')", "File Handling & Paths", "Intermediate", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'settings.ini'", "open('settings.ini', 'r')", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'test.py'", "f = open('test.py')", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'records.txt'", "with open('records.txt', 'r') as file:\n    content = file.read()", "File Handling & Paths", "Beginner", "Python"),
        ("FileNotFoundError", "FileNotFoundError: [Errno 2] No such file or directory: 'input.txt'", "file = open('input.txt')\nlines = file.readlines()", "File Handling & Paths", "Beginner", "Python"),
    ]

    columns = ["error_type", "error_message", "code_snippet", "concept", "difficulty", "language"]
    df = pd.DataFrame(data, columns=columns)
    
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)
    
    dataset_path = "data/concept_error_dataset.csv"
    df.to_csv(dataset_path, index=False)
    print(f"Dataset successfully created with {len(df)} samples across {df['error_type'].nunique()} error types and {df['concept'].nunique()} concepts.")
    print(f"Saved to {dataset_path}")

if __name__ == "__main__":
    generate_dataset()
