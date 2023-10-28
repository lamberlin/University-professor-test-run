import streamlit as st
import pandas as pd
import os
import joblib
from chatbox import predict_universities
from MAB import cac_weight
import warnings
import time
import openai
import requests
import base64
import io




warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Reach Best LUR Bot", layout="centered", page_icon="logo.png", initial_sidebar_state="collapsed"
)
st.write(
    '<div style="text-align: center;">'
    '<h1 style="color: #E1930F;">Reach Best LUR Bot</h1>'
    '</div>',
    unsafe_allow_html=True)
st.markdown("""
<style>
.arrow {
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 15px solid black;
  display: inline-block;
  margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)


University_replace = {
    'University of California, Berkeley': 'University of California Berkeley',
    'University of California, Los Angeles': 'University of California Los Angeles (UCLA)',
    'University of North Carolina at Chapel Hill': 'The University of North Carolina at Chapel Hill',
    'University of California, San Diego': 'University of California San Diego',
    'University of California, Santa Barbara': 'University of California Santa Barbara'
}
def push_df_to_github(df):
    TOKEN = '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'  # Replace with your GitHub token
    REPO_OWNER = 'lamberlin'
    REPO_NAME = 'University-professor-test-run'
    FILE_PATH = 'ID%20weight.csv'
    
    # Convert DataFrame to CSV & Base64 encode
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    encoded_content = base64.b64encode(buffer.getvalue().encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    # Fetch the file to get its SHA
    response = requests.get(f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}', headers=headers)
    if response.status_code != 200:
        print("Error fetching the file from GitHub:", response.json())
        return
    
    sha = response.json()['sha']
    
    # Update the file
    update_data = {
        "message": "Updated ID weight.csv",
        "content": encoded_content,
        "sha": sha
    }
    response = requests.put(f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}', headers=headers, json=update_data)
    
    if response.status_code == 200:
        print("Successfully pushed to GitHub.")
    else:
        print("Error pushing to GitHub:", response.json())
ID_weight = pd.read_csv('ID weight.csv')

if 'University' not in st.session_state:
    for _ in os.listdir('models'):
        st.session_state[_.split('.pkl')[0]] = joblib.load(os.path.join('models', _))
else:
    pass
st.sidebar.markdown(
    '<div style="text-align: center; margin-top: 0; padding-top: 0;margin-bottom: 20px;">'
    '<img src="https://i.imgur.com/CMfb6aI.png" style="width: 30%;height:30%">'
    '</div>',
    unsafe_allow_html=True)
st.sidebar.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Proxima+Nova&display=swap');
    .big-font {
        font-family: 'Proxima Nova', Arial, sans-serif;
        color: black;
        font-size:20px !important;
        text-align:center;
        margin-bottom: 20px;
    }
</style>
<div class='big-font'>Adjust Weights</div>
""", unsafe_allow_html=True)
col1, col2 = st.sidebar.columns(2)

# General preference items in the first column
with col1:
    with st.expander("General Preference"):
        USNEWSmajor_ranking = st.slider('USNEWS major ranking', 0.0, 100.0, 10.0, 0.1)
        qsmajor_ranking = st.slider('QS major ranking', 0.0, 100.0, 10.0, 0.1)
        thmajor_ranking = st.slider('Times High Education major ranking', 0.0, 100.0, 10.0, 0.1)
        mean_school_world_reputation = st.slider('General world reputation', 0.0, 100.0, 10.0, 0.1)
        technology = st.selectbox('Technology Strategy', ['Technology conservative', 'Technology-philic'])
        mean_students_per_staff = st.slider('Student culture vs Professor culture', 0.0, 100.0, 10.0, 0.1)
        mean_international_students = st.slider('Diversed ethnic culture', 0.0, 100.0, 10.0, 0.1)
        avgDifficulty = st.slider('Academically laid back vs academically rigorous', 0.0, 100.0, 10.0, 0.1)

