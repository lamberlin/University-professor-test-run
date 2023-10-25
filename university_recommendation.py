import streamlit as st
import pandas as pd
import os
import joblib
from chatbox import predict_universities
from MAB import cac_weight
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="University-recommendation", layout="centered", page_icon="logo.png", initial_sidebar_state="collapsed"
)
st.write(
    '<div style="text-align: center;">'
    '<h1 style="color: #E1930F;">University-recommendation</h1>'
    '<a href="https://docs.google.com/document/d/13BochD6AsN-zTQwEndk0LW0VdMjrbr0OLvmTaKGyYvc/edit?usp=sharing" target="_blank">Show me how to use this</a>'
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
    .big-font {
        font-family: 'Times New Roman', Times, serif;
        color: orange;
        font-size:20px !important;
        text-align:center;
        margin-bottom: 20px;
    }
</style>
<div class='big-font'>Other important academic preference to you</div>
""", unsafe_allow_html=True)
USNEWSmajor_ranking = st.sidebar.slider('USNEWS major ranking', 0.0, 100.0, 10.0, 0.1)
qsmajor_ranking = st.sidebar.slider('QS major ranking', 0.0, 100.0, 10.0, 0.1)
thmajor_ranking = st.sidebar.slider('Times High Education major ranking', 0.0, 100.0, 10.0, 0.1)
mean_school_world_reputation = st.sidebar.slider('General world reputation', 0.0, 100.0, 10.0, 0.1)
technology = st.sidebar.selectbox('Technology Strategy', ['Technology conservative', 'Technology-philic'])
mean_students_per_staff = st.sidebar.slider('Student culture vs Professor culture', 0.0, 100.0, 10.0, 0.1)
mean_international_students = st.sidebar.slider('Diversed ethnic culture', 0.0, 100.0, 10.0, 0.1)
avgDifficulty = st.sidebar.slider('Academically laid back vs academically rigorous', 0.0, 100.0, 10.0, 0.1)
topic = st.sidebar.selectbox('students view topic', ['Online learning', 'Career opportunities',
                                                     'General academic quality', 'Admission process',
                                                     'Diversity and inclusion', 'Student opportunities',
                                                     'Major programs', 'Financial aid and scholarships',
                                                     'Administration and school policies',
                                                     'Technology and computer labs'])
rating = st.sidebar.slider('Student view on University', 0.0, 100.0, 10.0, 0.1)
studentview_major = st.sidebar.slider('Student view on major', 0.0, 100.0, 10.0, 0.1)
avgRating = st.sidebar.slider('Student view on professor', 0.0, 100.0, 10.0, 0.1)
numRatings = st.sidebar.slider('engagement of student and professor', 0.0, 100.0, 10.0, 0.1)

col4, col5 = st.columns([5, 5])
with col4:
    major = st.selectbox('Select Major', ['architecture_design', 'biology', 'computer.science',
                                          'electrical.engineering', 'english.language.and.literature',
                                          'linguistics', 'history', 'development.studies', 'philosophy',
                                          'physics', 'psychology', 'political.science', 'sociology',
                                          'accounting.and.finance', 'communication_info', 'economics',
                                          'archeology', 'agriculture_environment', 'education', 'arts',
                                          'medicine_health', 'chemical.engineering', 'theology_theater',
                                          'law', 'mechanical.engineering', 'sports.sciences.and.management',
                                          'civil.engineering', 'geography'])

if 'rec' in st.session_state:
    st.write(
        '<h2 style="color: #6495ED;">Mark For University</h2>',
        unsafe_allow_html=True)
    st.dataframe(st.session_state["rec"])
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
        st.session_state["weight"] = cac_weight(cac_df)
        st.experimental_rerun()
else:
    st.markdown("<br>", unsafe_allow_html=True) #space
    st.markdown("""
<div class="arrow"></div><strong>Check the sidebar for more preferences!</strong>
""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  
    st.markdown("<div style='font-family:Times New Roman, Times, serif; font-size: 20px;'><strong>Give me key phrases "
                "that show your preference of the University?</strong></div>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  

    bullet_col = st.columns([1])[0]  

    with bullet_col:
        st.markdown("<div style='text-align:center; font-size: 24px;'>Examples:</div>", unsafe_allow_html=True)
        bullet_list = """
        <div style='text-align:center;'>
            <ul style='display:inline-block; text-align:left; font-size: 22px;'> <!-- Adjusted the font-size here -->
                <li><span class="copyable-text" onclick="copyToClipboard('well online leaning courses')">well online leaning courses</span></li>
                <li><span class="copyable-text" onclick="copyToClipboard('diversed major setting')">diversed major setting</span></li>
                <li><span class="copyable-text" onclick="copyToClipboard('beautiful library')">beautiful library</span></li>
            </ul>
        </div>
        """
        st.markdown(bullet_list, unsafe_allow_html=True)

    answer = st.text_input(
        label="answer",
        placeholder="Enter some key phrases",
        label_visibility='hidden'
    )
    if st.button("Recommend"):
        uni_dic = {}
        for cl in st.session_state["University"].classes_:
            uni_dic.update({cl: st.session_state["University"].transform([cl])[0]})

        model_data = pd.read_csv('model_data.csv')
        des_df = model_data[
            [_ for _ in model_data.columns if _ not in [_.split('.pkl')[0] for _ in os.listdir('models')]]].describe()
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
                        (des_df.loc['max', col] - des_df.loc['min', col]) * (1 - label_dic[col] * 0.01) + des_df.loc[
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
            if 'weight' not in st.session_state and chat_result != 'No matching universities found.':
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
            elif 'weight' not in st.session_state and chat_result == 'No matching universities found.':
                pass
            else:
                for uni in chat_result:
                    if uni in University_replace.keys():
                        show_df.loc[University_replace[uni], "probability"] = show_df.loc[University_replace[
                            uni], "probability"] * st.session_state['weight'][0] + chat_result[uni] * \
                                                                              st.session_state['weight'][1]
                    else:
                        show_df.loc[uni, "probability"] = show_df.loc[uni, "probability"] * st.session_state['weight'][
                            0] + chat_result[uni] * st.session_state['weight'][1]

            st.success("✅Recommend success")
            show_df["rank"] = show_df["probability"].rank(ascending=False).astype(int)
            show_df["probability"] = show_df["probability"].map(lambda x: '{:.2f}%'.format(x*100))
            st.dataframe(show_df.sort_values(by='rank')[:3].reset_index().rename(columns={'index': 'University'})[["rank", "University", "probability"]])

            if 'weight' not in st.session_state and chat_result != 'No matching universities found.':
                st.button('mark for above University')
                st.session_state["rec"] = show_df.sort_values(by='rank')[:3].reset_index().rename(columns={'index': 'University'})[["rank", "University", "probability"]]
                st.session_state["weight_df"] = weight_df.set_index('University').loc[st.session_state["rec"]["University"]]
            elif chat_result == 'No matching universities found.':
                if st.button("finish"):
                    st.experimental_rerun()
            else:
                st.session_state.pop('weight')
                st.session_state.pop('weight_df')
                st.write("Based on your input and academic preference, It seems  that {} with probability "
                         "{},{} with probability of {}, {} with probability of {} maybe be good "
                         "fits for you".format(show_df.sort_values(by='rank')[:3].index[0],
                                               show_df.sort_values(by='rank')[:3]["probability"][0],
                                               show_df.sort_values(by='rank')[:3].index[1],
                                               show_df.sort_values(by='rank')[:3]["probability"][1],
                                               show_df.sort_values(by='rank')[:3].index[2],
                                               show_df.sort_values(by='rank')[:3]["probability"][2]))
                if st.button("finish"):
                    st.experimental_rerun()
st.markdown(
    "<p style='text-align:center; color: #C5C5C5;'>Free prototype preview. AI may sometimes provide innacurate "
    "information. This model was trained on Reddit posts in r/collegeresults. Results will be biased towards posts "
    "from the subreddit.</p>",
    unsafe_allow_html=True,
)
