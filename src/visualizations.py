import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import pandas as pd
import numpy as np

from config import PALETTE, BG_COLOR, TEXT_COLOR, PLOT_CONFIG

plt.rcParams.update(PLOT_CONFIG)

def plot_toss_analysis(toss_data: dict, save_path: Path):
    if toss_data["by_decision"].empty or toss_data["season_trend"].empty:
        return
        
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("IPL Toss Analysis - Does Winning the Toss Help?", fontsize=20, fontweight="bold", y=1.02, color=TEXT_COLOR)

    ax1 = axes[0]
    overall_pct = toss_data["overall_pct"]
    loser_pct = 100 - overall_pct
    by_dec = toss_data["by_decision"]

    categories = ["Toss Winner", "Toss Loser"] + [f"Chose to {str(r).title()}" for r in by_dec["toss_decision"]]
    values = [overall_pct, loser_pct] + by_dec["win_pct"].tolist()
    colors = [PALETTE[0], PALETTE[1]] + [PALETTE[2], PALETTE[3]]

    bars = ax1.bar(categories, values, color=colors[:len(categories)], width=0.55, zorder=3, edgecolor=BG_COLOR, linewidth=1.2)

    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8, f"{val:.1f}%", ha="center", va="bottom", fontsize=12, fontweight="bold", color=TEXT_COLOR)

    ax1.axhline(50, linestyle="--", color=TEXT_COLOR, alpha=0.35, linewidth=1.2, zorder=2)
    ax1.set_ylim(0, 75)
    ax1.set_ylabel("Win Percentage (%)")
    ax1.set_title("Win % - Toss Winner vs Loser & Breakdown by Toss Decision")
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax1.grid(axis="y", zorder=0)

    ax2 = axes[1]
    trend_df = toss_data["season_trend"]

    ax2.plot(trend_df["season"], trend_df["win_pct"], marker="o", color=PALETTE[0], linewidth=2.5, markersize=7, zorder=3)
    ax2.fill_between(trend_df["season"], trend_df["win_pct"], 50, where=(trend_df["win_pct"] >= 50), alpha=0.15, color=PALETTE[0], zorder=2)
    ax2.fill_between(trend_df["season"], trend_df["win_pct"], 50, where=(trend_df["win_pct"] < 50), alpha=0.15, color=PALETTE[1], zorder=2)
    ax2.axhline(50, linestyle="--", color=TEXT_COLOR, alpha=0.35, linewidth=1.2, zorder=2)

    for _, row in trend_df.iterrows():
        ax2.annotate(f"{row['win_pct']:.0f}%", xy=(row["season"], row["win_pct"]), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=8, color=TEXT_COLOR, alpha=0.8)

    ax2.set_xlabel("Season")
    ax2.set_ylabel("Toss Winners' Match Win %")
    ax2.set_title("Season-by-Season Toss Advantage Trend")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax2.set_xticks(trend_df["season"])
    ax2.set_xticklabels([str(int(s)) for s in trend_df["season"]], rotation=45, ha="right")
    ax2.set_ylim(30, 75)
    ax2.grid(axis="y", zorder=0)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_phase_analysis(phase_avg: pd.DataFrame, num_matches: int, save_path: Path):
    if phase_avg.empty:
        return
        
    fig, ax = plt.subplots(figsize=(13, 7))

    phases = phase_avg["phase"].unique()
    outcomes = ["Winner", "Loser"]
    x = np.arange(len(phases))
    width = 0.35

    for i, outcome in enumerate(outcomes):
        subset = phase_avg[phase_avg["outcome"] == outcome].set_index("phase").reindex(phases)
        bars = ax.bar(x + (i - 0.5) * width, subset["avg_runs"], width=width, label=f"{outcome}s", color=PALETTE[0] if outcome == "Winner" else PALETTE[1], zorder=3, edgecolor=BG_COLOR, linewidth=1.2)
        
        for bar, val in zip(bars, subset["avg_runs"]):
            if not np.isnan(val):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4, f"{val:.1f}", ha="center", va="bottom", fontsize=11, fontweight="bold", color=TEXT_COLOR)

    ax.set_xticks(x)
    ax.set_xticklabels(phases, fontsize=12)
    ax.set_ylabel("Average Runs per Match Phase")
    ax.set_title("Average Runs per Match Phase - Winners vs Losers", fontsize=17, pad=16)
    ax.legend(fontsize=12)
    ax.grid(axis="y", zorder=0)
    
    max_runs = phase_avg["avg_runs"].max()
    ax.set_ylim(0, (max_runs * 1.25) if not np.isnan(max_runs) else 100)
    ax.text(0.99, 0.98, f"Based on {num_matches:,} IPL matches", transform=ax.transAxes, ha="right", va="top", fontsize=9, color=TEXT_COLOR, alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_top_performers(batters: pd.DataFrame, bowlers: pd.DataFrame, save_path: Path):
    if batters.empty or bowlers.empty:
        return
        
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("IPL Top Performers", fontsize=20, fontweight="bold", y=1.02, color=TEXT_COLOR)

    bat_sorted = batters.sort_values("total_runs")
    colors_bat = sns.color_palette("YlOrRd", len(bat_sorted))

    bars_b = ax1.barh(bat_sorted["batter"], bat_sorted["total_runs"], color=colors_bat, edgecolor=BG_COLOR, linewidth=1.2, zorder=3)
    for bar, val in zip(bars_b, bat_sorted["total_runs"]):
        ax1.text(bar.get_width() + 30, bar.get_y() + bar.get_height() / 2, f"{val:,}", va="center", ha="left", fontsize=11, fontweight="bold", color=TEXT_COLOR)

    ax1.set_xlabel("Total Runs")
    ax1.set_title("Top Batters - Career Runs", fontsize=15)
    ax1.grid(axis="x", zorder=0)
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    bow_sorted = bowlers.sort_values("wickets")
    colors_bow = sns.color_palette("GnBu", len(bow_sorted))

    bars_w = ax2.barh(bow_sorted["bowler"], bow_sorted["wickets"], color=colors_bow, edgecolor=BG_COLOR, linewidth=1.2, zorder=3)
    for bar, val in zip(bars_w, bow_sorted["wickets"]):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, str(int(val)), va="center", ha="left", fontsize=11, fontweight="bold", color=TEXT_COLOR)

    ax2.set_xlabel("Wickets Taken")
    ax2.set_title("Top Bowlers - Career Wickets", fontsize=15)
    ax2.grid(axis="x", zorder=0)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_season_scoring(df: pd.DataFrame, save_path: Path):
    innings_runs = df[df["innings"].isin([1, 2])].groupby(["match_id", "season", "innings"])["runs_total"].sum().reset_index(name="innings_runs")
    season_avg = innings_runs.groupby("season")["innings_runs"].mean().reset_index().dropna(subset=["season"]).sort_values("season")

    if season_avg.empty:
        return
        
    fig, ax = plt.subplots(figsize=(13, 6))

    ax.plot(season_avg["season"], season_avg["innings_runs"], marker="o", color=PALETTE[3], linewidth=2.5, markersize=8, zorder=3)
    ax.fill_between(season_avg["season"], season_avg["innings_runs"], alpha=0.12, color=PALETTE[3], zorder=2)

    for _, row in season_avg.iterrows():
        ax.annotate(f"{row['innings_runs']:.0f}", xy=(row["season"], row["innings_runs"]), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=9, color=TEXT_COLOR, alpha=0.85)

    ax.set_xlabel("Season")
    ax.set_ylabel("Average Innings Score (Runs)")
    ax.set_title("IPL Scoring Trend - Average Innings Runs per Season", fontsize=17, pad=16)
    ax.set_xticks(season_avg["season"])
    ax.set_xticklabels([str(int(s)) for s in season_avg["season"]], rotation=45, ha="right")
    ax.grid(axis="y", zorder=0)
    
    min_runs = season_avg["innings_runs"].min()
    max_runs = season_avg["innings_runs"].max()
    ax.set_ylim(min_runs * 0.85, max_runs * 1.15)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
