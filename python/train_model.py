import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, confusion_matrix

try:
    from python.feature_engineering import FeatureEngineer
except ImportError:
    from feature_engineering import FeatureEngineer

try:
    import xgboost as xgb  # type: ignore
    XGBClassifier = xgb.XGBClassifier  # type: ignore
    HAS_XGBOOST = True
except Exception:
    XGBClassifier = None  # type: ignore
    HAS_XGBOOST = False

def train_and_evaluate(dataset_path: str = "data/concept_error_dataset.csv"):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    if not os.path.isabs(dataset_path):
        candidate = os.path.join(base_dir, dataset_path)
        if os.path.exists(candidate) or not os.path.exists(dataset_path):
            dataset_path = candidate

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please run create_dataset.py first.")

    df = pd.read_csv(dataset_path)
    print(f"Loaded dataset from {dataset_path} with {len(df)} samples.")

    # Target variable: concept
    y = df['concept'].values
    unique_concepts = np.unique(y)
    concept_to_label = {concept: i for i, concept in enumerate(unique_concepts)}
    label_to_concept = {i: concept for i, concept in enumerate(unique_concepts)}

    # Initialize and fit FeatureEngineer
    fe = FeatureEngineer()
    fe.fit(df)
    X = fe.prepare_feature_matrix(df)

    # Save feature encoders
    encoder_path = os.path.join(base_dir, "models", "feature_encoder.pkl")
    fe.save_encoders(encoder_path)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set: {X_train.shape[0]} samples | Testing set: {X_test.shape[0]} samples")

    # --- Model 1: Random Forest Classifier ---
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        class_weight='balanced'
    )
    rf_model.fit(X_train, y_train)

    y_pred_rf = rf_model.predict(X_test)
    rf_acc = accuracy_score(y_test, y_pred_rf)
    rf_prec, rf_rec, rf_f1, _ = precision_recall_fscore_support(y_test, y_pred_rf, average='weighted')

    print("\n==========================================")
    print("      RANDOM FOREST EVALUATION RESULTS    ")
    print("==========================================")
    print(f"Accuracy:  {rf_acc * 100:.2f}%")
    print(f"Precision: {rf_prec * 100:.2f}%")
    print(f"Recall:    {rf_rec * 100:.2f}%")
    print(f"F1-Score:  {rf_f1 * 100:.2f}%")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred_rf))

    cm_rf = confusion_matrix(y_test, y_pred_rf, labels=unique_concepts)

    best_model = rf_model
    best_model_name = "RandomForest"
    best_acc = rf_acc

    # --- Model 2: XGBoost Classifier (Optional Comparison) ---
    xgb_metrics = None
    if HAS_XGBOOST:
        try:
            y_train_num = np.array([concept_to_label[c] for c in y_train], dtype=int)
            y_test_num = np.array([concept_to_label[c] for c in y_test], dtype=int)

            xgb_model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric='mlogloss',
                objective='multi:softprob',
                num_class=len(unique_concepts)
            )
            xgb_model.fit(X_train, y_train_num)

            y_pred_xgb_num = xgb_model.predict(X_test)
            y_pred_xgb = [label_to_concept[int(i)] for i in y_pred_xgb_num]

            xgb_acc = accuracy_score(y_test, y_pred_xgb)
            xgb_prec, xgb_rec, xgb_f1, _ = precision_recall_fscore_support(y_test, y_pred_xgb, average='weighted', zero_division=0)

            print("\n==========================================")
            print("       XGBOOST EVALUATION RESULTS        ")
            print("==========================================")
            print(f"Accuracy:  {xgb_acc * 100:.2f}%")
            print(f"Precision: {xgb_prec * 100:.2f}%")
            print(f"Recall:    {xgb_rec * 100:.2f}%")
            print(f"F1-Score:  {xgb_f1 * 100:.2f}%")

            xgb_metrics = {
                "accuracy": float(xgb_acc),
                "precision": float(xgb_prec),
                "recall": float(xgb_rec),
                "f1_score": float(xgb_f1)
            }

            if xgb_acc > best_acc:
                best_model = xgb_model
                best_model_name = "XGBoost"
                best_acc = xgb_acc
        except Exception as e:
            print(f"XGBoost training encountered an issue: {e}. Falling back to Random Forest.")

    # Create bidirectional label maps supporting both int and str keys
    robust_label_map = {}
    for i, concept in enumerate(unique_concepts):
        robust_label_map[i] = concept
        robust_label_map[str(i)] = concept
        robust_label_map[concept] = concept

    # Save model artifacts
    model_path = os.path.join(base_dir, "models", "concept_gap_model.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model_artifact = {
        "model": best_model,
        "model_name": best_model_name,
        "unique_concepts": unique_concepts.tolist(),
        "concept_to_label": concept_to_label,
        "label_to_concept": robust_label_map
    }
    joblib.dump(model_artifact, model_path)
    print(f"\nBest trained model ({best_model_name}) saved to {model_path}")

    # Save metrics report
    os.makedirs("reports", exist_ok=True)
    metrics_report = {
        "best_model": best_model_name,
        "random_forest": {
            "accuracy": float(rf_acc),
            "precision": float(rf_prec),
            "recall": float(rf_rec),
            "f1_score": float(rf_f1),
            "confusion_matrix": cm_rf.tolist()
        },
        "xgboost": xgb_metrics,
        "target_concepts": unique_concepts.tolist()
    }
    metrics_path = "reports/metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics_report, f, indent=4)
    print(f"Metrics report saved to {metrics_path}")

if __name__ == "__main__":
    train_and_evaluate()
