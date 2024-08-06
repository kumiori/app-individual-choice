import streamlit as st
import streamlit_survey as ss

def _submit(pages):
    st.write('Submit function called.')
    st.write(f'Received pages object: {pages}')
    survey_data = pages.survey.data  # or similar approach to access data
    st.write('Thanks, expand below to see your data')    
    st.json(survey_data, expanded=False)

survey = ss.StreamlitSurvey('Question map')

DEFAULT_SUBMIT_BUTTON = lambda pages: st.button(
    "Submit",
    type="primary",
    use_container_width=True,
    key=f"{pages.current_page_key}_btn_submit",
)
pages_total = 2
# Instantiate the survey with a debug lambda
pages = survey.pages(pages_total, 
        on_submit= DEFAULT_SUBMIT_BUTTON
        # lambda pages: _submit(pages)
        )
with pages:
    if pages.current == 0:
        st.write("Have you used Streamlit before?")
        used_before = survey.radio(
            "used_st_before", options=["NA", "Yes", "No"], index=0, label_visibility="collapsed", horizontal=True
        )
    elif pages.current == 1:
        st.write("How satisfied are you with this survey?")
        survey.select_slider(
            "Overall Satisfaction",
            options=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
            label_visibility="collapsed",
        )