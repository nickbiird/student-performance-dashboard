# pages/03_Student_Deep_Dive.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Data Loading and Caching ---
@st.cache_data
def load_data(file_path="StudentPerformanceFactors.csv"):
    df = pd.read_csv(file_path)
    ordinal_cols_mapping = { # Store this for later use if needed for filter options
        'Parental_Involvement': ['Low', 'Medium', 'High'],
        'Access_to_Resources': ['Low', 'Medium', 'High'],
        'Motivation_Level': ['Low', 'Medium', 'High'],
        'Family_Income': ['Low', 'Medium', 'High'],
        'Teacher_Quality': ['Low', 'Medium', 'High'],
        'Parental_Education_Level': ['High School', 'College', 'Postgraduate'],
        'Peer_Influence': ['Negative', 'Neutral', 'Positive']
    }
    load_data.ordinal_cols_mapping = ordinal_cols_mapping # Make it accessible

    for col, order in ordinal_cols_mapping.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=order, ordered=True)
    if 'Student_ID' not in df.columns:
        df = df.reset_index().rename(columns={'index': 'Student_ID'})
    return df

# --- Page Content ---
st.title("Student Deep Dive & Comparison")
st.markdown("""
Filter students based on performance and other criteria. Optionally, compare an individual student to class averages.
*   **Purpose:** Exception Identification & Comparative Analysis - "Which students need attention? How do they compare?"
*   **Design Focus:** Interactive filtering and clear comparative visualization.
""")

try:
    df_students = load_data()
except FileNotFoundError:
    st.error("Error: 'StudentPerformanceFactors.csv' not found. Please make sure the file is in the root directory of the app.")
    st.stop()

st.sidebar.header("Student Filters") # Filters will appear on the sidebar for this page

# Ensure Exam_Score is numeric for min/max
if pd.api.types.is_numeric_dtype(df_students['Exam_Score']):
    score_min_val = int(df_students['Exam_Score'].min())
    score_max_val = int(df_students['Exam_Score'].max())
    default_score_range = (score_min_val, score_max_val)
else: # Fallback
    score_min_val, score_max_val, default_score_range = 0, 100, (0, 100)
    st.sidebar.warning("Exam_Score column is not numeric. Using default range 0-100.")

score_range_selected = st.sidebar.slider(
    "Filter by Exam Score Range:",
    min_value=score_min_val,
    max_value=score_max_val,
    value=default_score_range
)

# Categorical filter options
# Access the mapping stored on the function object or redefine
ordinal_mapping = getattr(load_data, 'ordinal_cols_mapping', {})
filter_options_cat = ['None'] + \
                     [col for col in ordinal_mapping.keys() if col in df_students.columns] + \
                     [col for col in ['Extracurricular_Activities', 'Internet_Access', 'Learning_Disabilities', 'School_Type', 'Gender'] if col in df_students.columns]

filter_cat1_col = st.sidebar.selectbox("Categorical Filter 1:", filter_options_cat, index=0, key="cat_filter1_col")
filter_cat1_val_selected = None
if filter_cat1_col != 'None':
    unique_vals1 = ['All'] + sorted(list(df_students[filter_cat1_col].astype(str).unique())) # astype(str) to handle mixed types if any
    filter_cat1_val_selected = st.sidebar.selectbox(f"Select Value for {filter_cat1_col}:", unique_vals1, index=0, key="cat_filter1_val")

# Apply Filters
filtered_df = df_students[
    (df_students['Exam_Score'] >= score_range_selected[0]) & (df_students['Exam_Score'] <= score_range_selected[1])
]
if filter_cat1_col != 'None' and filter_cat1_val_selected != 'All':
    filtered_df = filtered_df[filtered_df[filter_cat1_col].astype(str) == filter_cat1_val_selected]


st.subheader(f"Filtered Student List ({len(filtered_df)} students)")
if not filtered_df.empty:
    display_cols = ['Student_ID', 'Hours_Studied', 'Attendance', 'Previous_Scores', 'Motivation_Level', 'Exam_Score']
    valid_display_cols = [col for col in display_cols if col in filtered_df.columns]
    st.dataframe(filtered_df[valid_display_cols].head(20), use_container_width=True)
    # JUSTIFICATION POINT 6 (From previous list)
else:
    st.warning("No students match the current filter criteria.")

st.markdown("---")
st.subheader("Individual Student Comparison")

# Select student from filtered list or all
student_ids_for_selection = []
if not filtered_df.empty:
    use_filtered_list = st.checkbox("Select student from filtered list above?", value=True)
    if use_filtered_list:
        student_ids_for_selection = filtered_df['Student_ID'].tolist()
    else:
        student_ids_for_selection = df_students['Student_ID'].tolist()
else:
    st.info("Filtered list is empty. Showing all students for selection.")
    student_ids_for_selection = df_students['Student_ID'].tolist()


if not student_ids_for_selection:
    st.warning("No students available for selection.")
    selected_student_id = None
else:
    selected_student_id = st.selectbox("Select Student ID to Compare:", student_ids_for_selection)

if selected_student_id is not None:
    student_data = df_students[df_students['Student_ID'] == selected_student_id].iloc[0]
    comparison_metrics_options = ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Exam_Score', 'Tutoring_Sessions', 'Sleep_Hours']
    valid_comparison_metrics = [m for m in comparison_metrics_options if m in df_students.columns and pd.api.types.is_numeric_dtype(df_students[m])]

    if valid_comparison_metrics:
        student_values = student_data[valid_comparison_metrics]
        class_averages = df_students[valid_comparison_metrics].mean()

        comp_data = pd.DataFrame({
            'Metric': valid_comparison_metrics,
            'Student': student_values.values,
            'Class Average': class_averages.values
        })
        comp_data_melted = comp_data.melt(id_vars='Metric', var_name='Group', value_name='Value') # Renamed 'Score' to 'Value' for generality

        fig_compare, ax_compare = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Metric', y='Value', hue='Group', data=comp_data_melted, ax=ax_compare, palette={"Student": "coral", "Class Average": "skyblue"})
        ax_compare.set_title(f'Comparison for Student ID: {selected_student_id}')
        ax_compare.set_ylabel('Value/Score')
        ax_compare.set_xlabel('Metric')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig_compare)
        # JUSTIFICATION POINT 7 (From previous list)
    else:
        st.warning("Not enough valid numeric metrics for comparison for the selected student.")