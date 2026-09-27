import sys
import io
import traceback

def execute_user_code(code_str: str) -> dict:
    """
    Safely executes user Python code, capturing stdout, stderr, and any runtime/syntax exceptions.
    Returns a dictionary with execution status, output, and formatted error details.
    """
    buffer = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = buffer
    sys.stderr = buffer

    # Execution scope
    exec_globals = {
        "__name__": "__main__",
        "__doc__": None,
        "__package__": None,
    }

    try:
        # First try compiling to catch SyntaxError / IndentationError early
        compiled_code = compile(code_str, "<student_code>", "exec")
        exec(compiled_code, exec_globals)
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        output = buffer.getvalue().strip()
        return {
            "success": True,
            "output": output if output else "✅ Code executed successfully with no print output.",
            "error_type": None,
            "error_message": None,
            "traceback": None
        }
    except Exception as e:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        output = buffer.getvalue().strip()
        
        err_type = type(e).__name__
        err_msg = str(e)
        
        # Format clean execution error string
        full_err_str = f"{err_type}: {err_msg}"
        tb_lines = traceback.format_exc()
        
        return {
            "success": False,
            "output": output,
            "error_type": err_type,
            "error_message": full_err_str,
            "traceback": tb_lines
        }
