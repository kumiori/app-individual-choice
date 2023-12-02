import streamlit as st
import streamlit_survey as ss

st.set_page_config(page_title="Home", page_icon="🧊")

st.header("🧊 Hello 🧊")

st.markdown('''
Sometimes, _________ has an underlying reason which is the feeling of uncertainty regarding _____________.

Therefore, let's to discuss our ________ in an intentional and clear way.

I would therefore like to discuss this openly and very clearly to know our potential timeline.
''')
survey = ss.StreamlitSurvey()


with st.expander("Some questions:", expanded=True):
    survey = ss.StreamlitSurvey("Home")
    pages = survey.pages(2, on_submit=lambda: 
        st.success("Your responses have been recorded. Thank you!"))
    
    with pages:
        if pages.current == 0:
            st.write("Do you want to _______ together?")
            organise_together = survey.radio(
                "organise_together", options=["nan", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )

            if organise_together == "Yes":
                st.write("Are you willing to ____________?")
                move_1 = survey.select_slider(
                    "move_1",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )
                
                st.write("Would you like me to _________?")
                move_2 = survey.select_slider(
                    "move_2",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )

                st.write("Do you want to _________ within the next 12 months?")
                _within_12_months = survey.select_slider(
                    "_within_12_months",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )       
                         
                if _within_12_months == "Yes":
                    st.write("When?")
                    date_input = survey.select_slider(
                    "move_when",
                    options = ["October", "November", "December", "January", "February", "March", "April", "May", "June", "July", "August", "September"],
                    label_visibility="collapsed",
                )       
                    
            elif organise_together == "No":
                st.write("Please write why and lets talk about it.")
                
                survey.text_input("Here are some thoughts...", id="Q3")

        elif pages.current == 1:
            st.write("How satisfied are you with this survey?")
            survey.select_slider(
                "Overall Satisfaction",
                options=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                label_visibility="collapsed",
            )


st.subheader("The data 🍊")
st.json(survey.data)

json = survey.to_json()

st.download_button(
    label="Download preferences as JSON",
    data=json,
    file_name='survey.json',
    mime='text/json',
)
