import streamlit as st
import lib.survey as sv

survey = sv.CustomStreamlitSurvey()

location = survey.text_input("location", help="Our location will appear shortly...", value=st.session_state.get('location', 'Venegono Superiore, Varese, Italy'))
button = survey.button("Submit", key="submit_location")

st.json(survey.data)


import streamlit_survey as ss

personal_data = ss.StreamlitSurvey(label="personal")
col1, col2 = st.columns([1, 1])
with col1:
    name = personal_data.text_input("Name", key="name")
    email = personal_data.text_input("Email", key="email")
with col2:
    phone = personal_data.text_input("Phone Number (starting with +)", key="phone")
    # default_start = datetime.datetime(2024, 9, 24)
    # default_end = default_start + timedelta(days=5)


st.write(personal_data.data)
