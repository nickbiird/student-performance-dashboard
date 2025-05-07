# pages/02_Factor_Exploration.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Data Loading and Caching ---
@st.cache_data
def load_data(file_path="StudentPerformanceFactors.csv"):
    df = pd.read_csv(file_path)
    ordinal_cols_mapping = {
        'Parental_Involvement': ['Low', 'Medium', 'High'],
        'Access_to_Resources': ['Low', 'Medium', 'High'],
        'Motivation_Level': ['Low', 'Medium', 'High'],
        'Family_Income': ['Low', 'Medium', 'High'],
        'Teacher_Quality': ['Low', 'Medium', 'High'],
        'Parental_Education_Level': ['High School', 'College', 'Postgraduate'],
        'Peer_Influence': ['Negative', 'Neutral', 'Positive']
    }
    # Store the mapping on the function object so it can be accessed after loading
    # This is a way to pass 'configuration' out of the cached function
    load_data.ordinal_cols_mapping = ordinal_cols_mapping

    for col, order in ordinal_cols_mapping.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=order, ordered=True)
    if 'Student_ID' not in df.columns:
        df = df.reset_index().rename(columns={'index': 'Student_ID'})
    return df

# --- Page Content ---
st.title("Explore Factors Influencing Performance")
st.markdown("""
Investigate how different student-related factors correlate with exam scores.
*   **Purpose:** Causal Investigation & Pattern Recognition - "What factors seem to influence scores?"
*   **Design Focus:** Interactive exploration of numerical and categorical factors.
""")

try:
    df_students = load_data()
except FileNotFoundError:
    st.error("Error: 'StudentPerformanceFactors.csv' not found. Please make sure the file is in the root directory of the app.")
    st.stop()


st.subheader("Numerical Factors vs. Exam Score")
numerical_factors_options = ['Hours_Studied', 'Previous_Scores', 'Attendance', 'Sleep_Hours', 'Physical_Activity', 'Tutoring_Sessions']
valid_numerical_factors = [f for f in numerical_factors_options if f in df_students.columns and pd.api.types.is_numeric_dtype(df_students[f])]

if not valid_numerical_factors:
    st.warning("No valid numerical factors found for scatter plot.")
else:
    selected_numerical_factor = st.selectbox("Select Numerical Factor:", valid_numerical_factors)

    categorical_cols_for_hue = [col for col in df_students.columns if (df_students[col].dtype.name == 'category' or df_students[col].nunique() < 6) and col != selected_numerical_factor]
    hue_options = ['None'] + categorical_cols_for_hue
    selected_hue = st.selectbox("Color points by (categorical):", hue_options, index=0)

    fig_scatter, ax_scatter = plt.subplots()
    plot_hue_data = df_students[selected_hue] if selected_hue != 'None' else None
    sns.scatterplot(x=df_students[selected_numerical_factor], y=df_students['Exam_Score'], hue=plot_hue_data, ax=ax_scatter, alpha=0.6, palette="viridis" if selected_hue != 'None' else None)
    title_suffix = f' (Colored by {selected_hue})' if selected_hue != 'None' else ''
    ax_scatter.set_title(f'{selected_numerical_factor} vs. Exam Score{title_suffix}')
    ax_scatter.set_xlabel(selected_numerical_factor)
    ax_scatter.set_ylabel('Exam Score')
    if selected_hue != 'None':
         ax_scatter.legend(title=selected_hue, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig_scatter)


st.markdown("---")
st.subheader("Categorical Factors vs. Exam Score")

# --- START OF CORRECTION ---
# Access the mapping stored on the function object AFTER load_data has been called
# and df_students is populated.
ordinal_mapping_from_load = getattr(load_data, 'ordinal_cols_mapping', {}) # Get it if set
if not ordinal_mapping_from_load: # Fallback if not set (e.g., cache miss or first run weirdness)
    ordinal_mapping_from_load = { # Redefine as a last resort
        'Parental_Involvement': ['Low', 'Medium', 'High'],
        'Access_to_Resources': ['Low', 'Medium', 'High'],
        'Motivation_Level': ['Low', 'Medium', 'High'],
        'Family_Income': ['Low', 'Medium', 'High'],
        'Teacher_Quality': ['Low', 'Medium', 'High'],
        'Parental_Education_Level': ['High School', 'College', 'Postgraduate'],
        'Peer_Influence': ['Negative', 'Neutral', 'Positive']
    }

categorical_factors_options_list = list(ordinal_mapping_from_load.keys()) + \
                                   ['School_Type', 'Gender', 'Extracurricular_Activities', 'Internet_Access', 'Learning_Disabilities']
# --- END OF CORRECTION ---

valid_categorical_factors = [f for f in categorical_factors_options_list if f in df_students.columns]


if not valid_categorical_factors:
    st.warning("No valid categorical factors found for box plot.")
else:
    selected_categorical_factor = st.selectbox("Select Categorical Factor:", valid_categorical_factors)
    fig_box, ax_box = plt.subplots(figsize=(10, 6))
    hue_for_boxplot = selected_categorical_factor if df_students[selected_categorical_factor].nunique() <= 10 else None
    sns.boxplot(x=df_students[selected_categorical_factor], y=df_students['Exam_Score'], ax=ax_box, palette="Set2", hue=df_students[hue_for_boxplot] if hue_for_boxplot else None, legend=False if hue_for_boxplot else None)
    ax_box.set_title(f'Exam Score Distribution by {selected_categorical_factor}')
    ax_box.set_xlabel(selected_categorical_factor)
    ax_box.set_ylabel('Exam Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_box)

st.markdown("---")
st.subheader("Correlation Heatmap of Numerical Variables")
numerical_cols_for_corr = ['Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Scores', 'Tutoring_Sessions', 'Physical_Activity', 'Exam_Score']
valid_cols_for_corr = [col for col in numerical_cols_for_corr if col in df_students.columns and pd.api.types.is_numeric_dtype(df_students[col])]

if len(valid_cols_for_corr) > 1:
    correlation_matrix = df_students[valid_cols_for_corr].corr()
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax_heatmap, vmin=-1, vmax=1)
    ax_heatmap.set_title('Correlation Matrix of Numerical Factors and Exam Score')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig_heatmap)
else:
    st.warning("Not enough numerical columns found/valid for a correlation heatmap.")