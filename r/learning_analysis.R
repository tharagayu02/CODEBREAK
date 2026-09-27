# learning_analysis.R
# Visual Learning Pattern Analysis script for CodeBreak in R (Mocha & Cream Theme).

input_csv <- "data/processed/all_student_history.csv"
reports_dir <- "reports"

dir.create(reports_dir, showWarnings = FALSE, recursive = TRUE)

if (!file.exists(input_csv)) {
  cat("Input history CSV not found at", input_csv, "\n")
  quit(status = 0)
}

data <- read.csv(input_csv, stringsAsFactors = FALSE)
if (nrow(data) == 0) {
  cat("No attempt records found.\n")
  quit(status = 0)
}

# --- Plot 1: Errors by Concept Bar Chart (Mocha & Cream Theme) ---
png(filename = file.path(reports_dir, "errors_by_concept.png"), width = 850, height = 520, res = 120)
concept_counts <- table(data$predicted_concept)
concept_counts <- sort(concept_counts, decreasing = TRUE)

par(
  mar = c(8, 5, 4, 2) + 0.1,
  bg = "#fffdfa",
  fg = "#3c2a21",
  col.axis = "#5c4033",
  col.lab = "#3c2a21",
  col.main = "#6f4e37",
  font.main = 2
)

bp <- barplot(
  concept_counts,
  main = "Student Error Distribution by Programming Concept",
  col = colorRampPalette(c("#6f4e37", "#9c6644", "#ddb892"))(length(concept_counts)),
  border = "#e6ccb2",
  las = 2,
  cex.names = 0.85,
  ylab = "Number of Errors"
)
grid(nx = NA, ny = NULL, col = "#e6ccb2", lty = "solid")
dev.off()
cat("Saved plot: reports/errors_by_concept.png\n")

# --- Plot 2: Errors Over Time Line Chart (Mocha & Cream Theme) ---
png(filename = file.path(reports_dir, "errors_over_time.png"), width = 850, height = 520, res = 120)
par(
  mar = c(5, 5, 4, 2) + 0.1,
  bg = "#fffdfa",
  fg = "#3c2a21",
  col.axis = "#5c4033",
  col.lab = "#3c2a21",
  col.main = "#7f5539",
  font.main = 2
)

attempts_index <- 1:nrow(data)
confidences <- data$confidence

plot(
  attempts_index,
  confidences,
  type = "o",
  col = "#7f5539",
  pch = 19,
  cex = 1.2,
  lwd = 2.5,
  main = "Concept Detection Confidence & Progress Over Time",
  xlab = "Attempt Sequence Number",
  ylab = "Model Confidence (%)",
  ylim = c(0, 100),
  bty = "n"
)
grid(col = "#e6ccb2", lty = "solid")
dev.off()
cat("Saved plot: reports/errors_over_time.png\n")

# --- Plot 3: Student Concept Performance Error Breakdown (Mocha & Cream Theme) ---
png(filename = file.path(reports_dir, "student_concept_performance.png"), width = 850, height = 520, res = 120)
par(
  mar = c(8, 5, 4, 2) + 0.1,
  bg = "#fffdfa",
  fg = "#3c2a21",
  col.axis = "#5c4033",
  col.lab = "#3c2a21",
  col.main = "#4a6b5d",
  font.main = 2
)

err_counts <- table(data$error_type)
err_counts <- sort(err_counts, decreasing = TRUE)

barplot(
  err_counts,
  main = "Frequency Breakdown of Error Types",
  col = colorRampPalette(c("#4a6b5d", "#7f9a8b", "#c2d6cb"))(length(err_counts)),
  border = "#e6ccb2",
  las = 2,
  cex.names = 0.85,
  ylab = "Count"
)
grid(nx = NA, ny = NULL, col = "#e6ccb2", lty = "solid")
dev.off()
cat("Saved plot: reports/student_concept_performance.png\n")
