import pandas as pd
import numpy as np

def analyse_toss(matches: pd.DataFrame) -> dict:
    if "toss_win_match_win" not in matches.columns:
        return {"overall_pct": 0, "by_decision": pd.DataFrame(), "season_trend": pd.DataFrame(), "total_matches": 0}
        
    total = len(matches)
    toss_win_cnt = matches["toss_win_match_win"].sum()
    overall_pct = toss_win_cnt / total * 100 if total > 0 else 0

    by_decision = (
        matches.groupby("toss_decision")["toss_win_match_win"]
        .agg(wins="sum", total="count")
        .assign(win_pct=lambda x: np.where(x["total"] > 0, x["wins"] / x["total"] * 100, 0))
        .reset_index()
    )

    season_trend = (
        matches.groupby("season")["toss_win_match_win"]
        .agg(wins="sum", total="count")
        .assign(win_pct=lambda x: np.where(x["total"] > 0, x["wins"] / x["total"] * 100, 0))
        .reset_index()
        .dropna(subset=["season"])
        .sort_values("season")
    )

    return {
        "overall_pct": overall_pct,
        "by_decision": by_decision,
        "season_trend": season_trend,
        "total_matches": total,
    }

def classify_phase(over_1idx: pd.Series) -> pd.Series:
    conditions = [
        over_1idx.between(1, 6),
        over_1idx.between(7, 15),
        over_1idx.between(16, 20),
    ]
    choices = ["Powerplay (1-6)", "Middle (7-15)", "Death (16-20)"]
    return pd.Series(np.select(conditions, choices, default="Unknown"), index=over_1idx.index)

def analyse_phases(df: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    work = df[df["innings"].isin([1, 2])].copy()
    work["phase"] = classify_phase(work["over_1idx"])

    # Vectorized match winner merge
    work = work.merge(
        matches[["match_id", "winner"]].rename(columns={"winner": "match_winner"}),
        on="match_id", how="left"
    )

    work["outcome"] = np.where(work["batting_team"] == work["match_winner"], "Winner", "Loser")

    phase_match = work.groupby(["match_id", "phase", "outcome"])["runs_total"].sum().reset_index()
    phase_avg = phase_match.groupby(["phase", "outcome"])["runs_total"].mean().reset_index().rename(columns={"runs_total": "avg_runs"})

    phase_order = ["Powerplay (1-6)", "Middle (7-15)", "Death (16-20)"]
    phase_avg["phase"] = pd.Categorical(phase_avg["phase"], categories=phase_order, ordered=True)
    phase_avg = phase_avg.sort_values(["phase", "outcome"]).reset_index(drop=True)
    return phase_avg

def top_batters(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    batter_runs = df.groupby("batter")["runs_batter"].sum().reset_index(name="total_runs")
    batter_runs = batter_runs.sort_values("total_runs", ascending=False).head(n).reset_index(drop=True)
    batter_runs.index += 1
    batter_runs.index.name = "Rank"

    # Optimize innings counting with nunique
    innings = df.groupby("batter")["match_id"].nunique().reset_index(name="innings")
    
    # Vectorized boundary counting
    fours = df[df["runs_batter"] == 4].groupby("batter").size().reset_index(name="fours")
    sixes = df[df["runs_batter"] == 6].groupby("batter").size().reset_index(name="sixes")

    batter_runs = (
        batter_runs
        .merge(innings, on="batter", how="left")
        .merge(fours, on="batter", how="left")
        .merge(sixes, on="batter", how="left")
    )
    
    batter_runs["average"] = np.where(batter_runs["innings"] > 0, (batter_runs["total_runs"] / batter_runs["innings"]).round(2), 0)
    batter_runs[["fours", "sixes"]] = batter_runs[["fours", "sixes"]].fillna(0).astype(int)
    return batter_runs

def top_bowlers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    bowler_wickets = (
        df[df["is_wicket"] & ~df["wicket_kind"].isin(["run out", "retired hurt", "retired out", "obstructing the field"])]
        .groupby("bowler").size().reset_index(name="wickets")
        .sort_values("wickets", ascending=False).head(n).reset_index(drop=True)
    )
    bowler_wickets.index += 1
    bowler_wickets.index.name = "Rank"

    runs_conceded = df.groupby("bowler")["runs_total"].sum().reset_index(name="runs_conceded")
    balls_bowled = df[df["extras_wides"] == 0].groupby("bowler").size().reset_index(name="balls")
    
    bowler_wickets = bowler_wickets.merge(runs_conceded, on="bowler", how="left").merge(balls_bowled, on="bowler", how="left")
    
    bowler_wickets["economy"] = np.where(
        bowler_wickets["balls"] > 0, 
        (bowler_wickets["runs_conceded"] / (bowler_wickets["balls"] / 6)).round(2), 
        0
    )
    return bowler_wickets

def generate_insights(toss_data, phase_avg, batters, bowlers, df, matches) -> list[str]:
    insights = []
    
    try:
        overall = toss_data.get("overall_pct", 0)
        edge = overall - 50
        
        by_dec = toss_data.get("by_decision", pd.DataFrame())
        if not by_dec.empty and "toss_decision" in by_dec.columns:
            by_dec = by_dec.set_index("toss_decision")
            field_pct = by_dec.loc["field", "win_pct"] if "field" in by_dec.index else 0
            bat_pct = by_dec.loc["bat", "win_pct"] if "bat" in by_dec.index else 0
        else:
            field_pct = bat_pct = 0

        insights.append(
            f"INSIGHT 1 - Toss Impact: Toss winners win {overall:.1f}% of matches ({edge:.1f}pp above 50%). "
            f"Fielding first yields {field_pct:.1f}% win rate vs {bat_pct:.1f}% for batting first."
        )

        if not phase_avg.empty:
            winner_death = phase_avg.query("phase == 'Death (16-20)' and outcome == 'Winner'")["avg_runs"].values
            loser_death = phase_avg.query("phase == 'Death (16-20)' and outcome == 'Loser'")["avg_runs"].values
            winner_pp = phase_avg.query("phase == 'Powerplay (1-6)' and outcome == 'Winner'")["avg_runs"].values
            loser_pp = phase_avg.query("phase == 'Powerplay (1-6)' and outcome == 'Loser'")["avg_runs"].values
            
            diff_death = winner_death[0] - loser_death[0] if len(winner_death) > 0 and len(loser_death) > 0 else 0
            diff_pp = winner_pp[0] - loser_pp[0] if len(winner_pp) > 0 and len(loser_pp) > 0 else 0
            
            insights.append(
                f"INSIGHT 2 - Match Phases: Winners outscore losers by {diff_death:.1f} runs in the Death overs, "
                f"compared to a {diff_pp:.1f} run gap in the Powerplay."
            )

        if not batters.empty and not bowlers.empty:
            top_batter = batters.iloc[0]
            boundary_runs = (top_batter["fours"] * 4) + (top_batter["sixes"] * 6)
            boundary_pct = (boundary_runs / top_batter["total_runs"] * 100) if top_batter["total_runs"] > 0 else 0
            
            total_sixes = df["runs_batter"].eq(6).sum()
            top_bowler = bowlers.iloc[0]
            
            insights.append(
                f"INSIGHT 3 - Top Performers: {top_batter['batter']} leads with {top_batter['total_runs']} runs "
                f"({boundary_pct:.1f}% from boundaries). {top_bowler['bowler']} leads with {top_bowler['wickets']} wickets. "
                f"Total tournament sixes: {total_sixes}."
            )
            
    except Exception as e:
        insights.append(f"Could not generate insights due to error: {e}")
        
    return insights