# Students' view items in the second column
with col2:
    with st.expander("Students' View"):
        topic = st.selectbox('students view topic', ['Online learning', 'Career opportunities',
                                                     'General academic quality', 'Admission process',
                                                     'Diversity and inclusion', 'Student opportunities',
                                                     'Major programs', 'Financial aid and scholarships',
                                                     'Administration and school policies',
                                                     'Technology and computer labs'])
        rating = st.slider('Student view on University', 0.0, 100.0, 10.0, 0.1)
        studentview_major = st.slider('Student view on major', 0.0, 100.0, 10.0, 0.1)
        avgRating = st.slider('Student view on professor', 0.0, 100.0, 10.0, 0.1)
        numRatings = st.slider('engagement of student and professor', 0.0, 100.0, 10.0, 0.1)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='font-size: 24px;'>Examples-general preference</div>", unsafe_allow_html=True)
    general_list = """
    <ul style='font-size: 22px; padding-left: 0; list-style-type: none;'> <!-- Adjusted the font-size here -->
        <li><span class="copyable-text" onclick="copyToClipboard('well online leaning courses')">well online leaning courses</span></li>
        <li><span class="copyable-text" onclick="copyToClipboard('diversed major setting')">diversed major setting</span></li>
        <li><span class="copyable-text" onclick="copyToClipboard('beautiful library')">beautiful library</span></li>
    </ul>
    """
    st.markdown(general_list, unsafe_allow_html=True)

# For "Examples of specific major"
with col2:
    st.markdown("<div style='font-size: 24px;'>Examples-specific majors</div>", unsafe_allow_html=True)
    major_list = """
    <ul style='font-size: 22px; padding-left: 0; list-style-type: none;'> <!-- Adjusted the font-size here -->
        <li><span class="copyable-text" onclick="copyToClipboard('strong engineering')">strong engineering</span></li>
        <li><span class="copyable-text" onclick="copyToClipboard('great computer labs')">great computer labs</span></li>
        <li><span class="copyable-text" onclick="copyToClipboard('unique CS courses')">unique CS courses</span></li>
    </ul>
    """
    st.markdown(major_list, unsafe_allow_html=True)
col4, col5 = st.columns([5, 5])
with col4:
    username = st.text_input(
        label="Save your personalized model",
        placeholder="Enter your name"
    )


with col5:
    major = st.selectbox(
        'Select Major', 
        ['architecture_design', 'biology', 'computer.science',
         'electrical.engineering', 'english.language.and.literature',
         'linguistics', 'history', 'development.studies', 'philosophy',
         'physics', 'psychology', 'political.science', 'sociology',
         'accounting.and.finance', 'communication_info', 'economics',
         'archeology', 'agriculture_environment', 'education', 'arts',
         'medicine_health', 'chemical.engineering', 'theology_theater',
         'law', 'mechanical.engineering', 'sports.sciences.and.management',
         'civil.engineering', 'geography']
    )
if 'rec' in st.session_state:
    st.write(
        '<h2 style="color: #6495ED;">Mark For University</h2>',
        unsafe_allow_html=True)
    st.dataframe(st.session_state["rec"])
    st.markdown("Based on your input and academic preference, It seems  that **{}** with probability "
                "**{}**,**{}** with probability of **{}**, **{}** with probability of **{}** maybe be good "
                "fits for you".format(st.session_state["rec"].sort_values(by='rank')[:3].index[0],
                                      st.session_state["rec"].sort_values(by='rank')[:3]["probability"][0],
                                      st.session_state["rec"].sort_values(by='rank')[:3].index[1],
                                      st.session_state["rec"].sort_values(by='rank')[:3]["probability"][1],
                                      st.session_state["rec"].sort_values(by='rank')[:3].index[2],
                                      st.session_state["rec"].sort_values(by='rank')[:3]["probability"][2]))
    col1, col2, col21, col22, col23 = st.columns([2, 1, 1, 1, 1])
    col3, col4, col41, col42, col43 = st.columns([2, 1, 1, 1, 1])
    col5, col6, col61, col62, col63 = st.columns([2, 1, 1, 1, 1])
    with col1:
        st.write(st.session_state["rec"]["University"][0])
    with col2:
        if st.button("👍👍"):
            st.session_state["marks1"] = 9
    with col21:
        if st.button("👍"):
            st.session_state["marks1"] = 7
    with col22:
        if st.button("👎"):
            st.session_state["marks1"] = 3
    with col23:
        if st.button("👎👎"):
            st.session_state["marks1"] = 1
    with col3:
        st.write(st.session_state["rec"]["University"][1])
    with col4:
        if st.button("👍👍", key='1'):
            st.session_state["marks2"] = 9
    with col41:
        if st.button("👍", key='2'):
            st.session_state["marks2"] = 7
    with col42:
        if st.button("👎", key='3'):
            st.session_state["marks2"] = 3
    with col43:
        if st.button("👎👎", key='4'):
            st.session_state["marks2"] = 1
    with col5:
        st.write(st.session_state["rec"]["University"][2])
    with col6:
        if st.button("👍👍", key='11'):
            st.session_state["marks3"] = 9
    with col61:
        if st.button("👍", key='21'):
            st.session_state["marks3"] = 7
    with col62:
        if st.button("👎", key='31'):
            st.session_state["marks3"] = 3
    with col63:
        if st.button("👎👎", key='41'):
            st.session_state["marks3"] = 1
    if st.button('submit'):
        st.session_state.pop('rec')
        cac_df = st.session_state["weight_df"]
        cac_df["User scores"] = [st.session_state["marks1"], st.session_state["marks2"], st.session_state["marks3"]]
