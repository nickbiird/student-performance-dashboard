# student_performance_dashboard.py

import streamlit as st

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Student Performance Dashboard",
    page_icon="📊" # Optional: Add an icon
)

st.title("📊 Student Performance Analysis Dashboard")

st.markdown("""
Welcome to the Student Performance Analysis Dashboard.
This application is designed to help educators understand student performance
by exploring various influencing factors and diving deep into individual student data.

**Navigate through the pages using the sidebar on the left to:**
*   Get an **Overall Performance** overview.
*   **Explore Influencing Factors** that correlate with exam scores.
*   Conduct a **Student Deep Dive & Comparison** for targeted insights.

This dashboard leverages data visualization principles and cognitive factors
to provide actionable insights for decision-making.
""")

st.sidebar.success("Select a page above to begin.")

# Note: Streamlit automatically discovers and lists .py files in the 'pages'
# directory in the sidebar for navigation. You don't need to manually create
# the navigation radio buttons here if you use the 'pages' folder structure.