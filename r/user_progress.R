# user_progress.R
# Generates R visualizations for student learning curve, level progress, and concept gap decay in Mocha & Cream theme.

suppressPackageStartupMessages({
  if (!require("jsonlite", quietly = TRUE)) {}
})

input_csv <- "data/processed/all_student_history.csv"
reports_dir <- "reports"

dir.create(reports_dir, showWarnings = FALSE, recursive = TRUE)

# Function to render empty state graphics when user has no attempts yet
render_empty_state <- function(filename, title_text) {
  png(filename = file.path(reports_dir, filename), width = 850, height = 520, res = 120)
  par(bg = "#fffdfa", fg = "#3c2a21", col.axis = "#7f5539", col.main = "#6f4e37", font.main = 2)
  plot(1, type = "n", xlab = "", ylab = "", xlim = c(0, 10), ylim = c(0, 10), axes = FALSE, main = title_text)
  text(5, 5, "No execution attempts logged yet.\nSubmit code or complete level questions to generate your live R graphs!", col = "#7f5539", cex = 1.1)
  box(col = "#ddb892")
  dev.off()
}

if (!file.exists(input_csv)) {
  render_empty_state("r_user_progress.png", "Student Learning Curve (R Analytics)")
  render_empty_state("errors_by_concept.png", "Programming Concept Gaps Frequency")
  cat("Created empty state R plots.\n")
  quit(status = 0)
}

data <- read.csv(input_csv, stringsAsFactors = FALSE)
if (nrow(data) == 0) {
  render_empty_state("r_user_progress.png", "Student Learning Curve (R Analytics)")
  render_empty_state("errors_by_concept.png", "Programming Concept Gaps Frequency")
  cat("Created empty state R plots for empty user data.\n")
  quit(status = 0)
}

# --- Plot 1: User Learning Curve & XP Progress Over Time (Mocha & Cream Theme) ---
png(filename = file.path(reports_dir, "r_user_progress.png"), width = 900, height = 550, res = 120)

par(
  mar = c(5, 5, 4, 2) + 0.1,
  bg = "#fffdfa",
  fg = "#3c2a21",
  col.axis = "#5c4033",
  col.lab = "#3c2a21",
  col.main = "#6f4e37",
  font.main = 2
)

attempts <- 1:nrow(data)
cum_conf <- cumsum(data$confidence) / attempts

plot(
  attempts,
  cum_conf,
  type = "o",
  col = "#6f4e37",
  pch = 19,
  cex = 1.2,
  lwd = 3,
  main = "Student Learning Curve & Progress Trend (R Analytics)",
  xlab = "Attempt Sequence Number",
  ylab = "Cumulative Diagnostic Accuracy (%)",
  ylim = c(0, 100),
  bty = "n"
)

grid(nx = NULL, ny = NULL, col = "#e6ccb2", lty = "solid", lwd = 1)
lines(attempts, cum_conf, col = "#6f4e37", lwd = 3)
points(attempts, cum_conf, col = "#9c6644", pch = 21, bg = "#ddb892", cex = 1.3)

if (length(attempts) >= 3) {
  smooth_fit <- loess(cum_conf ~ attempts, span = 0.75)
  lines(attempts, predict(smooth_fit), col = "#4a6b5d", lwd = 2, lty = 2)
  legend(
    "bottomright",
    legend = c("Attempt Accuracy", "Progress Trendline"),
    col = c("#6f4e37", "#4a6b5d"),
    lwd = c(3, 2),
    lty = c(1, 2),
    bty = "n",
    cex = 0.85
  )
}

dev.off()
cat("Saved plot: reports/r_user_progress.png\n")

# --- Plot 2: Errors by Concept Breakdown (Mocha & Cream Theme) ---
png(filename = file.path(reports_dir, "errors_by_concept.png"), width = 900, height = 550, res = 120)

par(
  mar = c(8, 5, 4, 2) + 0.1,
  bg = "#fffdfa",
  fg = "#3c2a21",
  col.axis = "#5c4033",
  col.lab = "#3c2a21",
  col.main = "#7f5539",
  font.main = 2
)

concept_counts <- table(data$predicted_concept)
concept_counts <- sort(concept_counts, decreasing = TRUE)

bp <- barplot(
  concept_counts,
  main = "Programming Concept Gaps Frequency (R Plot)",
  col = colorRampPalette(c("#6f4e37", "#9c6644", "#ddb892"))(length(concept_counts)),
  border = "#e6ccb2",
  las = 2,
  cex.names = 0.85,
  ylab = "Error Count",
  bty = "n"
)

grid(nx = NA, ny = NULL, col = "#e6ccb2", lty = "solid")
dev.off()
cat("Saved plot: reports/errors_by_concept.png\n")
