import os
import sys
import pandas as pd
import streamlit as st

# Add current directory and parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from python.predict import ConceptGapPredictor
from python.ai_explainer import AIConceptExplainer
from python.database import StudentDatabase
from python.r_runner import RRunner
from python.code_executor import execute_user_code
from python.question_bank import QUESTIONS, get_questions_by_difficulty

# Page Configuration
st.set_page_config(
    page_title="CodeBreak - AI Concept Gap Detection & Learning Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling: Mocha & Cream Palette with Top Gap Removal & Flawless Alignment
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');

    /* Remove Streamlit Top Header Bar & Eliminate Top Gap */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    
    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stAppViewBlockContainer"] {
        padding-top: 0.5rem !important;
    }

    /* Global Mocha & Cream Main Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #faf7f2 !important;
        color: #3c2a21 !important;
    }

    /* Main Container Padding & Alignment Fix (Flush to top, no top/right gap!) */
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        margin-top: 0rem !important;
        max-width: 1450px !important;
        width: 100% !important;
    }

    /* Left Sidebar: Deep Mocha / Rich Espresso Background */
    section[data-testid="stSidebar"] {
        background-color: #3c2a21 !important;
        border-right: 1px solid #5c4033 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #f5f0e6 !important;
    }

    /* Custom Cards & Containers (Mocha & Cream) */
    .light-card {
        background-color: #fffdfa !important;
        border: 1px solid #e6ccb2 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 10px rgba(60, 42, 33, 0.05) !important;
        margin-bottom: 20px !important;
        width: 100% !important;
    }

    .auth-card {
        background-color: #fffdfa !important;
        border: 1.5px solid #ddb892 !important;
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0 10px 25px -5px rgba(60, 42, 33, 0.12) !important;
        max-width: 550px !important;
        margin: 20px auto !important;
    }

    .sidebar-user-card {
        background-color: #4a3525 !important;
        border: 1px solid #6f4e37 !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
    }

    /* Page Header Titles */
    .page-title {
        font-size: 2.0rem !important;
        font-weight: 800 !important;
        color: #6f4e37 !important;
        letter-spacing: -0.02em !important;
        margin-top: 0rem !important;
        margin-bottom: 4px !important;
        padding-top: 0rem !important;
    }

    .section-header {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #3c2a21 !important;
        border-bottom: 2px solid #e6ccb2 !important;
        padding-bottom: 8px !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }

    /* Difficulty Badges (Mocha / Warm Tones) */
    .badge-easy {
        background-color: #e8f0ec !important;
        color: #2d5a47 !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
    }

    .badge-medium {
        background-color: #fef3e7 !important;
        color: #92400e !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
    }

    .badge-hard {
        background-color: #f9ebea !important;
        color: #8c2d19 !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
    }

    /* Inputs & Textareas */
    .stTextArea textarea, .stTextInput input {
        background-color: #fffdfa !important;
        color: #2c1d11 !important;
        border: 1px solid #ddb892 !important;
        border-radius: 8px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.95rem !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #6f4e37 !important;
        box-shadow: 0 0 0 3px rgba(111, 78, 55, 0.2) !important;
    }

    /* Dropdown Styling */
    div[data-baseweb="select"] {
        background-color: #fffdfa !important;
        border: 1px solid #ddb892 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] * {
        color: #2c1d11 !important;
        background-color: #fffdfa !important;
    }

    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] *,
    li[role="option"],
    div[role="option"] {
        background-color: #fffdfa !important;
        color: #2c1d11 !important;
        font-weight: 600 !important;
    }

    div[role="option"]:hover, li[role="option"]:hover, [aria-selected="true"] {
        background-color: #f5f0e6 !important;
        color: #6f4e37 !important;
    }

    /* Buttons Styling */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #7f5539, #6f4e37) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 6px -1px rgba(111, 78, 55, 0.25) !important;
        width: 100% !important;
    }

    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6f4e37, #5c4033) !important;
    }

    .stButton button[kind="secondary"] {
        background-color: #fffdfa !important;
        color: #6f4e37 !important;
        font-weight: 700 !important;
        border: 1.5px solid #7f5539 !important;
        border-radius: 8px !important;
        width: 100% !important;
    }

    .stButton button[kind="secondary"]:hover {
        background-color: #f5f0e6 !important;
    }

    /* Sidebar buttons styling */
    section[data-testid="stSidebar"] .stButton button {
        background-color: #6f4e37 !important;
        color: #ffffff !important;
        border: 1px solid #7f5539 !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #5c4033 !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: 2px solid #e6ccb2 !important;
        padding-bottom: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 700 !important;
        color: #7f5539 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        background-color: #f5f0e6 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #3c2a21 !important;
        background-color: #fffdfa !important;
        border-top: 3px solid #6f4e37 !important;
    }

    /* Code Output Console Box */
    .console-output {
        background-color: #231709 !important;
        color: #ebd9b4 !important;
        font-family: 'Fira Code', monospace !important;
        padding: 16px !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        white-space: pre-wrap !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Core Services
@st.cache_resource
def load_services():
    predictor = ConceptGapPredictor()
    explainer = AIConceptExplainer()
    db = StudentDatabase()
    r_runner = RRunner()
    return predictor, explainer, db, r_runner

try:
    predictor, explainer, db, r_runner = load_services()
except Exception as e:
    st.error(f"Error loading system models: {e}. Make sure model is trained by running `python python/train_model.py`!")
    st.stop()

# Initialize Session State for User Auth
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

# ==========================================
# AUTHENTICATION SCREEN (WHEN NOT LOGGED IN)
# ==========================================
if not st.session_state["logged_in_user"]:
    st.markdown("""
    <div style='text-align: center; margin-top: 10px; margin-bottom: 10px;'>
        <div style='display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #7f5539, #6f4e37); border-radius: 16px; padding: 12px 24px; font-size: 1.8rem; font-weight: 900; color: white; box-shadow: 0 8px 18px rgba(60, 42, 33, 0.25);'>
            CodeBreak
        </div>
        <div style='font-size: 1.1rem; color: #5c4033; font-weight: 600; margin-top: 10px;'>AI Programming Concept Gap Detection & Learning Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_auth_center = st.columns([1, 2, 1])[1]
    
    with col_auth_center:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["Log In", "Sign Up (New User)"])
        
        with tab_login:
            st.markdown("#### Welcome Back! Please Log In")
            login_user = st.text_input("Username:", key="login_u")
            login_pw = st.text_input("Password:", type="password", key="login_p")
            login_btn = st.button("Log In to CodeBreak", type="primary", key="btn_login")
            
            if login_btn:
                if not login_user or not login_pw:
                    st.warning("Please enter both username and password.")
                else:
                    user_data = db.authenticate_user(login_user, login_pw)
                    if user_data:
                        st.session_state["logged_in_user"] = user_data
                        st.success(f"Welcome back, {user_data['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again or Sign Up!")

        with tab_signup:
            st.markdown("#### Create Your CodeBreak Account")
            st.info("New users start at 0 XP with a clean progress tracking profile. No demo data!")
            signup_u = st.text_input("Choose Username:", key="signup_u")
            signup_name = st.text_input("Full Name:", key="signup_name")
            signup_p = st.text_input("Choose Password:", type="password", key="signup_p")
            signup_btn = st.button("Create Account & Start Learning", type="primary", key="btn_signup")
            
            if signup_btn:
                res = db.create_user(signup_u, signup_p, signup_name)
                if res["status"] == "success":
                    st.success(res["message"])
                    user_data = db.authenticate_user(signup_u, signup_p)
                    if user_data:
                        st.session_state["logged_in_user"] = user_data
                        st.rerun()
                else:
                    st.error(res["message"])
                    
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# MAIN DASHBOARD (WHEN LOGGED IN)
# ==========================================
current_user = st.session_state["logged_in_user"]
username = current_user["username"]
full_name = current_user["full_name"]

# Fetch Live User Progress Metrics from Database
user_prog = db.get_user_progress_summary(username)
completed_ids = set(user_prog["completed_q_ids"])
total_q_count = len(QUESTIONS)
completion_pct = (user_prog["total_completed"] / total_q_count * 100.0) if total_q_count > 0 else 0.0

# Left Sidebar Setup (Espresso & Cream Mocha)
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom: 16px;'>
        <div style='font-size: 1.6rem; font-weight: 900; color: #f5f0e6; line-height: 1.1;'>CodeBreak</div>
        <div style='font-size: 0.8rem; color: #d5cea3; font-weight: 600;'>AI Learning & Concept Gap Engine</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='sidebar-user-card'>
        <div style='font-size: 0.75rem; color: #d5cea3; font-weight: 700; text-transform: uppercase;'>Logged In User</div>
        <div style='font-size: 1.15rem; font-weight: 800; color: #f5f0e6;'>{full_name}</div>
        <div style='font-size: 0.8rem; color: #d5cea3;'>@{username}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Log Out", key="btn_logout"):
        st.session_state["logged_in_user"] = None
        st.rerun()
        
    st.divider()
    
    st.markdown("#### Your Live Progress")
    m1, m2 = st.columns(2)
    m1.metric("Total XP", f"{user_prog['xp']} XP")
    m2.metric("Solved", f"{user_prog['total_completed']}/{total_q_count}")
    
    st.progress(min(1.0, completion_pct / 100.0), text=f"Overall Completion: {completion_pct:.1f}%")
    
    st.divider()
    
    st.markdown("#### Difficulty Breakdown")
    st.write(f"Easy Completed: {user_prog['easy_completed']} / 6")
    st.write(f"Medium Completed: {user_prog['medium_completed']} / 6")
    st.write(f"Hard Completed: {user_prog['hard_completed']} / 6")
    
    st.divider()
    st.caption("CodeBreak Database Recorded for @" + username)

# App Top Header (FLUSH TO TOP, ZERO GAP)
col_header_title, col_header_stats = st.columns([3, 1])

with col_header_title:
    st.markdown(f"<div class='page-title'>Welcome, {full_name}!</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 1.0rem; color: #5c4033; font-weight: 500;'>Write Python code, detect programming concept gaps in real-time, solve Easy/Medium/Hard questions, and track your database progress.</div>", unsafe_allow_html=True)

with col_header_stats:
    st.markdown(f"""
    <div style='background-color: #fffdfa; border: 1px solid #ddb892; border-radius: 12px; padding: 10px 14px; text-align: center; box-shadow: 0 2px 4px rgba(60,42,33,0.04);'>
        <div style='font-size: 0.75rem; color: #7f5539; font-weight: 700; text-transform: uppercase;'>User XP Status</div>
        <div style='font-size: 1.25rem; font-weight: 800; color: #6f4e37;'>{user_prog['xp']} XP Points</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Navigation Tabs
tab_playground, tab_question_bank, tab_my_code, tab_r_analytics, tab_guide = st.tabs([
    "Write Code & Debug Error", 
    "Easy, Medium & Hard Coding Levels", 
    "My Solved Code Database",
    "User R Analytics & Progress",
    "Concept Handbook"
])

# ==========================================
# TAB 1: WRITE CODE & DEBUG ERROR PLAYGROUND
# ==========================================
with tab_playground:
    st.markdown("<div class='section-header'>Interactive Live Code Execution & Error Explainer</div>", unsafe_allow_html=True)
    
    st.markdown("Write or paste **any Python code** below. Execute the code to see real-time output. If an error occurs, CodeBreak catches the error, predicts the underlying concept gap, and explains how to fix it.")
    
    col_code_input, col_preset = st.columns([3, 1])
    
    PRESETS = {
        "Custom Code (Write your own)": "",
        "Example 1: List Index Out of Range": "items = [10, 20, 30]\nprint(items[5])",
        "Example 2: Missing Dictionary Key": "user = {'name': 'Alice'}\nprint(user['email'])",
        "Example 3: String & Number Concatenation": "age = 25\nmsg = 'I am ' + age\nprint(msg)",
        "Example 4: Division by Zero": "def calculate_avg(vals):\n    return sum(vals) / len(vals)\nprint(calculate_avg([]))",
        "Example 5: Indentation Error": "def greet():\nprint('Hello')",
        "Example 6: Undefined Variable": "item_price = 100\nprint(total_cost)"
    }
    
    with col_preset:
        selected_preset = st.selectbox("Quick Load Preset:", list(PRESETS.keys()))
        preset_code = PRESETS[selected_preset]
    
    initial_code_val = preset_code if preset_code else "numbers = [10, 20, 30]\n# Write or edit Python code below\nprint(numbers[5])"
    
    user_code = st.text_area(
        "Write / Edit Python Code:",
        value=initial_code_val,
        height=220,
        key="playground_code_area"
    )
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        run_and_debug_btn = st.button("Run Code & Explain Error", type="primary", use_container_width=True)
    with col_btn2:
        run_only_btn = st.button("Execute Code Only", type="secondary", use_container_width=True)
    
    if run_and_debug_btn or run_only_btn:
        if not user_code.strip():
            st.warning("Please enter Python code before running!")
        else:
            with st.spinner("Executing Python code and inspecting runtime tracebacks..."):
                exec_result = execute_user_code(user_code)
            
            st.divider()
            
            st.markdown("##### Execution Output Console:")
            if exec_result["success"]:
                st.markdown(f"<div class='console-output'>{exec_result['output']}</div>", unsafe_allow_html=True)
                st.success("Code executed cleanly with 0 errors!")
            else:
                st.markdown(f"<div class='console-output' style='color: #f87171;'>{exec_result['error_message']}\n\n{exec_result['traceback']}</div>", unsafe_allow_html=True)
                st.error(f"Runtime Error Detected: {exec_result['error_type']}")
                
                if run_and_debug_btn or not exec_result["success"]:
                    with st.spinner("Analyzing NLP tokens, predicting concept gap, and generating AI explanation..."):
                        pred_res = predictor.predict_concept_gap(
                            error_message=exec_result["error_message"],
                            code_snippet=user_code,
                            student_id=username
                        )
                        ai_exp = explainer.generate_explanation(pred_res)
                        
                        db.log_attempt(
                            student_id=username,
                            code=user_code,
                            error_type=exec_result["error_type"],
                            error_message=exec_result["error_message"],
                            predicted_concept=pred_res["predicted_concept"],
                            confidence=pred_res["confidence"],
                            signals=", ".join(pred_res["signals"])
                        )
                    
                    st.markdown("<div class='section-header'>ML Concept Gap & AI Diagnosis</div>", unsafe_allow_html=True)
                    
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.markdown(f"""
                        <div style='background-color: #fffdfa; border: 1px solid #ddb892; border-radius: 10px; padding: 16px;'>
                            <div style='font-size: 0.75rem; color: #7f5539; font-weight: 700; text-transform: uppercase;'>Predicted Concept Gap</div>
                            <div style='font-size: 1.2rem; font-weight: 800; color: #6f4e37; margin-top: 4px;'>{pred_res['predicted_concept']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_m2:
                        st.markdown(f"""
                        <div style='background-color: #fffdfa; border: 1px solid #ddb892; border-radius: 10px; padding: 16px;'>
                            <div style='font-size: 0.75rem; color: #7f5539; font-weight: 700; text-transform: uppercase;'>Model Confidence</div>
                            <div style='font-size: 1.2rem; font-weight: 800; color: #4a6b5d; margin-top: 4px;'>{pred_res['confidence']:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_m3:
                        st.markdown(f"""
                        <div style='background-color: #fffdfa; border: 1px solid #ddb892; border-radius: 10px; padding: 16px;'>
                            <div style='font-size: 0.75rem; color: #7f5539; font-weight: 700; text-transform: uppercase;'>Classified Error Type</div>
                            <div style='font-size: 1.2rem; font-weight: 800; color: #8c2d19; margin-top: 4px;'>{exec_result['error_type']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("")
                    
                    col_exp_left, col_exp_right = st.columns(2)
                    
                    with col_exp_left:
                        st.markdown("<div class='light-card'>", unsafe_allow_html=True)
                        st.markdown("### What Happened?")
                        st.write(ai_exp["what_happened"])
                        st.markdown("### Why It Happened?")
                        st.write(ai_exp["why_it_happened"])
                        st.markdown("### Why You May Have Made This Mistake")
                        st.write(ai_exp["why_mistake_made"])
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col_exp_right:
                        st.markdown("<div class='light-card'>", unsafe_allow_html=True)
                        st.markdown("### How to Fix It (Corrected Code)")
                        st.code(ai_exp["corrected_code"], language="python")
                        st.markdown("### Runnable Example")
                        st.code(ai_exp["simple_example"], language="python")
                        st.success(f"Actionable Advice: {ai_exp['learning_recommendation']}")
                        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# TAB 2: EASY, MEDIUM & HARD CODING LEVELS
# ==========================================
with tab_question_bank:
    st.markdown("<div class='section-header'>Coding Questions & Levels (Easy, Medium, Hard)</div>", unsafe_allow_html=True)
    st.markdown("Solve coding questions to record completed code into the database and increase your user progress metrics!")
    
    selected_diff = st.radio(
        "Select Level Difficulty Track:",
        ["All Levels", "Easy", "Medium", "Hard"],
        horizontal=True
    )
    
    filtered_questions = get_questions_by_difficulty(selected_diff if selected_diff != "All Levels" else "All")
    
    st.divider()
    
    for q in filtered_questions:
        q_id = q["id"]
        is_completed = q_id in completed_ids
        
        diff_class = "badge-easy" if q["difficulty"] == "Easy" else ("badge-medium" if q["difficulty"] == "Medium" else "badge-hard")
        status_text = "Solved & Recorded" if is_completed else "Unsolved"
        
        with st.expander(f"{q['title']} — ({q['difficulty']}) [{status_text}]", expanded=not is_completed):
            st.markdown(f"**Goal**: {q['description']}")
            st.markdown(f"**Difficulty**: <span class='{diff_class}'>{q['difficulty']}</span> &nbsp; **Category**: `{q['category']}` &nbsp; **XP Reward**: `+{q['xp']} XP`", unsafe_allow_html=True)
            st.markdown(f"Hint: {q['hint']}")
            
            q_code_key = f"q_code_{q_id}"
            user_q_code = st.text_area(
                f"Write your Python solution for {q['id']}:",
                value=q["starter_code"],
                height=160,
                key=q_code_key
            )
            
            c_col1, c_col2 = st.columns([1, 1])
            with c_col1:
                run_q_btn = st.button(f"Run & Explain Error ({q_id})", key=f"btn_run_{q_id}", type="secondary")
            with c_col2:
                sub_q_btn = st.button(f"Submit & Record Solution ({q_id})", key=f"btn_sub_{q_id}", type="primary")
            
            if run_q_btn or sub_q_btn:
                with st.spinner("Executing and validating code solution..."):
                    exec_res = execute_user_code(user_q_code)
                
                st.markdown("##### Execution Output:")
                if exec_res["success"]:
                    st.markdown(f"<div class='console-output'>{exec_res['output']}</div>", unsafe_allow_html=True)
                    
                    expected = q["expected_output"].strip()
                    output_actual = exec_res["output"].strip()
                    
                    if expected in output_actual or output_actual == expected:
                        st.success(f"Correct Answer! Solution for '{q['title']}' passed all checks!")
                        
                        record_res = db.record_submission(
                            username=username,
                            question_id=q_id,
                            difficulty=q["difficulty"],
                            question_title=q["title"],
                            submitted_code=user_q_code,
                            status="PASSED",
                            xp_earned=q["xp"]
                        )
                        
                        if record_res["first_time_passed"]:
                            st.info(f"+{q['xp']} XP recorded to database for @{username}! Progress updated.")
                            st.rerun()
                        else:
                            st.info("Code recorded in database (already completed previously).")
                    else:
                        st.warning(f"Code ran without errors, but output did not match expected result.\nExpected: `{expected}`\nActual: `{output_actual}`")
                else:
                    st.markdown(f"<div class='console-output' style='color: #f87171;'>{exec_res['error_message']}</div>", unsafe_allow_html=True)
                    
                    pred_res = predictor.predict_concept_gap(
                        error_message=exec_res["error_message"],
                        code_snippet=user_q_code,
                        student_id=username
                    )
                    ai_exp = explainer.generate_explanation(pred_res)
                    
                    db.log_attempt(
                        student_id=username,
                        code=user_q_code,
                        error_type=exec_res["error_type"],
                        error_message=exec_res["error_message"],
                        predicted_concept=pred_res["predicted_concept"],
                        confidence=pred_res["confidence"],
                        signals=", ".join(pred_res["signals"])
                    )
                    
                    db.record_submission(
                        username=username,
                        question_id=q_id,
                        difficulty=q["difficulty"],
                        question_title=q["title"],
                        submitted_code=user_q_code,
                        status="FAILED",
                        xp_earned=0
                    )
                    
                    st.markdown("#### AI Error Explanation & Concept Gap:")
                    st.error(f"Concept Gap Detected: {pred_res['predicted_concept']} ({pred_res['confidence']:.1f}% confidence)")
                    st.write(f"What happened: {ai_exp['what_happened']}")
                    st.write(f"Why it happened: {ai_exp['why_it_happened']}")
                    st.code(ai_exp['corrected_code'], language="python")


# ==========================================
# TAB 3: MY SOLVED CODE DATABASE
# ==========================================
with tab_my_code:
    st.markdown("<div class='section-header'>Completed Code Database Records</div>", unsafe_allow_html=True)
    st.markdown(f"Below are all recorded code submissions and completed challenges stored in SQLite for **@{username}**.")
    
    submissions_df = db.get_user_completed_submissions(username)
    
    if not submissions_df.empty:
        st.dataframe(submissions_df[['submitted_at', 'question_id', 'difficulty', 'question_title', 'status', 'xp_earned']], use_container_width=True)
        
        st.markdown("### Detailed Solved Code Snippets:")
        for idx, row in submissions_df.iterrows():
            if row['status'] == 'PASSED':
                with st.expander(f"{row['question_id']} - {row['question_title']} ({row['difficulty']}) — Submitted: {row['submitted_at']}"):
                    st.code(row['submitted_code'], language="python")
    else:
        st.info("No completed code submissions recorded yet. Go to Tab 2 to solve your first coding question!")


# ==========================================
# TAB 4: USER R ANALYTICS & PROGRESS
# ==========================================
with tab_r_analytics:
    st.markdown("<div class='section-header'>Personal R Progress Analytics & Visualizations</div>", unsafe_allow_html=True)
    st.markdown(f"Generate R graphics based strictly on **@{username}'s** execution history and database records.")
    
    col_r_actions, col_r_stats = st.columns([2, 1])
    
    with col_r_actions:
        st.markdown("Click below to refresh R statistical scripts (`r_user_progress.R`, `learning_analysis.R`) using your live database attempts.")
        refresh_r_btn = st.button("Update My R Progress Graphs", type="primary", key="btn_refresh_r")
        
        if refresh_r_btn:
            with st.spinner(f"Exporting history for @{username} and executing R scripts..."):
                csv_path = db.export_all_history_csv(username=username)
                r_res = r_runner.run_analysis(csv_path)
                if r_res["status"] == "success":
                    st.success(f"R Analysis rendered using `{r_res['rscript_path']}` for @{username}!")
                else:
                    st.error(f"R Script Error: {r_res.get('message')}")

    img_progress = "reports/r_user_progress.png"
    img_concept = "reports/errors_by_concept.png"
    img_time = "reports/errors_over_time.png"
    img_type = "reports/student_concept_performance.png"

    st.divider()

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        if os.path.exists(img_progress):
            st.image(img_progress, caption=f"R Plot 1: Learning Progress Curve (@{username})", use_container_width=True)
        if os.path.exists(img_concept):
            st.image(img_concept, caption=f"R Plot 2: Concept Gap Breakdown (@{username})", use_container_width=True)

    with r_col2:
        if os.path.exists(img_time):
            st.image(img_time, caption=f"R Plot 3: Detection Confidence Over Time (@{username})", use_container_width=True)
        if os.path.exists(img_type):
            st.image(img_type, caption=f"R Plot 4: Classified Error Frequency (@{username})", use_container_width=True)


# ==========================================
# TAB 5: CONCEPT HANDBOOK
# ==========================================
with tab_guide:
    st.markdown("<div class='section-header'>Programming Concept Gap Reference Guide</div>", unsafe_allow_html=True)
    st.markdown("Explore detailed explanations, sample triggers, and fix recommendations across all 10 core Python programming concepts.")
    
    kb = explainer.CONCEPT_KNOWLEDGE_BASE
    for concept_name, details in kb.items():
        with st.expander(f"Concept: {concept_name}"):
            st.markdown(f"**What Happens**: {details['what_happened']}")
            st.markdown(f"**Why It Happens**: {details['why_it_happened']}")
            st.markdown(f"**Common Misconception**: {details['why_mistake_made']}")
            st.markdown("**Corrected Code Example:**")
            st.code(details['corrected_code'], language="python")
            st.markdown(f"Recommendation: {details['recommendation']}")

st.divider()
st.caption(f"CodeBreak System — Logged in as {full_name} (@{username})")
