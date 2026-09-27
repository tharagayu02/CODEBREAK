import re
import string

class DataPreprocessor:
    """
    NLP Preprocessing module for CodeBreak.
    Cleans error messages, normalizes text, tokenizes, and extracts code syntax features.
    """

    def __init__(self):
        # Common Python keywords and syntax indicators
        self.code_keywords = [
            'def', 'class', 'for', 'while', 'if', 'else', 'elif', 'try', 'except',
            'import', 'from', 'return', 'raise', 'with', 'open', 'read', 'write',
            'len', 'int', 'str', 'float', 'list', 'dict', 'set', 'tuple', 'range',
            'append', 'pop', 'strip', 'split', 'index', 'get'
        ]

    def clean_error_message(self, error_msg: str) -> str:
        """
        Cleans and normalizes an error message.
        Removes file paths, line numbers, memory addresses, and normalizes spacing.
        """
        if not error_msg or not isinstance(error_msg, str):
            return "unknown error"

        msg = error_msg.strip()
        # Remove traceback path lines (e.g., File "c:/path/to/file.py", line 12 or File 'app.py', line 15)
        msg = re.sub(r"File ['\"].*?['\"], line \d+.*", '', msg, flags=re.IGNORECASE)
        # Remove line references (e.g., line 5)
        msg = re.sub(r'line \d+', '', msg, flags=re.IGNORECASE)
        # Remove hex memory addresses (e.g. 0x7fa8b9c)
        msg = re.sub(r'0x[0-9a-fA-F]+', '', msg)
        # Lowercase
        msg = msg.lower()
        # Normalize multiple whitespace
        msg = re.sub(r'\s+', ' ', msg).strip()

        return msg

    def extract_code_tokens(self, code_snippet: str) -> str:
        """
        Processes a code snippet to extract syntax elements, special tokens, and identifier patterns.
        """
        if not code_snippet or not isinstance(code_snippet, str):
            return ""

        code = code_snippet.strip()
        tokens = []

        # Check for indexing / bracket access patterns
        if re.search(r'\[.*?\]', code):
            tokens.append('FEATURE_INDEXING_BRACKET')

        # Check for dict key access or literal
        if '{' in code and '}' in code:
            tokens.append('FEATURE_DICT_LITERAL')

        # Check for string concatenation or type cast
        if '+' in code and ("'" in code or '"' in code):
            tokens.append('FEATURE_STR_CONCAT')

        # Check for function call pattern
        if re.search(r'\b\w+\([^)]*\)', code):
            tokens.append('FEATURE_FUNC_CALL')

        # Check for division / modulo
        if '/' in code or '%' in code or '//' in code:
            tokens.append('FEATURE_DIVISION_OPERATOR')

        # Check for file open / read pattern
        if 'open(' in code or '.read(' in code or '.write(' in code:
            tokens.append('FEATURE_FILE_IO')

        # Check for dot attribute access pattern
        if re.search(r'\.\w+', code):
            tokens.append('FEATURE_DOT_ACCESS')

        # Tokenize code text into identifiers
        raw_words = re.findall(r'\b[a-zA-Z_]\w*\b', code.lower())
        tokens.extend(raw_words)

        return " ".join(tokens)

    def prepare_combined_text(self, error_message: str, code_snippet: str) -> str:
        """
        Combines processed error message and extracted code tokens into a single text document for NLP.
        """
        cleaned_err = self.clean_error_message(error_message)
        code_toks = self.extract_code_tokens(code_snippet)
        
        return f"{cleaned_err} {code_toks}".strip()


if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    sample_err = "IndexError: list index out of range at File 'app.py', line 15"
    sample_code = "numbers = [1, 2, 3]\nprint(numbers[5])"

    cleaned = preprocessor.clean_error_message(sample_err)
    combined = preprocessor.prepare_combined_text(sample_err, sample_code)

    print("Cleaned Error:", cleaned)
    print("Combined Text:", combined)
