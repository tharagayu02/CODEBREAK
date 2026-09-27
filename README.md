# ⚡ CodeBreak: AI-Based Programming Concept Gap Detection and Personalized Learning System

![CodeBreak Banner](https://img.shields.io/badge/CodeBreak-AI%20%7C%20ML%20%7C%20NLP%20%7C%20R-indigo?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![R Version](https://img.shields.io/badge/R-4.6.1-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge)

---

## 1. Project Title
**CodeBreak – AI-Based Programming Concept Gap Detection and Personalized Learning System**

---

## 2. Problem Statement
Beginner programming students frequently encounter execution errors (`IndexError`, `KeyError`, `TypeError`, `NameError`, etc.) while learning to code. Generic chatbot assistance often provides surface-level error fixes without diagnosing **why** the student is making recurring errors. Traditional static error messages fail to identify underlying psychological or technical concept gaps—such as misunderstandings of 0-based indexing, dictionary key structures, or type mutability.

---

## 3. Motivation
Students need more than simple code patches; they need a diagnostic learning assistant that tracks historical error patterns across multiple assignments, identifies root concept gaps, provides pedagogically structured explanations, and generates target practice questions to reinforce understanding.

---

## 4. Proposed Solution
CodeBreak is a hybrid AI/ML system that:
1. **Tracks Historical Errors**: Logs student attempts into a local SQLite database with timestamps and error metadata.
2. **Predicts Concept Gaps**: Uses a supervised Machine Learning classifier (Random Forest / XGBoost) paired with NLP (TF-IDF vectorization + syntax tokenization) to predict the likely programming concept gap.
3. **Explains via AI/LLM**: Generates beginner-friendly explanations, corrected code, root cause analyses, and 3–5 tailored practice exercises.
4. **Analyzes via R**: Employs R programming scripts (`analyze_errors.R`, `learning_analysis.R`) to compute statistical distributions, recency trends, and generate publication-grade learning pattern visualizations.

---

## 5. Novelty
- **Pattern-Based Gap Detection**: Unlike standard error-explaining chatbots, CodeBreak incorporates student history recency metrics (`concept_error_freq`, `recent_error_frequency`, `recency_weighted_concept_score`) into the ML prediction matrix.
- **Strict Role Separation**:
  - **NLP**: Extracts syntactic features and converts error messages to TF-IDF vectors.
  - **ML**: Predicts the **Likely Concept Gap** with confidence scores.
  - **R**: Conducts statistical frequency analysis, error decay modeling, and plot generation.
  - **AI/LLM**: Translates predictions into safe, pedagogical explanations and exercises.
  - **Streamlit**: Provides a modern, dark-themed interactive web interface.

---

## 6. System Architecture

```
                                  STUDENT INPUT
                          (Code + Error Message + Student ID)
                                        │
                                        ▼
                                 SQLite Database
                           (Fetch Attempt History & Metrics)
                                        │
                                        ▼
                            Python NLP Preprocessor
                   (Traceback Cleaning & TF-IDF Vectorization)
                                        │
                                        ▼
                             Feature Engineer
                (Error Type OHE + TF-IDF + Syntax Flags + History)
                                        │
                                        ▼
                              Machine Learning Model
                       (Random Forest / XGBoost Classifier)
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
                 Likely Concept Gap             Confidence Score
                         │                             │
                         └──────────────┬──────────────┘
                                        ▼
                              AI Pedagogical Engine
                     (Explanation + Fix + Practice Questions)
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
            Streamlit Dashboard                   R Statistical Engine
       (Interactive User Interface)         (learning_analysis.R & Plots)
```

---

## 7. Dataset Description
The system is built upon an educational/research dataset (`data/concept_error_dataset.csv`) containing 123 realistic Python error instances across 10 core Python error types mapped to 10 programming concepts:

| Error Type | Target Concept Gap | Sample Trigger Pattern |
|---|---|---|
| `IndexError` | **List Indexing** | `arr = [10, 20]; print(arr[5])` |
| `KeyError` | **Dictionary Lookup** | `user = {'name': 'Alice'}; print(user['age'])` |
| `TypeError` | **Type Compatibility & Casting** | `msg = 'Age: ' + 20` |
| `NameError` | **Variable Scope & Naming** | `print(total_score)` (unassigned) |
| `ValueError` | **Value & Argument Constraints** | `num = int('abc')` |
| `SyntaxError` | **Syntax & Formatting Rules** | `if x == 5\n print(x)` (missing colon) |
| `IndentationError` | **Code Block Indentation** | `def foo():\nprint('hi')` |
| `AttributeError` | **Object Attributes & Methods** | `lst = []; lst.strip()` |
| `ZeroDivisionError` | **Arithmetic Operations** | `res = 10 / 0` |
| `FileNotFoundError` | **File Handling & Paths** | `f = open('missing.txt', 'r')` |

*Dataset Fields*: `error_type`, `error_message`, `code_snippet`, `concept`, `difficulty`, `language`.

---

## 8. NLP Methodology
1. **Cleaning & Normalization**: Strips file paths (`File "...", line X`), memory addresses (`0x7fa...`), and standardizes text to lowercase.
2. **Code Syntax Extraction**: Detects syntax operators (`[]`, `{}`, `.get`, `def`, `+`, `/`, `open()`).
3. **TF-IDF Vectorization**: Fits a sublinear TF-IDF vectorizer (max 150 features, unigram & bigram range `(1, 2)`) on combined error text and code tokens. Vectorizer saved to `models/tfidf_vectorizer.pkl`.

---

## 9. Feature Engineering
The feature matrix $X$ combines:
- **One-Hot Encoded Error Type** ($10$ binary columns)
- **TF-IDF Feature Matrix** ($150$ numerical columns)
- **Syntactic Code Indicators** ($6$ binary flags: bracket indexing, dict braces, dot access, colon, division operator, quotes)
- **Student History Metrics** ($5$ continuous metrics: `num_previous_errors`, `concept_error_freq`, `recent_error_freq`, `num_unique_error_types`, `recency_concept_weight`)

---

## 10. ML Methodology
- **Primary Model**: Random Forest Classifier (`n_estimators=100`, `max_depth=12`, `class_weight='balanced'`).
- **Comparison Model**: XGBoost Classifier (`n_estimators=100`, `max_depth=6`).
- **Evaluation Metrics**: Evaluated via Stratified 80/20 Train/Test Split & Cross-Validation:
  - **Accuracy**: 100.0%
  - **Precision**: 100.0%
  - **Recall**: 100.0%
  - **F1-Score**: 100.0%
- Model artifact saved to `models/concept_gap_model.pkl`.

---

## 11. R Analysis
R 4.6.1 is integrated to perform independent statistical learning-pattern analysis:
- **`r/analyze_errors.R`**: Reads student attempt logs exported from SQLite (`data/processed/all_student_history.csv`), computes total attempts, most frequent weak concepts, error distributions, and outputs `reports/r_analysis_summary.json`.
- **`r/learning_analysis.R`**: Generates high-resolution dark-themed PNG charts:
  - `reports/errors_by_concept.png` (Bar chart of errors by concept)
  - `reports/errors_over_time.png` (Line chart of model confidence & progress)
  - `reports/student_concept_performance.png` (Frequency breakdown of error types)

---

## 12. AI/LLM Component
After the ML model predicts the concept gap, the AI Explainer (`python/ai_explainer.py`) generates:
1. **What Happened**: Clear explanation of the error occurrence.
2. **Why It Happened**: Technical concept breakdown.
3. **Why Mistake Made**: Root cause insight.
4. **Corrected Code**: Drop-in fixed Python code snippet.
5. **Simple Example**: Illustrative demonstration code.
6. **3–5 Practice Questions**: Tailored exercises for the student.
7. **Learning Recommendation**: Phrased safely as *"You may need more practice with [Concept]"*.

---

## 13. Technology Stack
- **Languages**: Python 3.11, R 4.6.1, SQL, HTML/CSS
- **Libraries & Frameworks**:
  - `scikit-learn`, `xgboost`, `pandas`, `numpy`, `joblib`
  - `streamlit` (UI)
  - `matplotlib`, `seaborn`
  - Base R / `jsonlite`

---

## 14. Installation

```bash
# 1. Clone or navigate to CodeBreak directory
cd CodeBreak

# 2. Create and activate a Python virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install required Python packages
pip install -r requirements.txt
```

---

## 15. How to Train the Model

```bash
# Generate training dataset
python python/create_dataset.py

# Train NLP feature vectorizer and ML concept gap model
python -m python.train_model
```

---

## 16. How to Run the Application

```bash
# Launch Streamlit Web Application
streamlit run python/app.py
```

Open `http://localhost:8501` in your browser.

---

## 17. Example Input & Output

### Input
- **Student ID**: `S001`
- **Code Snippet**:
  ```python
  numbers = [10, 20, 30]
  print(numbers[5])
  ```
- **Error Message**: `IndexError: list index out of range`

### Output
- **Likely Concept Gap**: `List Indexing`
- **Model Confidence**: `100.0%`
- **Status**: `High Confidence`
- **Signals**: `Error Type: IndexError`, `Bracket Indexing Operator [] detected in code`
- **AI Recommendation**: *"You may need more practice with List Indexing. Review 0-based indexing and boundary conditions when accessing list items in loops."*

---

## 18. Limitations
- Dataset current scope focuses on 10 fundamental Python error classes; advanced framework errors (e.g. Django/TensorFlow) require expanding dataset classes.
- R analysis requires local installation of `Rscript`.

---

## 19. Future Improvements
- Multi-language parser for C++, Java, and JavaScript execution errors.
- Integration with LLM APIs (Google Gemini / OpenAI) for dynamic natural language exercise generation.
- Exportable PDF learning certificate and progress report generation.

---

## 20. Role Breakdown Summary

| Technology | Responsible Task |
|---|---|
| **Python NLP** | Preprocesses error messages, strips tracebacks, extracts TF-IDF vectors |
| **Python ML** | Classifies the **Likely Concept Gap** with confidence scores using Random Forest |
| **SQLite DB** | Stores historical student attempts and computes recency-weighted metrics |
| **R Language** | Performs statistical frequency analysis, error decay modeling, and outputs PNG graphs |
| **AI Component** | Translates ML predictions into beginner explanations, fixes, and practice questions |
| **Streamlit UI** | Renders the interactive dashboard, tabbed profile analysis, and R analytics |
