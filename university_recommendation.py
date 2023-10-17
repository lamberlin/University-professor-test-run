import streamlit as st
import pandas as pd

# Create a dictionary of universities and their attributes
universities = {
    "Yale": {
        "reputation": 4.5,
        "USNEWS": 80,
        "QS": 70,
        "Times Higher Education": 40,
        "Student Culture vs Professor Culture": 90,
        "ethnic_culture": 100,
        "Technology Strategy": 90,
        "Student View on Major": 70,
        "Level of Study": 40,
        "Student View on Faculty": 80,
    },
    "Berkeley": {
        "reputation": 4.2,
        "USNEWS": 20,
        "QS": 60,
        "Times Higher Education": 90,
        "Student Culture vs Professor Culture": 10,
        "ethnic_culture": 1,
        "Technology Strategy": 10,
        "Student View on Major": 30,
        "Level of Study": 90,
        "Student View on Faculty": 10,
    },
    "Columbia": {
        "reputation": 4.7,
        "USNEWS": 80,
        "QS": 70,
        "Times Higher Education": 90,
        "Student Culture vs Professor Culture": 70,
        "ethnic_culture": 1,
        "Technology Strategy": 80,
        "Student View on Major": 50,
        "Level of Study": 90,
        "Student View on Faculty": 60,
    },
}

# Create a DataFrame from the universities dictionary
df = pd.DataFrame(universities).T.reset_index()
df = df.rename(columns={"index": "University"})

# Create a function to recommend universities based on user preferences
def recommend_universities(user_preferences):
    # Calculate the total rank based on the preferences
    df["Total Rank"] = df[["reputation", "USNEWS", "QS", "Times Higher Education", "Student Culture vs Professor Culture", "ethnic_culture", "Technology Strategy", "Student View on Major", "Level of Study", "Student View on Faculty"]].sum(axis=1)
    
    # Sort the DataFrame by total rank in descending order
    filtered_df = df.sort_values(by="Total Rank", ascending=False)
    
    return filtered_df

# Streamlit app
st.title("University Recommendation System")

# User preferences
st.sidebar.header("User Preferences")
major = st.sidebar.selectbox("Select Major", ['Architecture', 'Biology', 'Computer Science', 'Electrical Engineering', 'English Language and Literature', 'Linguistics', 'History', 'Development Studies', 'Environmental Sciences', 'Philosophy', 'Physics', 'Psychology', 'Political Science', 'Sociology', 'Accounting and Finance', 'Communication Info', 'Economics', 'Archeology', 'Education', 'Arts', 'Medicine and Health', 'Chemical Engineering', 'Theology', 'Agriculture and Forestry', 'Dentistry', 'Geography', 'Law', 'Mathematics and Statistics', 'Civil Engineering', 'Sports Sciences and Management', 'Mechanical Engineering'])

# Create expandable sections for preferences
with st.sidebar.expander("Expert View on Universities' Majors"):
    usnews = st.slider("USNEWS", 0, 100, 50, step=1)
    qs = st.slider("QS", 0, 100, 50, step=1)
    times_higher_education = st.slider("Times Higher Education", 0, 100, 50, step=1)

with st.sidebar.expander("University Reputation"):
    reputation = st.slider("Reputation", 0, 100, 50, step=1)

with st.sidebar.expander("Student Culture vs Professor Culture"):
    student_culture_vs_professor_culture = st.slider("Student Culture vs Professor Culture", 0, 100, 50, step=1)

with st.sidebar.expander("Ethnic Culture"):
    ethnic_culture = st.slider("Ethnic Culture", 0, 100, 50, step=1)

with st.sidebar.expander("Student View on University"):
    technology_strategy = st.slider("Technology Strategy", 0, 100, 50, step=1)
    student_view_on_major = st.slider("Student View on Major", 0, 100, 50, step=1)
    level_of_study = st.slider("Level of Study", 0, 100, 50, step=1)
    student_view_on_faculty = st.slider("Student View on Faculty", 0, 100, 50, step=1)

# Recommendation
if st.sidebar.button("Recommend for me"):
    user_preferences = {
        "USNEWS": usnews,
        "QS": qs,
        "Times Higher Education": times_higher_education,
        "reputation": reputation,
        "Student Culture vs Professor Culture": student_culture_vs_professor_culture,
        "ethnic_culture": ethnic_culture,
        "Technology Strategy": technology_strategy,
        "Student View on Major": student_view_on_major,
        "Level of Study": level_of_study,
        "Student View on Faculty": student_view_on_faculty,
    }
    
    recommended_universities = recommend_universities(user_preferences)
    st.header("University Recommendations")
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
    st.header("Fill out a Survey")
    st.write("Please click [here](#) to finish a survey about your experience with this app.")
