import streamlit as st

def render_charts(df):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Productivity: With vs Without AI")
        st.bar_chart(df.set_index("task")[["time_without_ai", "time_with_ai"]])

    with col2:
        st.markdown("### AI Tool Usage Distribution")
        st.bar_chart(df["ai_tool"].value_counts())