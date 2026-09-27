# analyze_errors.R
# Statistical and Learning Pattern Analysis script for CodeBreak in R.

suppressPackageStartupMessages({
  if (!require("jsonlite", quietly = TRUE)) {
    # If jsonlite is missing, we write formatted text or basic output
  }
})

input_csv <- "data/processed/all_student_history.csv"
output_json <- "reports/r_analysis_summary.json"

dir.create("reports", showWarnings = FALSE, recursive = TRUE)

if (!file.exists(input_csv)) {
  cat("Input history CSV not found at", input_csv, "\n")
  quit(status = 0)
}

data <- read.csv(input_csv, stringsAsFactors = FALSE)
total_attempts <- nrow(data)

if (total_attempts == 0) {
  cat("No attempt records found in CSV.\n")
  quit(status = 0)
}

# 1. Concept Error Frequency
concept_freq <- table(data$predicted_concept)
concept_df <- as.data.frame(concept_freq)
colnames(concept_df) <- c("Concept", "ErrorCount")
concept_df <- concept_df[order(-concept_df$ErrorCount), ]

# 2. Error Type Frequency
error_type_freq <- table(data$error_type)
error_type_df <- as.data.frame(error_type_freq)
colnames(error_type_df) <- c("ErrorType", "Count")
error_type_df <- error_type_df[order(-error_type_df$Count), ]

# 3. Student Summary
student_freq <- table(data$student_id)
student_df <- as.data.frame(student_freq)
colnames(student_df) <- c("StudentID", "TotalErrors")

# 4. Top Weak Concept
top_weak_concept <- as.character(concept_df$Concept[1])
top_weak_count <- as.numeric(concept_df$ErrorCount[1])

# Summary statistics text
summary_info <- list(
  total_attempts = total_attempts,
  unique_students = length(unique(data$student_id)),
  top_weak_concept = top_weak_concept,
  top_weak_count = top_weak_count,
  most_common_error = as.character(error_type_df$ErrorType[1]),
  concept_distribution = setNames(as.list(concept_df$ErrorCount), concept_df$Concept),
  error_type_distribution = setNames(as.list(error_type_df$Count), error_type_df$ErrorType)
)

cat("==========================================\n")
cat("      CODEBREAK R STATISTICAL ANALYSIS    \n")
cat("==========================================\n")
cat("Total Analyzed Student Attempts:", total_attempts, "\n")
cat("Most Frequent Concept Gap:", top_weak_concept, "(", top_weak_count, "occurrences )\n")
cat("Most Common Error Type:", summary_info$most_common_error, "\n\n")

if (require("jsonlite", quietly = TRUE)) {
  write(jsonlite::toJSON(summary_info, auto_unbox = TRUE, pretty = TRUE), output_json)
  cat("Statistical summary JSON written to", output_json, "\n")
} else {
  # Fallback basic JSON creation
  cat("JSON output skipped (jsonlite package not installed).\n")
}