#         push_df_to_github(pd.concat([ID_weight, pd.DataFrame(
#             [username, cac_weight(cac_df)[0], cac_weight(cac_df)[1],
#              st.session_state["answer"]], index=ID_weight.columns).T],
#                   ignore_index=True).to_csv(
#             'ID weight.csv', index=False))
        new_csv = pd.concat([ID_weight, pd.DataFrame(
            [username, cac_weight(cac_df)[0], cac_weight(cac_df)[1],
             st.session_state["answer"]], index=ID_weight.columns).T], 
            ignore_index=True)
        push_df_to_github(new_csv)
        # st.session_state["weight"] = cac_weight(cac_df)
        st.session_state.pop('weight_df')
        st.experimental_rerun()
else:
    answer = st.text_input('Give key phrases that show your preference of University', key="text_area", placeholder='E.g.beautiful library')
    if username in ID_weight["name"].tolist():
        try:
            st.write("Your last answer: {}".format(ID_weight.set_index('name').loc[username, "lastphrase"].values[-1]))
        except:
            st.write("Your last answer: {}".format(ID_weight.set_index('name').loc[username, "lastphrase"]))
    if st.button("Recommend"):
        st.session_state["answer"] = answer
        if username != '':
            if username in ID_weight["name"].tolist():
                try:
                    st.session_state["rem_weight"] = [
                        ID_weight.set_index('name').loc[username, "Model1weight"].values[-1],
                        ID_weight.set_index('name').loc[username, "Model2weight"].values[-1]]
                except:
                    st.session_state["rem_weight"] = [ID_weight.set_index('name').loc[username, "Model1weight"],
                                                      ID_weight.set_index('name').loc[username, "Model2weight"]]
            else:
                pass
            uni_dic = {}
            for cl in st.session_state["University"].classes_:
                uni_dic.update({cl: st.session_state["University"].transform([cl])[0]})

            model_data = pd.read_csv('model_data.csv')
            des_df = model_data[
                [_ for _ in model_data.columns if
                 _ not in [_.split('.pkl')[0] for _ in os.listdir('models')]]].describe()
            st.write("Your Answer: {}".format(answer))
            with st.spinner("Calculating, please wait..."):
                pred_lis = []
                label_dic = {
                    'major_field': major,
                    'sub_topic': topic,
                    'Technology_strategy': technology,
                    'USNEWSmajor_ranking': USNEWSmajor_ranking,
                    'qsmajor_ranking': qsmajor_ranking,
                    'thmajor_ranking': thmajor_ranking,
                    'mean_school_world_reputation': mean_school_world_reputation,
                    'mean_students_per_staff': mean_students_per_staff,
                    'mean_international_students': mean_international_students,
                    'studentview_major': studentview_major,
                    'avgRating': avgRating,
                    'numRatings': numRatings,
                    'avgDifficulty': avgDifficulty,
                    'rating': rating
                }
                for col in model_data.columns[1:]:
                    if col in [_.split('.pkl')[0] for _ in os.listdir('models')]:
                        pred_lis.append(int(st.session_state[col].transform([label_dic[col]])[0]))
                    elif col in ['USNEWSmajor_ranking', 'qsmajor_ranking', 'thmajor_ranking',
                                 'mean_school_world_reputation']:
                        pred_lis.append(
                            (des_df.loc['max', col] - des_df.loc['min', col]) * (1 - label_dic[col] * 0.01) +
                            des_df.loc[
                                'min', col])
                    else:
                        pred_lis.append(
                            (des_df.loc['max', col] - des_df.loc['min', col]) * label_dic[col] * 0.01 + des_df.loc[
                                'min', col])
                show_df = pd.DataFrame(st.session_state["model"].predict_proba(
                    pd.DataFrame(pred_lis, index=model_data.columns[1:]).T
                ), columns=list(uni_dic.keys()), index=['probability']).T
                weight_df = show_df.reset_index().rename(columns={'index': 'University', 'probability': 'Model1'})

                chat_result = predict_universities(answer)
                weight_ = []
                if 'weight' not in st.session_state and 'rem_weight' not in st.session_state:
                    for uni in chat_result:
                        if uni in University_replace.keys():
                            weight_.append({'University': University_replace[uni], 'Model2': chat_result[uni]})
                            show_df.loc[University_replace[uni], "probability"] = (show_df.loc[University_replace[
                                uni], "probability"] + chat_result[uni]) / 2
                        else:
                            weight_.append({'University': uni, 'Model2': chat_result[uni]})
                            show_df.loc[uni, "probability"] = (show_df.loc[uni, "probability"] + chat_result[uni]) / 2
                    weight_df = pd.merge(weight_df, pd.DataFrame(weight_), on='University')
                    weight_df["weight1"] = [0.5 for _ in range(weight_df.shape[0])]
                    weight_df["weight2"] = [0.5 for _ in range(weight_df.shape[0])]
                elif 'weight' not in st.session_state and 'rem_weight' in st.session_state:
                    for uni in chat_result:
                        if uni in University_replace.keys():
                            weight_.append({'University': University_replace[uni], 'Model2': chat_result[uni]})
                            show_df.loc[University_replace[uni], "probability"] = show_df.loc[University_replace[
                                uni], "probability"] * st.session_state['rem_weight'][0] + chat_result[uni] * \
                                                                                  st.session_state['rem_weight'][1]
                        else:
                            weight_.append({'University': uni, 'Model2': chat_result[uni]})
                            show_df.loc[uni, "probability"] = show_df.loc[uni, "probability"] * \
                                                              st.session_state['rem_weight'][
                                                                  0] + chat_result[uni] * \
                                                              st.session_state['rem_weight'][1]
                    weight_df = pd.merge(weight_df, pd.DataFrame(weight_), on='University')
                    weight_df["weight1"] = [0.5 for _ in range(weight_df.shape[0])]
                    weight_df["weight2"] = [0.5 for _ in range(weight_df.shape[0])]
                else:
                    for uni in chat_result:
                        if uni in University_replace.keys():
                            show_df.loc[University_replace[uni], "probability"] = show_df.loc[University_replace[
                                uni], "probability"] * st.session_state['weight'][0] + chat_result[uni] * \
                                                                                  st.session_state['weight'][1]
                        else:
                            show_df.loc[uni, "probability"] = show_df.loc[uni, "probability"] * \
                                                              st.session_state['weight'][
                                                                  0] + chat_result[uni] * st.session_state['weight'][1]

                st.success("✅Recommend success")
                show_df["rank"] = show_df["probability"].rank(ascending=False).astype(int)
                show_df["probability"] = show_df["probability"].map(lambda x: '{:.2f}%'.format(x * 100))
                st.dataframe(show_df.sort_values(by='rank')[:3].reset_index().rename(columns={'index': 'University'})[
                                 ["rank", "University", "probability"]])

                st.markdown(
    "<div style='display: block; text-align: center; margin-bottom: -10px; font-size: 0.85em;'>"
    "💡 <i>Give feedback on the recommendations so we can make it more personalized for you</i>"
    "</div>", 
    unsafe_allow_html=True
)
                st.button('rate the output')
                
                st.session_state["rec"] = \
                    show_df.sort_values(by='rank')[:3].reset_index().rename(columns={'index': 'University'})[
                        ["rank", "University", "probability"]]
                st.session_state["weight_df"] = weight_df.set_index('University').loc[
                    st.session_state["rec"]["University"]]

                st.markdown("Based on your input and academic preference, It seems  that **{}** with probability "
                            "**{}**,**{}** with probability of **{}**, **{}** with probability of **{}** maybe be good "
                            "fits for you".format(show_df.sort_values(by='rank')[:3].index[0],
                                                  show_df.sort_values(by='rank')[:3]["probability"][0],
                                                  show_df.sort_values(by='rank')[:3].index[1],
                                                  show_df.sort_values(by='rank')[:3]["probability"][1],
                                                  show_df.sort_values(by='rank')[:3].index[2],
                                                  show_df.sort_values(by='rank')[:3]["probability"][2]))
                top_universities = show_df.sort_values(by='rank')[:3]

#                 llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai.api_key, temperature=0)
#                 embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

                

        else:
            st.warning("You should input you name first!")
            time.sleep(2)
            st.experimental_rerun()
st.markdown(
    "<p style='text-align:center; color: #C5C5C5;'>Free prototype preview. AI may sometimes provide innacurate "
    "information. This model was trained on Nich reviews and Rate My Professors. "
    "</p>",
    unsafe_allow_html=True,
)
