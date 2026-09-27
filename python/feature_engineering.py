import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
try:
    from python.nlp_processor import NLPProcessor
except ImportError:
    from nlp_processor import NLPProcessor

class FeatureEngineer:
    """
    Feature engineering module for CodeBreak.
    Extracts and combines:
    1. Error type categorical features (One-Hot Encoded)
    2. NLP TF-IDF text features from error message and code tokens
    3. Syntactic regex features from student code
    4. Student historical features (previous error count, concept frequencies, recency weighting)
    """

    KNOWN_ERROR_TYPES = [
        "IndexError", "KeyError", "TypeError", "NameError", "ValueError",
        "SyntaxError", "IndentationError", "AttributeError", "ZeroDivisionError", "FileNotFoundError"
    ]

    def __init__(self, nlp_processor: NLPProcessor = None):
        self.nlp_processor = nlp_processor or NLPProcessor()
        self.error_type_encoder = OneHotEncoder(
            categories=[self.KNOWN_ERROR_TYPES],
            handle_unknown='ignore',
            sparse_output=False
        )
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        """
        Fits vectorizer and categorical encoders on the training dataframe.
        """
        # Fit OneHotEncoder on error_type
        error_types = df[['error_type']]
        self.error_type_encoder.fit(error_types)

        # Fit NLPProcessor
        self.nlp_processor.fit(df['error_message'], df['code_snippet'])
        self.is_fitted = True
        return self

    def extract_syntactic_features(self, code_snippets: list) -> np.ndarray:
        """
        Extracts boolean/binary syntax flags directly from code snippets.
        """
        feats = []
        for code in code_snippets:
            if not isinstance(code, str):
                code = ""
            
            has_brackets = 1 if ('[' in code and ']' in code) else 0
            has_braces = 1 if ('{' in code and '}' in code) else 0
            has_dot = 1 if '.' in code else 0
            has_colon = 1 if ':' in code else 0
            has_div = 1 if ('/' in code or '%' in code) else 0
            has_quotes = 1 if ("'" in code or '"' in code) else 0

            feats.append([has_brackets, has_braces, has_dot, has_colon, has_div, has_quotes])

        return np.array(feats)

    def prepare_feature_matrix(
        self,
        df: pd.DataFrame,
        history_features: pd.DataFrame = None
    ) -> np.ndarray:
        """
        Builds the complete numerical feature matrix X.
        combining error_type OHE + TF-IDF + Syntax flags + Student history metrics.
        """
        if not self.is_fitted:
            raise ValueError("FeatureEngineer is not fitted yet! Call fit() or load_encoders() first.")

        # 1. Error Type One-Hot Encoding (shape: N x 10)
        err_types = df[['error_type']].copy()
        err_types['error_type'] = err_types['error_type'].apply(
            lambda x: x if x in self.KNOWN_ERROR_TYPES else self.KNOWN_ERROR_TYPES[0]
        )
        X_err_type = self.error_type_encoder.transform(err_types)

        # 2. TF-IDF features (shape: N x MaxFeatures)
        X_tfidf = self.nlp_processor.transform(df['error_message'], df['code_snippet'])

        # 3. Syntactic features (shape: N x 6)
        X_syntax = self.extract_syntactic_features(df['code_snippet'])

        # 4. Student History Features (shape: N x 5)
        # Features: [num_previous_errors, concept_error_freq, recent_error_freq, num_unique_error_types, recency_concept_weight]
        if history_features is not None:
            X_hist = history_features.to_numpy()
        else:
            # Default zero history for synthetic training dataset
            n_samples = len(df)
            X_hist = np.zeros((n_samples, 5))

        # Stack horizontally
        X_combined = np.hstack([X_err_type, X_tfidf, X_syntax, X_hist])
        return X_combined

    def save_encoders(self, filepath: str = "models/feature_encoder.pkl"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            'error_type_encoder': self.error_type_encoder,
            'nlp_processor': self.nlp_processor
        }, filepath)
        print(f"Feature encoders saved to {filepath}")

    def load_encoders(self, filepath: str = "models/feature_encoder.pkl"):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Feature encoder file not found at {filepath}")
        data = joblib.load(filepath)
        self.error_type_encoder = data['error_type_encoder']
        self.nlp_processor = data['nlp_processor']
        self.is_fitted = True
        print(f"Feature encoders loaded from {filepath}")
        return self


if __name__ == "__main__":
    df = pd.read_csv("data/concept_error_dataset.csv")
    fe = FeatureEngineer()
    fe.fit(df)
    X = fe.prepare_feature_matrix(df)
    print(f"Constructed Feature Matrix Shape: {X.shape}")
    fe.save_encoders()
