import streamlit as st
import pandas as pd
import joblib

loaded_model = joblib.load("log_reg_classifier_balanced.joblib")


user_data = pd.DataFrame(columns=['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score', 'A6_Score',
           'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score', 'age', 'gender',
           'jaundice', 'family_autism', 'used_app_before', 'ethnicity_Asian',
           'ethnicity_Black', 'ethnicity_Hispanic', 'ethnicity_Latino',
           'ethnicity_Middle Eastern ', 'ethnicity_Others', 'ethnicity_Pasifika',
           'ethnicity_South Asian', 'ethnicity_Turkish', 'ethnicity_White-European'])


st.title("Autism Test")

question_dict = {"1. I often notice small sounds when others do not." : "A1_Score", 
                 "2. When I’m reading a story, I find it difficult to work out the characters’ intentions." : "A2_Score", 
                 "3. I find it easy to 'read between the lines' when someone is talking to me." : "A3_Score", 
                 "4. I usually concentrate more on the whole picture, rather than the small details." : "A4_Score", 
                 "5. I know how to tell if someone listening to me is getting bored." : "A5_Score", 
                 "6. I find it easy to do more than one thing at once." : "A6_Score", 
                 "7. I find it easy to work out what someone is thinking or feeling just by looking at their face." : "A7_Score", 
                 "8. If there is an interruption, I can switch back to what I was doing very quickly." : "A8_Score", 
                 "9. I like to collect information about categories of things." : "A9_Score",
                 "10. I find it difficult to work out people’s intentions" : "A10_Score", 
                 "11. What is your age?": "age",
                 "12. What is your gender?": "gender",
                 "13. Did you have jaundice when you were born?": "jaundice",
                 "14. Has anyone in your family been diagnosed with autism?": "family_autism", 
                 "15. Have you ever been tested by a dcotor for autism?": "used_app_before"}



ethnicity_to_column = {
    "White-European": "ethnicity_White-European",
    "Other": "ethnicity_Others",
    "Middle Eastern": "ethnicity_Middle Eastern ",
    "Asian": "ethnicity_Asian",
    "Black": "ethnicity_Black",
    "South Asian": "ethnicity_South Asian",
    "Pacific": "ethnicity_Pasifika",
    "Latino": "ethnicity_Latino",
    "Hispanic": "ethnicity_Hispanic",
    "Turkish": "ethnicity_Turkish"
}


for question, column_name in question_dict.items():
    if "Score" in column_name:
        response = st.selectbox(question, ["Agree", "Disagree"])
        user_data.at[0, column_name] = 1 if response == "Agree" else 0
    elif column_name == "age":
        response = st.number_input(question, min_value=0, max_value=120, step=1)
        user_data.at[0, column_name] = response
    elif column_name == "gender":
        respose = st.selectbox(question, ["Male", "Female"])
        user_data.at[0, column_name] = 1 if response == "Female" else 0
    elif column_name == "gender" or column_name == "family_autism" or "used_app_before":
        response = st.selectbox(question, ["Yes", "No"])
        user_data.at[0, column_name] = 1 if response == "Yes" else 0



selected_ethnicity = st.selectbox("Which of the following best describes your ethnicity", list(ethnicity_to_column.keys()))
selected_col = ethnicity_to_column[selected_ethnicity]

for ethnicity, col in ethnicity_to_column.items():
    if col == selected_col:
        user_data.at[0, col] = 1
    else:
        user_data.at[0, col] = 0


prediction = loaded_model.predict(user_data)

if prediction == 1:
    st.write("It is very likely you would be diagnosed with autism")
else:
    st.write("It is very unlikely you have autism")