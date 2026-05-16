import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Styling constants for Plotly
BG_COLOR = "#0D1117"
CARD_COLOR = "#161B22"
TEXT_COLOR = "#E6EDF3"
GRID_COLOR = "#21262D"
PALETTE = ["#1DB954", "#E63946", "#F4A261", "#457B9D", "#A8DADC"]

def apply_common_layout(fig):
    fig.update_layout(
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR, family="sans-serif"),
        title_font=dict(size=18, color=TEXT_COLOR),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        legend=dict(bgcolor=CARD_COLOR, bordercolor=GRID_COLOR, font=dict(color=TEXT_COLOR)),
        margin=dict(t=50, b=30, l=30, r=30)
    )
    return fig

def plot_toss_win_pct(toss_data):
    overall_pct = toss_data.get("overall_pct", 0)
    loser_pct = 100 - overall_pct
    by_dec = toss_data.get("by_decision", pd.DataFrame())
    
    categories = ["Toss Winner", "Toss Loser"]
    values = [overall_pct, loser_pct]
    colors = [PALETTE[0], PALETTE[1]]
    
    if not by_dec.empty and "toss_decision" in by_dec.columns:
        categories += [f"Chose to {str(r).title()}" for r in by_dec["toss_decision"]]
        values += by_dec["win_pct"].tolist()
        colors += [PALETTE[2], PALETTE[3]]
        
    fig = go.Figure(data=[
        go.Bar(x=categories, y=values, marker_color=colors, text=[f"{v:.1f}%" for v in values], textposition="outside")
    ])
    
    fig.add_hline(y=50, line_dash="dash", line_color=TEXT_COLOR, annotation_text="50% Baseline", opacity=0.5)
    fig.update_layout(title="Win % - Toss Winner vs Loser & Decision Breakdown", yaxis_title="Win Percentage (%)", yaxis_range=[0, max(values)*1.2 if values else 100])
    return apply_common_layout(fig)

def plot_toss_season_trend(toss_data):
    trend_df = toss_data.get("season_trend", pd.DataFrame())
    if trend_df.empty:
        return go.Figure()
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df["season"], y=trend_df["win_pct"],
        mode='lines+markers+text',
        name='Win %',
        line=dict(color=PALETTE[0], width=3),
        marker=dict(size=8),
        text=[f"{v:.0f}%" for v in trend_df["win_pct"]],
        textposition="top center"
    ))
    fig.add_hline(y=50, line_dash="dash", line_color=TEXT_COLOR, opacity=0.5)
    fig.update_layout(title="Season-by-Season Toss Advantage Trend", xaxis_title="Season", yaxis_title="Toss Winners' Match Win %", xaxis=dict(type='category'))
    return apply_common_layout(fig)

def plot_phase_analysis(phase_avg):
    if phase_avg.empty:
        return go.Figure()
        
    fig = px.bar(
        phase_avg, x="phase", y="avg_runs", color="outcome", barmode="group",
        color_discrete_map={"Winner": PALETTE[0], "Loser": PALETTE[1]},
        text="avg_runs"
    )
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(title="Average Runs per Match Phase - Winners vs Losers", xaxis_title="Match Phase", yaxis_title="Average Runs", yaxis_range=[0, phase_avg["avg_runs"].max()*1.2])
    return apply_common_layout(fig)

def plot_top_batters(batters):
    if batters.empty:
        return go.Figure()
    bat_sorted = batters.sort_values("total_runs", ascending=True)
    fig = px.bar(
        bat_sorted, y="batter", x="total_runs", orientation='h',
        text="total_runs", color="total_runs", color_continuous_scale="YlOrRd"
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(title="Top Batters - Career Runs", xaxis_title="Total Runs", yaxis_title="")
    return apply_common_layout(fig)

def plot_top_bowlers(bowlers):
    if bowlers.empty:
        return go.Figure()
    bow_sorted = bowlers.sort_values("wickets", ascending=True)
    fig = px.bar(
        bow_sorted, y="bowler", x="wickets", orientation='h',
        text="wickets", color="wickets", color_continuous_scale="GnBu"
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(title="Top Bowlers - Career Wickets", xaxis_title="Wickets Taken", yaxis_title="")
    return apply_common_layout(fig)

def plot_season_scoring(df):
    innings_runs = df[df["innings"].isin([1, 2])].groupby(["match_id", "season", "innings"])["runs_total"].sum().reset_index(name="innings_runs")
    season_avg = innings_runs.groupby("season")["innings_runs"].mean().reset_index().dropna(subset=["season"]).sort_values("season")

    if season_avg.empty:
        return go.Figure()
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=season_avg["season"], y=season_avg["innings_runs"],
        mode='lines+markers+text',
        line=dict(color=PALETTE[3], width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor=f'rgba(69, 123, 157, 0.2)',
        text=[f"{v:.0f}" for v in season_avg["innings_runs"]],
        textposition="top center"
    ))
    fig.update_layout(title="IPL Scoring Trend - Average Innings Runs per Season", xaxis_title="Season", yaxis_title="Average Innings Score (Runs)", xaxis=dict(type='category'))
    min_val = season_avg["innings_runs"].min() * 0.85
    fig.update_yaxes(range=[min_val, season_avg["innings_runs"].max() * 1.15])
    return apply_common_layout(fig)
