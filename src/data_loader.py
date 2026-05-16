import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_and_clean(path: Path) -> pd.DataFrame:
    """Load the IPL ball-by-ball CSV and apply data-quality fixes."""
    try:
        logger.info(f"Loading data from {path}")
        df = pd.read_csv(path, low_memory=False)
        logger.info(f"Raw shape: {df.shape}")
        
        # Check required columns
        required_cols = ["season", "over", "runs_batter", "runs_extras", "runs_total", 
                         "extras_wides", "extras_noballs", "wicket_kind", "date", 
                         "match_id", "innings", "ball"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Missing required columns in dataset: {missing_cols}")
        
        # Season normalization
        df["season"] = df["season"].astype(str).str.split("/").str[0].str.strip()
        df["season"] = pd.to_numeric(df["season"], errors="coerce").astype("Int64")
        
        # Convert 0-indexed overs to 1-indexed
        df["over_1idx"] = df["over"] + 1
        
        # Ensure numeric delivery columns
        num_cols = ["runs_batter", "runs_extras", "runs_total", "extras_wides", "extras_noballs"]
        df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
        
        # Boolean wicket flag
        df["is_wicket"] = df["wicket_kind"].notna()
        
        # Date parsing
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        
        # Drop duplicates
        before = len(df)
        df.drop_duplicates(subset=["match_id", "innings", "over", "ball"], keep="first", inplace=True)
        after = len(df)
        if before != after:
            logger.warning(f"Dropped {before - after} duplicate deliveries")
            
        logger.info(f"Clean shape: {df.shape}")
        return df
        
    except FileNotFoundError:
        logger.error(f"Dataset not found at {path}. Please ensure the file exists.")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Dataset at {path} is empty.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading data: {e}")
        raise

def build_match_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate the ball-by-ball frame down to one row per match."""
    match_cols = [
        "match_id", "date", "season", "event", "venue", "city",
        "team1", "team2", "toss_winner", "toss_decision", "winner",
        "win_by_runs", "win_by_wickets", "player_of_match",
    ]
    # Filter available cols to avoid KeyErrors on optional columns
    match_cols = [col for col in match_cols if col in df.columns]
    
    snap = df[match_cols].drop_duplicates(subset="match_id").copy().reset_index(drop=True)
    
    if "toss_winner" in snap.columns and "winner" in snap.columns:
        snap["toss_win_match_win"] = snap["toss_winner"] == snap["winner"]
    else:
        snap["toss_win_match_win"] = False
        
    return snap
