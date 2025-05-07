# Student Performance Analysis Dashboard

This interactive dashboard, built with Streamlit, provides educators with tools to analyze and understand student exam performance based on a variety of influencing factors. Users can gain an overall situational awareness, explore potential causal relationships, and conduct deep dives into individual student data for targeted interventions.

## Features

*   **Overall Performance Overview:**
    *   Key Performance Indicators (KPIs) for a quick snapshot of class performance (e.g., average score, median score, percentage of students meeting a threshold).
    *   Distribution of exam scores to understand the overall spread and identify common score ranges.
    *   Comparison of average scores across different school types.
*   **Influencing Factor Exploration:**
    *   Interactive scatter plots to visualize the relationship between numerical factors (e.g., Hours Studied, Previous Scores, Attendance) and exam scores.
    *   Ability to color-code scatter plot points by a selected categorical factor for deeper insights.
    *   Box plots to compare exam score distributions across different levels of categorical factors (e.g., Parental Involvement, Motivation Level).
    *   A correlation heatmap to quickly identify linear relationships between numerical variables.
*   **Student Deep Dive & Comparison:**
    *   Interactive filters to narrow down student lists based on exam score ranges and various categorical attributes.
    *   A table displaying key information for filtered students.
    *   A comparative bar chart showing an individual selected student's performance on key metrics against the class average.

## Project Structure

Interactive App/
├── student_performance_dashboard.py # Main Streamlit application script
├── StudentPerformanceFactors.csv # Dataset
├── requirements.txt # Python dependencies
├── .gitignore # Specifies intentionally untracked files that Git should ignore
└── pages/ # Subdirectory for individual app pages
├── 01_Overall_Performance.py
├── 02_Factor_Exploration.py
└── 03_Student_Deep_Dive.py


## Running the Application

### Prerequisites

*   Python 3.8+
*   Git (for cloning)

### Local Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit app:**
    ```bash
    streamlit run student_performance_dashboard.py
    ```
    The application will open in your default web browser.

## Deployed Application

https://nick-student-performance-dashboard.streamlit.app/Student_Deep_Dive

## Dataset

The dashboard utilizes the "Student Performance Factors" dataset, which includes information on study habits, attendance, parental involvement, and other aspects influencing academic success.
*   **Source:** https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
*   **File:** `StudentPerformanceFactors.csv`

## Design Rationale

The design of this dashboard prioritizes clarity, ease of use, and actionable insights for educators. Key design decisions are based on established data visualization principles and cognitive factors to support effective decision-making. For a detailed explanation, please refer to the accompanying design rationale document.
