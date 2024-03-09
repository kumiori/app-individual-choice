import streamlit as st
import lib.survey as sv

survey = sv.CustomStreamlitSurvey()

location = survey.text_input("location", help="Our location will appear shortly...", value=st.session_state.get('location', 'Venegono Superiore, Varese, Italy'))
button = survey.button("Submit", key="submit_location")

st.json(survey.data)

