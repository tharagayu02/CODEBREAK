import os
import unittest
import pandas as pd
import numpy as np

from python.data_preprocessing import DataPreprocessor
from python.nlp_processor import NLPProcessor
from python.feature_engineering import FeatureEngineer
from python.database import StudentDatabase
from python.predict import ConceptGapPredictor
from python.ai_explainer import AIConceptExplainer
from python.r_runner import RRunner

class TestCodeBreakPipeline(unittest.TestCase):
    """
    Comprehensive test suite for the CodeBreak system.
    """

    @classmethod
    def setUpClass(cls):
        cls.preprocessor = DataPreprocessor()
        cls.db = StudentDatabase("test_codebreak.db")
        cls.predictor = ConceptGapPredictor(db_path="test_codebreak.db")
        cls.explainer = AIConceptExplainer()
        cls.r_runner = RRunner()

    def test_1_nlp_preprocessing(self):
        err = "IndexError: list index out of range at File 'app.py', line 15"
        cleaned = self.preprocessor.clean_error_message(err)
        self.assertNotIn("line 15", cleaned)
        self.assertNotIn("app.py", cleaned)
        self.assertIn("indexerror", cleaned)

        code = "arr = [1, 2]\nprint(arr[5])"
        tokens = self.preprocessor.extract_code_tokens(code)
        self.assertIn("FEATURE_INDEXING_BRACKET", tokens)

    def test_2_database_operations(self):
        self.db.log_attempt(
            student_id="S_TEST",
            code="x = 5 / 0",
            error_type="ZeroDivisionError",
            error_message="ZeroDivisionError: division by zero",
            predicted_concept="Arithmetic Operations",
            confidence=95.0,
            signals="Zero division operator"
        )
        df = self.db.get_student_history("S_TEST")
        self.assertGreaterEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['error_type'], "ZeroDivisionError")

        metrics = self.db.get_student_history_metrics("S_TEST")
        self.assertGreaterEqual(metrics['num_previous_errors'], 1)

    def test_3_predict_across_all_error_types(self):
        test_cases = [
            ("IndexError: list index out of range", "lst = [10]\nprint(lst[2])", "List Indexing"),
            ("KeyError: 'user'", "d = {}\nprint(d['user'])", "Dictionary Lookup"),
            ("TypeError: can only concatenate str (not \"int\") to str", "msg = 'val' + 5", "Type Compatibility & Casting"),
            ("NameError: name 'x' is not defined", "print(x)", "Variable Scope & Naming"),
            ("ValueError: invalid literal for int() with base 10: 'abc'", "num = int('abc')", "Value & Argument Constraints"),
            ("SyntaxError: invalid syntax", "if x == 5\n pass", "Syntax & Formatting Rules"),
            ("IndentationError: expected an indented block", "def foo():\npass", "Code Block Indentation"),
            ("AttributeError: 'list' object has no attribute 'strip'", "lst = []\nlst.strip()", "Object Attributes & Methods"),
            ("ZeroDivisionError: division by zero", "val = 10 / 0", "Arithmetic Operations"),
            ("FileNotFoundError: [Errno 2] No such file or directory: 'a.txt'", "open('a.txt')", "File Handling & Paths"),
        ]

        for err_msg, code_snip, expected_concept in test_cases:
            res = self.predictor.predict_concept_gap(
                error_message=err_msg,
                code_snippet=code_snip,
                student_id="S_TEST"
            )
            self.assertIn("predicted_concept", res)
            self.assertGreaterEqual(res["confidence"], 0.0)
            self.assertLessEqual(res["confidence"], 100.0)

    def test_4_edge_cases_no_crash(self):
        # Empty error message
        res1 = self.predictor.predict_concept_gap("", "x = 1", student_id="S_TEST")
        self.assertIsNotNone(res1["predicted_concept"])

        # Empty code snippet
        res2 = self.predictor.predict_concept_gap("SyntaxError: invalid syntax", "", student_id="S_TEST")
        self.assertIsNotNone(res2["predicted_concept"])

        # Unknown error message
        res3 = self.predictor.predict_concept_gap("CustomUnknownError: something bad happened", "foo()", student_id="S_TEST")
        self.assertIsNotNone(res3["predicted_concept"])

    def test_5_ai_explainer_payload(self):
        dummy_pred = {
            "predicted_concept": "List Indexing",
            "confidence": 90.0,
            "is_uncertain": False,
            "student_id": "S_TEST",
            "error_type": "IndexError",
            "code_snippet": "arr[5]",
            "error_message": "IndexError",
            "signals": ["Bracket detected"]
        }
        exp = self.explainer.generate_explanation(dummy_pred)
        self.assertIn("what_happened", exp)
        self.assertIn("why_it_happened", exp)
        self.assertIn("corrected_code", exp)
        self.assertEqual(len(exp["practice_questions"]), 4)

    def test_6_r_runner_execution(self):
        csv_path = self.db.export_all_history_csv("data/processed/test_student_history.csv")
        res = self.r_runner.run_analysis(csv_path)
        self.assertEqual(res["status"], "success")

    @classmethod
    def tearDownClass(cls):
        try:
            if os.path.exists("test_codebreak.db"):
                os.remove("test_codebreak.db")
        except Exception:
            pass

if __name__ == "__main__":
    unittest.main()
