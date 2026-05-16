from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "ipl_ball_by_ball.csv"
CHARTS_DIR = ROOT / "outputs" / "charts"
TABLES_DIR = ROOT / "outputs" / "tables"

# Styling Configuration
PALETTE = ["#1DB954", "#E63946", "#F4A261", "#457B9D", "#A8DADC"]
BG_COLOR = "#0D1117"
CARD_COLOR = "#161B22"
TEXT_COLOR = "#E6EDF3"
GRID_COLOR = "#21262D"

PLOT_CONFIG = {
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": CARD_COLOR,
    "axes.edgecolor": GRID_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "axes.titlecolor": TEXT_COLOR,
    "axes.titlesize": 16,
    "axes.titlepad": 14,
    "axes.labelsize": 12,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.facecolor": CARD_COLOR,
    "legend.edgecolor": GRID_COLOR,
    "legend.labelcolor": TEXT_COLOR,
    "legend.fontsize": 11,
    "grid.color": GRID_COLOR,
    "grid.linewidth": 0.6,
    "font.family": "sans-serif",
    "text.color": TEXT_COLOR,
    "savefig.dpi": 180,
    "savefig.bbox": "tight",
    "savefig.facecolor": BG_COLOR,
}
