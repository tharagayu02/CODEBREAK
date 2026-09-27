import os
import shutil
import subprocess
import json
import pandas as pd

class RRunner:
    """
    Python wrapper to execute R scripts (analyze_errors.R, learning_analysis.R, user_progress.R)
    and parse statistical output for Python/Streamlit integration.
    """

    def __init__(self, r_dir: str = "r", reports_dir: str = "reports"):
        self.r_dir = r_dir
        self.reports_dir = reports_dir
        self.rscript_bin = self._find_rscript()

    def _find_rscript(self) -> str:
        """
        Locates Rscript executable on Windows PATH or standard R installation paths.
        """
        bin_path = shutil.which("Rscript")
        if bin_path:
            return bin_path

        # Standard R Windows paths check
        candidates = [
            r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe",
            r"C:\Program Files\R\R-4.6.1\bin\x64\Rscript.exe",
            r"C:\Program Files\R\R-4.6.0\bin\Rscript.exe",
            r"C:\Program Files\R\R-4.5.0\bin\Rscript.exe",
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        
        return "Rscript"

    def run_analysis(self, history_csv_path: str = "data/processed/all_student_history.csv") -> dict:
        """
        Executes analyze_errors.R, learning_analysis.R, and user_progress.R, returning analysis results.
        """
        if not os.path.exists(history_csv_path):
            return {"status": "error", "message": f"History CSV not found at {history_csv_path}"}

        analyze_script = os.path.join(self.r_dir, "analyze_errors.R")
        visual_script = os.path.join(self.r_dir, "learning_analysis.R")
        progress_script = os.path.join(self.r_dir, "user_progress.R")

        logs = []
        try:
            # 1. Run statistical analysis
            res1 = subprocess.run(
                [self.rscript_bin, analyze_script],
                capture_output=True,
                text=True,
                check=False
            )
            logs.append(res1.stdout)

            # 2. Run visual plots generation
            res2 = subprocess.run(
                [self.rscript_bin, visual_script],
                capture_output=True,
                text=True,
                check=False
            )
            logs.append(res2.stdout)

            # 3. Run user progress graph generation
            if os.path.exists(progress_script):
                res3 = subprocess.run(
                    [self.rscript_bin, progress_script],
                    capture_output=True,
                    text=True,
                    check=False
                )
                logs.append(res3.stdout)

            summary_json_path = os.path.join(self.reports_dir, "r_analysis_summary.json")
            if os.path.exists(summary_json_path):
                with open(summary_json_path, "r") as f:
                    summary_data = json.load(f)
            else:
                summary_data = {"raw_output": "\n".join(logs)}

            return {
                "status": "success",
                "rscript_path": self.rscript_bin,
                "summary": summary_data,
                "logs": "\n".join(logs),
                "plots": {
                    "errors_by_concept": os.path.join(self.reports_dir, "errors_by_concept.png"),
                    "errors_over_time": os.path.join(self.reports_dir, "errors_over_time.png"),
                    "student_concept_performance": os.path.join(self.reports_dir, "student_concept_performance.png"),
                    "r_user_progress": os.path.join(self.reports_dir, "r_user_progress.png")
                }
            }

        except Exception as e:
            return {"status": "error", "message": str(e), "logs": "\n".join(logs)}


if __name__ == "__main__":
    runner = RRunner()
    result = runner.run_analysis()
    print("R Execution Result Status:", result["status"])
    print("Executable used:", result.get("rscript_path"))
