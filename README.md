<div align="center">
  <h1>🏏 IPL Crunch '26 Analytics Dashboard</h1>
  <p><strong>A Modern, Interactive Sports Analytics Application</strong></p>
  
  <a href="https://ipl-crunch-26-ntrgwckdmwd5q8gw6gpcry.streamlit.app/">
    <img src="https://img.shields.io/badge/🔴_Live_Demo-View_Dashboard-FF4B4B?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://github.com/sujitsahu461/IPL-CRUNCH-26/stargazers">
    <img src="https://img.shields.io/github/stars/sujitsahu461/IPL-CRUNCH-26?style=for-the-badge&color=1DB954" alt="Stars">
  </a>
</div>

<br/>

## 📖 Overview

The **IPL Crunch '26 Analytics Dashboard** is a comprehensive, production-ready data science web application that analyzes over 289,000+ ball-by-ball deliveries from the Indian Premier League. Built with a focus on speed, modularity, and modern UI/UX design, it provides deep statistical insights into match phases, toss advantages, scoring trends, and top player performances.

**🔗 [View the Live App Here](https://ipl-crunch-26-ntrgwckdmwd5q8gw6gpcry.streamlit.app/)**

## ✨ Features

- **⚡ Blazing Fast Performance:** Heavy computational tasks and dataset loading are wrapped in `@st.cache_data` for instantaneous chart rendering and tab switching.
- **🎨 Interactive Visualizations:** Beautiful, responsive, dark-mode adapted charts built exclusively using **Plotly**.
- **🎯 Dynamic Filtering:** Instantly slice the entire 1.6M+ row dataset by specific **Seasons** or **Teams** using the sidebar.
- **🔍 Player Search Engine:** Instantly search for any historical IPL batter or bowler to see their all-time rankings, total runs, boundaries, wickets, and economy rates.
- **💡 Automated AI Insights:** A dedicated page that mathematically derives and explains key statistical advantages based on the currently applied filters.

## 🛠️ Technology Stack

- **Frontend / Deployment:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Interactive Plotting:** [Plotly Express & Graph Objects](https://plotly.com/python/)
- **Version Control:** Git & GitHub

## 📂 Project Structure

```bash
IPL-CRUNCH-26/
│
├── app.py                     # Main Streamlit Application Entry Point
├── requirements.txt           # Python Dependencies
├── README.md                  # Project Documentation
│
├── data/
│   └── ipl_ball_by_ball.csv   # Primary Dataset (289,000+ Rows)
│
└── src/                       # Modular Analytical Engine
    ├── config.py              # UI/UX Constants and Styling
    ├── data_loader.py         # Data Validation & Caching Logic
    ├── analysis.py            # Mathematical Aggregations & KPIs
    └── charts.py              # Plotly Visualization Functions
```

## 🚀 Running Locally

Want to run this project on your own machine? It takes less than 2 minutes!

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sujitsahu461/IPL-CRUNCH-26.git
   cd IPL-CRUNCH-26
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/sujitsahu461/IPL-CRUNCH-26/issues).
