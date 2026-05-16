# IPL Analytics Streamlit Dashboard

This is an interactive, modern sports analytics dashboard built using Streamlit and Plotly. It allows users to explore IPL match data, toss advantages, match phases, and top performers dynamically.

## Project Structure
- `app.py`: Main Streamlit application.
- `src/`: Modular code containing data loading, caching, analytical functions, and visualization configurations.
- `data/`: Contains the `ipl_ball_by_ball.csv` dataset.
- `requirements.txt`: Python dependencies required to run the project.

## Deployment Instructions

### Local Deployment
To run this dashboard on your local machine, follow these steps:

1. **Activate your virtual environment** (if not already active):
   ```bash
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

4. **Access the Dashboard**:
   Open the Local URL provided in your terminal (typically `http://localhost:8501`) in your web browser.

### Cloud Deployment (Streamlit Community Cloud)
You can easily host this dashboard for free using Streamlit Community Cloud:

1. Push this entire project repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click "New app".
4. Select your repository, branch, and specify the main file path as `app.py`.
5. Click "Deploy". Streamlit will automatically install dependencies from `requirements.txt` and host your dashboard!

## Features
- **Caching**: The heavy dataset is cached (`@st.cache_data`) for ultra-fast performance across pages.
- **Interactive UI**: Utilizing Sidebar navigation and professional KPI cards.
- **Dynamic Filtering**: Analyze the entire dataset or slice it by specific Seasons and Teams.
- **Searchable Player Data**: Quickly find statistics for specific batters or bowlers.
