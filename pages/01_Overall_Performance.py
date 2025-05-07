# pages/01_Overall_Performance.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Data Loading and Caching ---
@st.cache_data # Caches the data to avoid reloading on every interaction
def load_data(file_path="StudentPerformanceFactors.csv"): # Default path
    df = pd.read_csv(file_path)
    # Define order for ordinal columns for consistent plotting
    ordinal_cols_mapping = {
        'Parental_Involvement': ['Low', 'Medium', 'High'],
        'Access_to_Resources': ['Low', 'Medium', 'High'],
        'Motivation_Level': ['Low', 'Medium', 'High'],
        'Family_Income': ['Low', 'Medium', 'High'],
        'Teacher_Quality': ['Low', 'Medium', 'High'],
        'Parental_Education_Level': ['High School', 'College', 'Postgraduate'],
        'Peer_Influence': ['Negative', 'Neutral', 'Positive']
    }
    for col, order in ordinal_cols_mapping.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=order, ordered=True)

    # Add a unique Student_ID if not present
    if 'Student_ID' not in df.columns:
        df = df.reset_index().rename(columns={'index': 'Student_ID'})
    return df

# --- Page Content ---
st.title("Overall Student Performance Dashboard")
st.markdown("""
This page provides a high-level overview of student exam performance.
*   **Purpose:** Situational Awareness - "How are students doing overall?"
*   **Design Focus:** Clear KPIs, appropriate chart types for distribution and comparison.
""")

# Load data
try:
    df_students = load_data() # Assumes StudentPerformanceFactors.csv is in the root directory
except FileNotFoundError:
    st.error("Error: 'StudentPerformanceFactors.csv' not found. Please make sure the file is in the root directory of the app.")
    st.stop()


# Row for KPIs
st.subheader("Key Performance Indicators")
avg_score = df_students['Exam_Score'].mean()
median_score = df_students['Exam_Score'].median()
num_students = len(df_students)
pass_threshold = 70 # Example threshold for "passing"
students_above_threshold = df_students[df_students['Exam_Score'] >= pass_threshold].shape[0]
percent_above_threshold = (students_above_threshold / num_students) * 100 if num_students > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", f"{num_students}")
col2.metric("Average Exam Score", f"{avg_score:.2f}")
col3.metric("Median Exam Score", f"{median_score:.2f}")
col4.metric(f"% Scores >= {pass_threshold}", f"{percent_above_threshold:.2f}%")
# JUSTIFICATION POINT 1 (From previous list)

st.markdown("---")
col_dist, col_school = st.columns(2)

with col_dist:
    st.subheader("Exam Score Distribution")
    fig_hist, ax_hist = plt.subplots()
    sns.histplot(df_students['Exam_Score'], kde=True, ax=ax_hist, bins=20, color="skyblue")
    ax_hist.set_title('Distribution of Exam Scores')
    ax_hist.set_xlabel('Exam Score')
    ax_hist.set_ylabel('Number of Students')
    st.pyplot(fig_hist)
    # JUSTIFICATION POINT 2 (From previous list)

with col_school:
    st.subheader("Average Scores by School Type")
    if 'School_Type' in df_students.columns:
        avg_score_school_type = df_students.groupby('School_Type', observed=False)['Exam_Score'].mean().reset_index()
        fig_bar, ax_bar = plt.subplots()
        sns.barplot(x='School_Type', y='Exam_Score', data=avg_score_school_type, ax=ax_bar, palette="pastel", hue='School_Type', legend=False)
        ax_bar.set_title('Average Exam Score by School Type')
        ax_bar.set_xlabel('School Type')
        ax_bar.set_ylabel('Average Exam Score')
        st.pyplot(fig_bar)
        # JUSTIFICATION POINT (Can be similar to point 2, focusing on categorical comparison)
    else:
        st.warning("Column 'School_Type' not found in the data.")