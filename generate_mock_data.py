import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(filepath="c:/Users/ADMIN/OneDrive/Desktop/ipl_analytics_project/ipl_analytics/data/ipl_ball_by_ball.csv"):
    np.random.seed(42)
    
    num_matches = 50
    balls_per_match = 240
    total_balls = num_matches * balls_per_match
    
    match_ids = np.repeat(np.arange(1000, 1000 + num_matches), balls_per_match)
    
    # Generate seasons (2008 to 2024)
    seasons = np.random.choice([str(y) for y in range(2008, 2025)], num_matches)
    season_col = np.repeat(seasons, balls_per_match)
    
    # Innings, over, ball
    innings = np.tile(np.repeat([1, 2], 120), num_matches)
    overs = np.tile(np.repeat(np.arange(0, 20), 6), num_matches * 2)
    balls = np.tile(np.arange(1, 7), num_matches * 40)
    
    # Runs
    runs_batter = np.random.choice([0, 1, 2, 3, 4, 6], size=total_balls, p=[0.4, 0.3, 0.05, 0.01, 0.14, 0.1])
    extras_wides = np.random.choice([0, 1], size=total_balls, p=[0.95, 0.05])
    extras_noballs = np.random.choice([0, 1], size=total_balls, p=[0.99, 0.01])
    runs_extras = extras_wides + extras_noballs
    runs_total = runs_batter + runs_extras
    
    # Wickets
    is_wicket = np.random.choice([True, False], size=total_balls, p=[0.05, 0.95])
    wicket_choices = np.random.choice(['caught', 'bowled', 'run out', 'lbw'], size=total_balls)
    wicket_kind = np.where(is_wicket, wicket_choices, "").astype(object)
    wicket_kind[~is_wicket] = np.nan
    
    # Teams & players
    teams = ['MI', 'CSK', 'RCB', 'KKR', 'DC', 'PBKS', 'RR', 'SRH']
    match_team1 = np.repeat(np.random.choice(teams, num_matches), balls_per_match)
    match_team2 = np.repeat(np.random.choice(teams, num_matches), balls_per_match)
    
    # Fix same teams
    for i in range(num_matches):
        if match_team1[i*balls_per_match] == match_team2[i*balls_per_match]:
            match_team2[i*balls_per_match:(i+1)*balls_per_match] = 'GT'
            
    batting_team = np.where(innings == 1, match_team1, match_team2)
    bowling_team = np.where(innings == 1, match_team2, match_team1)
    
    batters = [f'Batter_{i}' for i in range(1, 101)]
    bowlers = [f'Bowler_{i}' for i in range(1, 101)]
    
    batter = np.random.choice(batters, total_balls)
    bowler = np.random.choice(bowlers, total_balls)
    
    # Match metadata
    date = np.repeat([(datetime(2020, 1, 1) + timedelta(days=int(i))).strftime('%Y-%m-%d') for i in range(num_matches)], balls_per_match)
    toss_winner = np.where(np.random.rand(total_balls) > 0.5, match_team1, match_team2)
    toss_decision = np.repeat(np.random.choice(['bat', 'field'], num_matches), balls_per_match)
    
    # Simple winner logic based on runs
    winner = np.where(np.random.rand(total_balls) > 0.5, match_team1, match_team2)
    
    df = pd.DataFrame({
        'match_id': match_ids,
        'season': season_col,
        'innings': innings,
        'over': overs,
        'ball': balls,
        'runs_batter': runs_batter,
        'runs_extras': runs_extras,
        'runs_total': runs_total,
        'extras_wides': extras_wides,
        'extras_noballs': extras_noballs,
        'is_wicket': is_wicket,
        'wicket_kind': wicket_kind,
        'date': date,
        'event': 'IPL',
        'venue': 'Mock Stadium',
        'city': 'Mock City',
        'team1': match_team1,
        'team2': match_team2,
        'toss_winner': toss_winner,
        'toss_decision': toss_decision,
        'winner': winner,
        'win_by_runs': np.random.randint(1, 50, total_balls),
        'win_by_wickets': np.random.randint(1, 10, total_balls),
        'player_of_match': np.random.choice(batters, total_balls),
        'batting_team': batting_team,
        'bowling_team': bowling_team,
        'batter': batter,
        'bowler': bowler
    })
    
    df.to_csv(filepath, index=False)
    print(f"Mock data created at {filepath} with {len(df)} rows.")

if __name__ == "__main__":
    generate_mock_data()
