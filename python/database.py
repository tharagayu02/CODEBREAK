import os
import sqlite3
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any, List

class StudentDatabase:
    """
    SQLite database engine for CodeBreak:
    Handles user authentication, completed code submissions, user progress analytics,
    and historical error attempt logs for R statistical processing.
    """

    def __init__(self, db_path: str = "codebreak.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def _init_db(self):
        """
        Creates all required database tables and handles auto-migration if schema changes.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if user_progress table exists with old schema (student_id)
            cursor.execute("PRAGMA table_info(user_progress)")
            cols = [info[1] for info in cursor.fetchall()]
            if cols and "username" not in cols:
                cursor.execute("DROP TABLE user_progress")
                conn.commit()

            # 1. Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. Unified User Progress Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    username TEXT PRIMARY KEY,
                    xp INTEGER DEFAULT 0,
                    easy_completed INTEGER DEFAULT 0,
                    medium_completed INTEGER DEFAULT 0,
                    hard_completed INTEGER DEFAULT 0,
                    total_completed INTEGER DEFAULT 0,
                    streak INTEGER DEFAULT 1,
                    current_level INTEGER DEFAULT 1,
                    completed_challenges TEXT DEFAULT '',
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)

            # 3. User Submissions & Completed Code Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    question_title TEXT NOT NULL,
                    submitted_code TEXT NOT NULL,
                    status TEXT NOT NULL,
                    xp_earned INTEGER DEFAULT 0,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)

            # 4. Error Attempts Log Table (for ML & R Analytics)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    code TEXT,
                    error_type TEXT,
                    error_message TEXT,
                    predicted_concept TEXT,
                    confidence REAL,
                    signals TEXT,
                    FOREIGN KEY (student_id) REFERENCES users(username)
                )
            """)
            conn.commit()

    # ==========================================
    # USER AUTHENTICATION & MANAGEMENT
    # ==========================================
    def create_user(self, username: str, password: str, full_name: str) -> Dict[str, Any]:
        """
        Registers a new user account. Returns dict with status and message.
        """
        username = username.strip().lower()
        full_name = full_name.strip()
        
        if not username or not password or not full_name:
            return {"status": "error", "message": "All fields (Username, Password, Name) are required."}
        
        pw_hash = self._hash_password(password)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)",
                    (username, pw_hash, full_name)
                )
                cursor.execute(
                    "INSERT INTO user_progress (username, xp, easy_completed, medium_completed, hard_completed, total_completed, current_level, completed_challenges) VALUES (?, 0, 0, 0, 0, 0, 1, '')",
                    (username,)
                )
                conn.commit()
            return {"status": "success", "message": f"Account created successfully! Welcome, {full_name}."}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": f"Username '{username}' is already taken. Please choose another username or log in."}

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Validates user credentials. Returns user info dict if valid, else None.
        """
        username = username.strip().lower()
        pw_hash = self._hash_password(password)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, full_name, created_at FROM users WHERE username = ? AND password_hash = ?",
                (username, pw_hash)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "username": row[0],
                    "full_name": row[1],
                    "created_at": row[2]
                }
        return None

    # ==========================================
    # USER COMPLETED CODE & PROGRESS TRACKING
    # ==========================================
    def record_submission(
        self,
        username: str,
        question_id: str,
        difficulty: str,
        question_title: str,
        submitted_code: str,
        status: str,
        xp_earned: int = 0
    ) -> Dict[str, Any]:
        """
        Records a code submission and updates the user's progress dynamically.
        """
        username = username.strip().lower()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if this question was already solved by this user
            cursor.execute(
                "SELECT COUNT(*) FROM user_submissions WHERE username = ? AND question_id = ? AND status = 'PASSED'",
                (username, question_id)
            )
            already_passed = cursor.fetchone()[0] > 0

            # Insert submission record
            cursor.execute("""
                INSERT INTO user_submissions (username, question_id, difficulty, question_title, submitted_code, status, xp_earned, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, question_id, difficulty, question_title, submitted_code, status, xp_earned, timestamp))

            # If new successful completion, update user_progress stats
            if status == "PASSED" and not already_passed:
                diff_lower = difficulty.lower()
                easy_inc = 1 if "easy" in diff_lower else 0
                med_inc = 1 if "medium" in diff_lower else 0
                hard_inc = 1 if "hard" in diff_lower else 0

                cursor.execute("""
                    UPDATE user_progress
                    SET xp = xp + ?,
                        easy_completed = easy_completed + ?,
                        medium_completed = medium_completed + ?,
                        hard_completed = hard_completed + ?,
                        total_completed = total_completed + 1,
                        last_active = CURRENT_TIMESTAMP
                    WHERE username = ?
                """, (xp_earned, easy_inc, med_inc, hard_inc, username))
                conn.commit()
                return {"status": "success", "first_time_passed": True, "xp_earned": xp_earned}
            
            conn.commit()
            return {"status": "success", "first_time_passed": False, "xp_earned": 0}

    def get_user_progress_summary(self, username: str) -> Dict[str, Any]:
        """
        Fetches progress metrics for a specific logged-in user.
        """
        username = username.strip().lower()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT xp, easy_completed, medium_completed, hard_completed, total_completed, streak, current_level, completed_challenges FROM user_progress WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if not row:
                return {
                    "username": username,
                    "xp": 0,
                    "easy_completed": 0,
                    "medium_completed": 0,
                    "hard_completed": 0,
                    "total_completed": 0,
                    "streak": 1,
                    "current_level": 1,
                    "completed_q_ids": []
                }
            
            cursor.execute(
                "SELECT DISTINCT question_id FROM user_submissions WHERE username = ? AND status = 'PASSED'",
                (username,)
            )
            passed_ids = [r[0] for r in cursor.fetchall()]

            return {
                "username": username,
                "xp": row[0],
                "easy_completed": row[1],
                "medium_completed": row[2],
                "hard_completed": row[3],
                "total_completed": row[4],
                "streak": row[5],
                "current_level": row[6],
                "completed_q_ids": passed_ids
            }

    def get_user_completed_submissions(self, username: str) -> pd.DataFrame:
        """
        Returns all completed code submissions for a user.
        """
        username = username.strip().lower()
        query = """
            SELECT submitted_at, question_id, difficulty, question_title, status, xp_earned, submitted_code
            FROM user_submissions
            WHERE username = ?
            ORDER BY id DESC
        """
        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(username,))
        return df

    # ==========================================
    # ERROR ATTEMPTS LOGGING & R EXPORT
    # ==========================================
    def log_attempt(
        self,
        student_id: str,
        code: str,
        error_type: str,
        error_message: str,
        predicted_concept: str,
        confidence: float,
        signals: str = ""
    ):
        """
        Logs an error execution attempt for a logged-in student.
        """
        student_id = student_id.strip().lower() if student_id else "anonymous"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attempts (student_id, timestamp, code, error_type, error_message, predicted_concept, confidence, signals)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, timestamp, code, error_type, error_message, predicted_concept, confidence, signals))
            conn.commit()

    def get_student_history(self, student_id: str, limit: int = 50) -> pd.DataFrame:
        student_id = student_id.strip().lower()
        query = """
            SELECT id, student_id, timestamp, code, error_type, error_message, predicted_concept, confidence, signals
            FROM attempts
            WHERE student_id = ?
            ORDER BY id DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(student_id, limit))
        return df

    def get_student_history_metrics(self, student_id: str) -> dict:
        history_df = self.get_student_history(student_id, limit=100)
        num_previous_errors = len(history_df)
        if num_previous_errors == 0:
            return {
                "num_previous_errors": 0,
                "concept_error_freq": 0,
                "recent_error_freq": 0,
                "num_unique_error_types": 0,
                "recency_concept_weight": 0.0
            }

        num_unique_error_types = history_df['error_type'].nunique()
        recent_error_freq = min(num_previous_errors, 10)
        concept_counts = history_df['predicted_concept'].value_counts().to_dict()
        top_concept_freq = max(concept_counts.values()) if concept_counts else 0
        weights = np.exp(-0.1 * np.arange(len(history_df)))
        recency_weight = float(np.sum(weights))

        return {
            "num_previous_errors": num_previous_errors,
            "concept_error_freq": top_concept_freq,
            "recent_error_freq": recent_error_freq,
            "num_unique_error_types": num_unique_error_types,
            "recency_concept_weight": recency_weight
        }

    def export_all_history_csv(
        self, 
        username: Optional[str] = None, 
        filepath: str = "data/processed/all_student_history.csv"
    ) -> str:
        """
        Exports history logs to CSV for R analysis. If username provided, exports that user's history.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with self._get_connection() as conn:
            if username:
                username = username.strip().lower()
                query = "SELECT * FROM attempts WHERE student_id = ? ORDER BY timestamp ASC"
                df = pd.read_sql_query(query, conn, params=(username,))
                if len(df) == 0:
                    query_all = "SELECT * FROM attempts ORDER BY timestamp ASC"
                    df = pd.read_sql_query(query_all, conn)
            else:
                query = "SELECT * FROM attempts ORDER BY timestamp ASC"
                df = pd.read_sql_query(query, conn)

        df.to_csv(filepath, index=False)
        return filepath
