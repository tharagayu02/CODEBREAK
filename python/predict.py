import os
import joblib
import pandas as pd
import numpy as np

try:
    from python.feature_engineering import FeatureEngineer
    from python.database import StudentDatabase
except ImportError:
    from feature_engineering import FeatureEngineer
    from database import StudentDatabase

class ConceptGapPredictor:
    """
    Inference pipeline for predicting student programming concept gaps.
    Combines NLP feature extraction, student error history, ML classifier, and signal explainability.
    """

    def __init__(
        self,
        model_path: str = "models/concept_gap_model.pkl",
        encoder_path: str = "models/feature_encoder.pkl",
        db_path: str = "codebreak.db"
    ):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        if not os.path.isabs(model_path):
            candidate = os.path.join(base_dir, model_path)
            if os.path.exists(candidate) or not os.path.exists(model_path):
                model_path = candidate

        if not os.path.isabs(encoder_path):
            candidate = os.path.join(base_dir, encoder_path)
            if os.path.exists(candidate) or not os.path.exists(encoder_path):
                encoder_path = candidate

        if not os.path.isabs(db_path):
            candidate = os.path.join(base_dir, db_path)
            if os.path.exists(candidate) or not os.path.exists(db_path):
                db_path = candidate

        self.model_path = model_path
        self.encoder_path = encoder_path

        # Auto-train models on startup if missing (e.g. during cloud deployment)
        if not os.path.exists(self.model_path) or not os.path.exists(self.encoder_path):
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            print(f"Model artifacts missing. Auto-training model at {self.model_path}...")
            try:
                from python.train_model import train_and_evaluate
            except ImportError:
                from train_model import train_and_evaluate
            
            dataset_path = os.path.join(base_dir, "data", "concept_error_dataset.csv")
            if not os.path.exists(dataset_path):
                try:
                    from python.create_dataset import generate_synthetic_dataset
                except ImportError:
                    from create_dataset import generate_synthetic_dataset
                generate_synthetic_dataset(dataset_path)

            train_and_evaluate(dataset_path)

        self.db = StudentDatabase(db_path)
        
        self.feature_engineer = FeatureEngineer()
        self.feature_engineer.load_encoders(self.encoder_path)
        
        model_artifact = joblib.load(model_path)
        self.model = model_artifact["model"]
        self.model_name = model_artifact["model_name"]
        self.unique_concepts = model_artifact["unique_concepts"]
        self.label_to_concept = model_artifact.get("label_to_concept", {})

    def extract_important_signals(self, error_type: str, code_snippet: str, history_metrics: dict) -> list:
        """
        Generates explainability signals showing why the ML model made its prediction.
        """
        signals = [f"Error Type: {error_type}"]

        if "[" in code_snippet or "]" in code_snippet:
            signals.append("Bracket Indexing Operator `[]` detected in code")
        if "{" in code_snippet or "}" in code_snippet:
            signals.append("Dictionary Literal `{}` detected in code")
        if "." in code_snippet:
            signals.append("Dot Attribute Access `.` detected in code")
        if "/" in code_snippet or "%" in code_snippet:
            signals.append("Division / Modulo Operator `/` `%` detected in code")
        if "open(" in code_snippet or "read(" in code_snippet:
            signals.append("File I/O Operation detected in code")
        
        if history_metrics.get("num_previous_errors", 0) > 0:
            signals.append(f"{history_metrics['num_previous_errors']} previous total errors recorded for student")
            if history_metrics.get("concept_error_freq", 0) > 1:
                signals.append(f"Recurring error pattern detected ({history_metrics['concept_error_freq']} previous instances)")

        return signals

    def predict_concept_gap(
        self,
        error_message: str,
        code_snippet: str,
        student_id: str = "S001",
        error_type_hint: str = None
    ) -> dict:
        """
        Runs prediction for a given error message and code snippet.
        """
        if not error_message:
            error_message = "Unknown error"
        if not code_snippet:
            code_snippet = ""

        # Infer error_type if not provided
        if not error_type_hint or error_type_hint == "Auto-Detect":
            matched_types = [
                t for t in self.feature_engineer.KNOWN_ERROR_TYPES
                if t.lower() in error_message.lower()
            ]
            error_type = matched_types[0] if matched_types else "SyntaxError"
        else:
            error_type = error_type_hint

        # Fetch history metrics
        history_metrics = self.db.get_student_history_metrics(student_id)
        hist_df = pd.DataFrame([history_metrics])

        # Create input DataFrame
        input_df = pd.DataFrame([{
            'error_type': error_type,
            'error_message': error_message,
            'code_snippet': code_snippet
        }])

        # Extract features
        X_input = self.feature_engineer.prepare_feature_matrix(input_df, history_features=hist_df)

        # Predict probability
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(X_input)[0]
            max_idx = int(np.argmax(probabilities))
            confidence = float(probabilities[max_idx] * 100)
            
            if hasattr(self.model, "classes_"):
                predicted_class = self.model.classes_[max_idx]
                if predicted_class in self.label_to_concept:
                    predicted_concept = self.label_to_concept[predicted_class]
                elif str(predicted_class) in self.label_to_concept:
                    predicted_concept = self.label_to_concept[str(predicted_class)]
                elif isinstance(predicted_class, (int, np.integer)) and int(predicted_class) < len(self.unique_concepts):
                    predicted_concept = self.unique_concepts[int(predicted_class)]
                else:
                    predicted_concept = str(predicted_class)
            else:
                predicted_concept = self.unique_concepts[max_idx]
        else:
            predicted_class = self.model.predict(X_input)[0]
            if predicted_class in self.label_to_concept:
                predicted_concept = self.label_to_concept[predicted_class]
            elif str(predicted_class) in self.label_to_concept:
                predicted_concept = self.label_to_concept[str(predicted_class)]
            else:
                predicted_concept = str(predicted_class)
            confidence = 85.0

        # Safety / Reliability framing
        is_uncertain = confidence < 60.0
        status_label = "Prediction uncertain – please review multiple possible concepts." if is_uncertain else "High Confidence"

        # Generate signals
        signals = self.extract_important_signals(error_type, code_snippet, history_metrics)

        # Log attempt in SQLite
        self.db.log_attempt(
            student_id=student_id,
            code=code_snippet,
            error_type=error_type,
            error_message=error_message,
            predicted_concept=predicted_concept,
            confidence=confidence,
            signals="; ".join(signals)
        )

        return {
            "student_id": student_id,
            "error_type": error_type,
            "error_message": error_message,
            "code_snippet": code_snippet,
            "predicted_concept": predicted_concept,
            "confidence": round(confidence, 1),
            "status_label": status_label,
            "is_uncertain": is_uncertain,
            "signals": signals,
            "history_metrics": history_metrics
        }


if __name__ == "__main__":
    predictor = ConceptGapPredictor()
    res = predictor.predict_concept_gap(
        error_message="IndexError: list index out of range",
        code_snippet="items = [10, 20]\nprint(items[5])",
        student_id="S001"
    )
    print("\nInference Output:")
    print("Predicted Concept:", res["predicted_concept"])
    print("Confidence:", res["confidence"], "%")
    print("Signals:", res["signals"])
