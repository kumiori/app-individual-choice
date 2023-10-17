import streamlit as st
import streamlit_survey as ss

st.set_page_config(page_title="Home", page_icon="🍊")

st.header("Home 🍊")

st.markdown('''
Sometimes, sadness has an underlying reason which is the feeling of uncertainty regarding our future life together.

Therefore, let's to discuss our future in an intentional and clear way.

I have chosen you as my life partner and I am feeling very sure about this choice, plus I feel I'm at the stage of my life where I want to build a nest and grow long-lasting roots and I want to do it with you.

I want to be able to project myself in the future with you, and this thought keeps coming in, sometimes making me feel lost because there is nothing tangible to grasp.

I feel like each time we discuss it I am left in some way comforted and reassured and, in many ways, confused and not relieved.

I would therefore like to discuss this openly and very clearly to know our potential timeline as a couple. 

(This being said, it doesn't mean that I want to change anything right now or in the very near future, but within the next year – definitely):

''')
survey = ss.StreamlitSurvey()

# survey.select_slider(
#     "Likert scale:", options=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], id="Q1"
# )


st.text(dir(ss))
st.text(ss.__version__)

with st.expander("Some questions:", expanded=True):
    survey = ss.StreamlitSurvey("Questions Example")
    pages = survey.pages(2, on_submit=lambda: 
        st.success("Your responses have been recorded. Thank you!"))
    
    with pages:
        if pages.current == 0:
            st.write("Do you want to live together with me?")
            used_before = survey.radio(
                "used_st_before", options=["nan", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )

            if used_before == "Yes":
                st.write("Are you willing to transfer to Rome?")
                move_to_rome = survey.select_slider(
                    "st_move_to_rome",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )
                
                st.write("Would you like me to move to Paris?")
                move_to_paris = survey.select_slider(
                    "st_move_to_paris",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )

                st.write("Do you want to live with me within the next 12 months?")
                move_within_12_months = survey.select_slider(
                    "st_move_within_12_months",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )       
                         
                if move_within_12_months == "Yes":
                    st.write("When?")
                    date_input = survey.select_slider(
                    "st_move_when",
                    options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                    label_visibility="collapsed",
                )       
                    
            elif used_before == "No":
                st.write("Please write why and lets talk about it.")
                
                survey.text_input("Here are some thoughts...", id="Q3")
                # if used_other == "Yes":
                #     st.write("Which tools?")
                #     survey.multiselect(
                #         "other_tools",
                #         options=["Dash", "Voila", "Panel", "Bokeh", "Plotly", "Other"],
                #         label_visibility="collapsed",
                #     )
        elif pages.current == 1:
            st.write("How satisfied are you with this survey?")
            survey.select_slider(
                "Overall Satisfaction",
                options=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                label_visibility="collapsed",
            )


st.subheader("The data 🍊")

json = survey.to_json()
st.json(json)
st.text(dir(survey))
survey.download_button("Export Survey Data", use_container_width=True)


# survey.importer("Import Survey Data:")

