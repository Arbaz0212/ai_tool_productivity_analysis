import streamlit as st

from src.data_processing import load_data, compute_metrics
from src.model import train_model, predict_productivity
from src.ollama_client import get_ai_advice
from components.dashboard import render_dashboard

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Productivity Dashboard",
    layout="wide"
)

# -------------------- CUSTOM STYLING --------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

[data-testid="stMetric"] {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
}

h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD DATA --------------------
try:
    df = load_data("data/dataset.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Safety check
if df.empty:
    st.warning("Dataset is empty. Please check your CSV file.")
    st.stop()

# -------------------- SIDEBAR --------------------
st.sidebar.title("Filters")

# Handle missing column safely
if "ai_tool" not in df.columns:
    st.error("Column 'ai_tool' not found in dataset.")
    st.stop()

tool_options = ["All"] + sorted(df["ai_tool"].dropna().unique())

selected_tool = st.sidebar.selectbox(
    "AI Tool",
    tool_options
)

# -------------------- APPLY FILTER --------------------
filtered_df = df.copy()

if selected_tool != "All":
    filtered_df = filtered_df[filtered_df["ai_tool"] == selected_tool]

# Safety check after filtering
if filtered_df.empty:
    st.warning("No data available for selected filter.")
    st.stop()

# -------------------- METRICS --------------------
metrics = compute_metrics(filtered_df)

# -------------------- MODEL --------------------
try:
    model, model_score = train_model(filtered_df)   # ✅ UPDATED

    prediction = predict_productivity(
        model,
        ai_usage=2,
        task_complexity=2,
        time_with_ai=3
    )
except Exception as e:
    st.error(f"Model error: {e}")
    st.stop()

# -------------------- RENDER DASHBOARD --------------------
render_dashboard(
    df=filtered_df,
    metrics=metrics,
    model=model,
    prediction=prediction,
    get_ai_advice=get_ai_advice,
    model_score=model_score   # ✅ NEW
)