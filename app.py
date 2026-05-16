import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Ensure src modules can be imported
sys.path.append(str(Path(__file__).resolve().parent))

from src.config import DATA_PATH
from src.data_loader import load_and_clean, build_match_snapshot
from src.analysis import analyse_toss, analyse_phases, top_batters, top_bowlers, generate_insights
from src.charts import plot_toss_win_pct, plot_toss_season_trend, plot_phase_analysis, plot_top_batters, plot_top_bowlers, plot_season_scoring

# Streamlit Page Config
st.set_page_config(page_title="IPL Analytics Dashboard", page_icon="🏏", layout="wide")

# Custom CSS for modern UI
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #161B22;
    }
    .stMetric {
        background-color: #161B22;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #21262D;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading with Caching
@st.cache_data(show_spinner="Loading dataset...")
def get_data():
    try:
        df = load_and_clean(DATA_PATH)
        matches = build_match_snapshot(df)
        return df, matches
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df, matches = get_data()

# Sidebar Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/1200px-Indian_Premier_League_Official_Logo.svg.png", width=150)
st.sidebar.title("Filters")

# Season Filter
available_seasons = sorted(df["season"].dropna().unique().tolist())
selected_season = st.sidebar.selectbox("Select Season", ["All Time"] + available_seasons)

# Team Filter
available_teams = sorted(list(set(matches["team1"].dropna().unique()) | set(matches["team2"].dropna().unique())))
selected_team = st.sidebar.selectbox("Select Team", ["All Teams"] + available_teams)

# Filter Data Based on Selections
filtered_df = df.copy()
filtered_matches = matches.copy()

if selected_season != "All Time":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]
    filtered_matches = filtered_matches[filtered_matches["season"] == selected_season]

if selected_team != "All Teams":
    filtered_matches = filtered_matches[(filtered_matches["team1"] == selected_team) | (filtered_matches["team2"] == selected_team)]
    filtered_df = filtered_df[filtered_df["match_id"].isin(filtered_matches["match_id"])]
# Navigation
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Overview", "Toss Analysis", "Match Phase Analysis", "Top Batters", "Top Bowlers", "Insights Dashboard"])

if filtered_df.empty or filtered_matches.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

if page == "Overview":
    st.title("🏏 IPL Analytics Overview")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Matches", f"{filtered_matches['match_id'].nunique():,}")
    with col2:
        st.metric("Total Runs Scored", f"{filtered_df['runs_total'].sum():,}")
    with col3:
        st.metric("Total Wickets", f"{filtered_df['is_wicket'].sum():,}")
    with col4:
        st.metric("Total Sixes", f"{filtered_df[filtered_df['runs_batter'] == 6].shape[0]:,}")
        
    st.markdown("---")
    st.subheader("Historical Scoring Trend")
    # Using unfiltered data for the trend if "All Time" to show full history, else show filtered
    scoring_fig = plot_season_scoring(filtered_df)
    st.plotly_chart(scoring_fig, use_container_width=True)

elif page == "Toss Analysis":
    st.title("🎲 Toss Analysis")
    st.write("Does winning the toss actually provide a statistical advantage?")
    
    toss_data = analyse_toss(filtered_matches)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_toss_win_pct(toss_data), use_container_width=True)
    with col2:
        if selected_season == "All Time":
            st.plotly_chart(plot_toss_season_trend(toss_data), use_container_width=True)
        else:
            st.info("Season trend chart is only available when 'All Time' is selected.")

elif page == "Match Phase Analysis":
    st.title("⏱️ Match Phase Analysis")
    st.write("Comparing how match winners and losers perform across different phases of the game.")
    
    phase_avg = analyse_phases(filtered_df, filtered_matches)
    st.plotly_chart(plot_phase_analysis(phase_avg), use_container_width=True)
    
    st.dataframe(phase_avg, use_container_width=True)

elif page == "Top Batters":
    st.title("🏏 Top Batters")
    
    # Player Search
    search_query = st.text_input("Search for a Player", "")
    
    batters_df = top_batters(filtered_df, n=100) # Fetch more for searchability
    
    if search_query:
        batters_df = batters_df[batters_df["batter"].str.contains(search_query, case=False, na=False)]
    
    if batters_df.empty:
        st.warning("No batters found matching the search criteria.")
    else:
        st.plotly_chart(plot_top_batters(batters_df.head(10)), use_container_width=True)
        st.dataframe(batters_df, use_container_width=True)

elif page == "Top Bowlers":
    st.title("🎯 Top Bowlers")
    
    # Player Search
    search_query = st.text_input("Search for a Player", "")
    
    bowlers_df = top_bowlers(filtered_df, n=100)
    
    if search_query:
        bowlers_df = bowlers_df[bowlers_df["bowler"].str.contains(search_query, case=False, na=False)]
        
    if bowlers_df.empty:
        st.warning("No bowlers found matching the search criteria.")
    else:
        st.plotly_chart(plot_top_bowlers(bowlers_df.head(10)), use_container_width=True)
        st.dataframe(bowlers_df, use_container_width=True)

elif page == "Insights Dashboard":
    st.title("💡 Key Insights")
    st.write("Automated AI-driven insights based on the selected dataset filters.")
    
    toss_data = analyse_toss(filtered_matches)
    phase_avg = analyse_phases(filtered_df, filtered_matches)
    batters_df = top_batters(filtered_df, n=5)
    bowlers_df = top_bowlers(filtered_df, n=5)
    
    insights = generate_insights(toss_data, phase_avg, batters_df, bowlers_df, filtered_df, filtered_matches)
    
    for i, insight in enumerate(insights):
        st.info(insight)
