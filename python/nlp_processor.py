import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
try:
    from python.data_preprocessing import DataPreprocessor
except ImportError:
    from data_preprocessing import DataPreprocessor

class NLPProcessor:
    """
    NLP Processor module for vectorizing programming error text and code tokens using TF-IDF.
    """

    def __init__(self, max_features: int = 150, ngram_range: tuple = (1, 2)):
        self.preprocessor = DataPreprocessor()
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True
        )
        self.is_fitted = False

    def fit(self, error_messages: list, code_snippets: list):
        """
        Fits the TF-IDF vectorizer on combined error messages and code snippets.
        """
        combined_texts = [
            self.preprocessor.prepare_combined_text(err, code)
            for err, code in zip(error_messages, code_snippets)
        ]
        self.vectorizer.fit(combined_texts)
        self.is_fitted = True
        return self

    def transform(self, error_messages: list, code_snippets: list):
        """
        Transforms input error messages and code snippets into TF-IDF numerical vectors.
        """
        if not self.is_fitted:
            raise ValueError("NLPProcessor vectorizer is not fitted yet! Call fit() or load_vectorizer() first.")

        combined_texts = [
            self.preprocessor.prepare_combined_text(err, code)
            for err, code in zip(error_messages, code_snippets)
        ]
        return self.vectorizer.transform(combined_texts).toarray()

    def fit_transform(self, error_messages: list, code_snippets: list):
        self.fit(error_messages, code_snippets)
        return self.transform(error_messages, code_snippets)

    def save_vectorizer(self, filepath: str = "models/tfidf_vectorizer.pkl"):
        """
        Saves the fitted TF-IDF vectorizer to disk.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.vectorizer, filepath)
        print(f"TF-IDF Vectorizer successfully saved to {filepath}")

    def load_vectorizer(self, filepath: str = "models/tfidf_vectorizer.pkl"):
        """
        Loads a pre-trained TF-IDF vectorizer from disk.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Vectorizer file not found at {filepath}")
        self.vectorizer = joblib.load(filepath)
        self.is_fitted = True
        print(f"TF-IDF Vectorizer loaded from {filepath}")
        return self

    def get_feature_names(self):
        if self.is_fitted:
            return self.vectorizer.get_feature_names_out()
        return []


if __name__ == "__main__":
    df = pd.read_csv("data/concept_error_dataset.csv")
    nlp = NLPProcessor()
    X_tfidf = nlp.fit_transform(df['error_message'], df['code_snippet'])
    print(f"Fitted TF-IDF matrix shape: {X_tfidf.shape}")
    nlp.save_vectorizer()
