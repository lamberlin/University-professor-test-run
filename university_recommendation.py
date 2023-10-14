import streamlit as st
import pandas as pd

# Create a dictionary of universities and their attributes
universities = {
    "Yale": {
        "reputation": 4.5,
        "view_importance": 100,
        "ethnic_culture": 80,
        "academic_culture": 70,
        "study_difficulties": 40,
        "tech_strategy": 90,
    },
    "Berkeley": {
        "reputation": 4.2,
        "view_importance": 1,
        "ethnic_culture": 20,
        "academic_culture": 60,
        "study_difficulties": 90,
        "tech_strategy": 10,
    },
    "Columbia": {
        "reputation": 4.7,
        "view_importance": 70,
        "ethnic_culture": 80,
        "academic_culture": 70,
        "study_difficulties": 90,
        "tech_strategy": 80,
    },
}

# Create a DataFrame from the universities dictionary
df = pd.DataFrame(universities).T.reset_index()
df = df.rename(columns={"index": "University"})

# Create a function to recommend universities based on user preferences
def recommend_universities(user_preferences):
    # Calculate the total rank based on the preferences
    df["Total Rank"] = df[["reputation", "view_importance", "ethnic_culture", "academic_culture", "study_difficulties", "tech_strategy"]].sum(axis=1)
    
    # Sort the DataFrame by total rank in descending order
    filtered_df = df.sort_values(by="Total Rank", ascending=False)
    
    return filtered_df

# Streamlit app
st.title("University Recommendation System")

# User preferences
st.sidebar.header("User Preferences")
major = st.sidebar.selectbox("Select Major", ['architecture', 'biology', 'computer.science', 'electrical.engineering',
 'english.language.and.literature', 'linguistics', 'history',
 'development.studies', 'environmental.sciences', 'philosophy', 'physics',
 'psychology', 'political.science', 'sociology', 'accounting.and.finance',
 'communication_info', 'economics', 'archeology', 'education', 'arts',
 'medicine_health', 'chemical.engineering', 'theology',
 'agriculture.and.forestry', 'dentistry', 'geography', 'law',
 'mathematics_statistic', 'civil.engineering',
 'sports.sciences.and.management', 'mechanical.engineering'])
reputation = st.sidebar.slider("Reputation Preference (0-100)", 0, 100, 50, step=1)
view_importance = st.sidebar.slider("View Importance Preference (0-100)", 0, 100, 50, step=1)
ethnic_culture = st.sidebar.slider("Ethnic Culture Preference (0-100)", 0, 100, 50, step=1)
academic_culture = st.sidebar.slider("Academic Culture Preference (0-100)", 0, 100, 50, step=1)
study_difficulties = st.sidebar.slider("Study Difficulties Preference (0-100)", 0, 100, 50, step=1)
tech_strategy = st.sidebar.slider("Tech Strategy Preference (0-100)", 0, 100, 50, step=1)

user_preferences = {
    "major": major,
    "reputation": reputation,
    "view_importance": view_importance,
    "ethnic_culture": ethnic_culture,
    "academic_culture": academic_culture,
    "study_difficulties": study_difficulties,
    "tech_strategy": tech_strategy,
}

# Recommendation
st.header("University Recommendations")
recommended_universities = recommend_universities(user_preferences)
st.table(recommended_universities[["University", "Total Rank"]])

# Faculty information for each university
st.header("Faculty Information")
for university in recommended_universities["University"]:
    st.subheader(f"Faculty Information for {university}")
    st.write(f"Here are 10 faculties under {university}:")
    # Add faculty information here for each university
    for i in range(10):
        st.write(f"Faculty {i+1}")

# Link to write a survey
st.header("Write a Survey")
st.write("Please click [here](#) to finish a survey about your experience with this app.")

# Run the app
if __name__ == "__main__":
    st.warning("This demo requires internet access.")
