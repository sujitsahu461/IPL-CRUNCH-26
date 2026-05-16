import logging
from config import DATA_PATH, CHARTS_DIR, TABLES_DIR
from data_loader import load_and_clean, build_match_snapshot
from analysis import analyse_toss, analyse_phases, top_batters, top_bowlers, generate_insights
from visualizations import plot_toss_analysis, plot_phase_analysis, plot_top_performers, plot_season_scoring

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    setup_logging()
    logger = logging.getLogger("IPL_Analytics")
    
    logger.info("Starting IPL Analytics Pipeline...")
    
    # 1. Load Data
    try:
        df = load_and_clean(DATA_PATH)
        matches = build_match_snapshot(df)
    except Exception as e:
        logger.error("Pipeline failed during data loading. Exiting.")
        return

    # 2. Analysis
    logger.info("Performing analysis...")
    toss_data = analyse_toss(matches)
    phase_avg = analyse_phases(df, matches)
    batters = top_batters(df)
    bowlers = top_bowlers(df)
    
    # 3. Export Tables
    logger.info("Exporting tables...")
    try:
        phase_avg.to_csv(TABLES_DIR / "phase_analysis.csv", index=False)
        batters.to_csv(TABLES_DIR / "top_batters.csv", index=False)
        bowlers.to_csv(TABLES_DIR / "top_bowlers.csv", index=False)
        if not toss_data["by_decision"].empty:
            toss_data["by_decision"].to_csv(TABLES_DIR / "toss_by_decision.csv", index=False)
        if not toss_data["season_trend"].empty:
            toss_data["season_trend"].to_csv(TABLES_DIR / "toss_season_trend.csv", index=False)
    except Exception as e:
        logger.error(f"Failed to export tables: {e}")

    # 4. Visualizations
    logger.info("Generating visualizations...")
    try:
        plot_toss_analysis(toss_data, CHARTS_DIR / "01_toss_analysis.png")
        plot_phase_analysis(phase_avg, matches["match_id"].nunique(), CHARTS_DIR / "02_phase_analysis.png")
        plot_top_performers(batters, bowlers, CHARTS_DIR / "03_top_performers.png")
        plot_season_scoring(df, CHARTS_DIR / "04_season_scoring_trend.png")
    except Exception as e:
        logger.error(f"Failed to generate visualizations: {e}")

    # 5. Insights
    logger.info("Generating insights...")
    insights = generate_insights(toss_data, phase_avg, batters, bowlers, df, matches)
    print("\n" + "="*70)
    print("  KEY INSIGHTS  ")
    print("="*70)
    for ins in insights:
        print(f"\n{ins}")
    print("\n" + "="*70)
    
    logger.info("IPL Analytics Pipeline completed successfully!")

if __name__ == "__main__":
    main()
