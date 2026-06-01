import streamlit as st
import pandas as pd
import plotly.express as px


def render_dashboard(df, metrics, model, prediction, get_ai_advice, model_score):

    # -------------------- TITLE --------------------
    st.markdown("# AI Tool Productivity Analysis Dashboard")

    # -------------------- KPI CARDS --------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📊 Productivity Score", f"{metrics['productivity_score']}/100")
    col2.metric("⏱ Time Saved", f"{round(metrics['time_saved'], 2)} hrs")
    col3.metric("✅ Tasks Completed", metrics['tasks_completed'])
    col4.metric("📉 Error Reduction", f"{round(metrics['error_reduction'], 2)}%")
    col5.metric("🤖 AI Usage Rate", f"{round(metrics['ai_usage_rate'], 2)}%")

    st.divider()

    # -------------------- CHARTS (UPGRADED 🔥) --------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Productivity: With vs Without AI")

        grouped = df.groupby("task")[["time_with_ai", "time_without_ai"]].mean().reset_index()

        fig = px.bar(
            grouped,
            x="task",
            y=["time_with_ai", "time_without_ai"],
            barmode="group"
        )

        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown("### AI Tool Usage Distribution")

        tool_counts = df["ai_tool"].value_counts().reset_index()
        tool_counts.columns = ["ai_tool", "count"]

        fig = px.pie(tool_counts, names="ai_tool", values="count")
        st.plotly_chart(fig, width="stretch")

    st.divider()

    # -------------------- PRODUCTIVITY TREND --------------------
    st.markdown("### 📈 Productivity Trend Over Time")

    df["date"] = pd.to_datetime(df["date"])
    trend = df.groupby("date")[["time_with_ai", "time_without_ai"]].mean().reset_index()

    fig = px.line(trend, x="date", y=["time_with_ai", "time_without_ai"])
    st.plotly_chart(fig, width="stretch")

    st.divider()

    # -------------------- INSIGHTS --------------------
    st.markdown("### 📊 Key Insights")

    try:
        best_tool = df.groupby("ai_tool")["time_with_ai"].mean().idxmin()
        st.info(f"🚀 Most efficient AI tool: {best_tool}")

        df["time_saved"] = df["time_without_ai"] - df["time_with_ai"]
        best_task = df.loc[df["time_saved"].idxmax()]

        st.info(f"⏱ Highest time saved in: {best_task['task']} ({round(best_task['time_saved'],2)} hrs)")
    except:
        st.warning("Not enough data to generate insights")

    st.divider()

    # -------------------- ROI / IMPACT --------------------
    st.markdown("### 💰 Business Impact")

    avg_hourly_rate = 500
    cost_savings = metrics["time_saved"] * avg_hourly_rate

    efficiency = df["time_without_ai"].sum() / df["time_with_ai"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💸 Cost Savings", f"₹{round(cost_savings, 2)}")
    col2.metric("⚡ Efficiency Gain", f"{round(metrics['error_reduction'], 2)}%")
    col3.metric("📈 Predicted Score", f"{round(prediction, 2)}")
    col4.metric("🧠 Model Accuracy (R²)", round(model_score, 2))  # NEW

    st.metric("⚡ Efficiency Boost", f"{round(efficiency, 2)}x faster with AI")

    st.divider()

    # -------------------- INTERACTIVE PREDICTION (FIXED ✅) --------------------
    st.markdown("### 🔮 Try Your Own Productivity Prediction")

    ai_usage = st.selectbox("AI Usage Level", [1, 2, 3])
    task_complexity = st.selectbox("Task Complexity", [1, 2, 3])
    time_with_ai = st.slider("Time With AI (hrs)", 1.0, 10.0, 3.0)

    try:
        input_df = pd.DataFrame([{
            "ai_usage": ai_usage,
            "task_complexity": task_complexity,
            "time_with_ai": time_with_ai
        }])

        new_prediction = model.predict(input_df)[0]

        st.success(f"Predicted Productivity Score: {round(new_prediction, 2)}")
    except:
        st.warning("Prediction model not ready")

    st.divider()

    # -------------------- AI ADVISOR --------------------
    st.markdown("### 🤖 AI Productivity Advisor")

    user_input = st.text_area("Describe your workflow:")

    if st.button("Get AI Suggestions"):
        if user_input.strip() == "":
            st.warning("Please enter your workflow.")
        else:
            with st.spinner("Analyzing with AI..."):
                advice = get_ai_advice(user_input)
            st.success(advice)

    st.divider()

    # -------------------- DOWNLOAD --------------------
    st.download_button(
        "📥 Download Dataset",
        df.to_csv(index=False),
        "ai_productivity_data.csv"
    )

    # -------------------- RAW DATA --------------------
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df)