import sys
import streamlit.components.v1 as components
import streamlit as st
import streamlit_survey as ss
import time
from st_supabase_connection import SupabaseConnection
import json
# st.write(sys.path)
# sys.path.append('../lib')
# from libquestions import questions

table_name = "dinners"

# import test_lib
story  = """
"""
plan  = """The plan is three-fold:
1. From underwater to survival
2. Kick out the nasty bug, make him pay damages
3. Steering the ship, with a new crew



"""

st.header("Welcome to the game ⥸")
st.markdown('Competition is twofold: both defense and attack. This is Global Basketball, not italian soccer.')
_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)

if "name" not in st.session_state:
    st.session_state["name"] = ''


def qualitative_parametric(name, question, areas, data_values, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    key=key,
    areas = areas,
    data_values  = data_values,
    question = question)

        
def dichotomy(name, question, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    key=key,
    question = question)


# def qualitative(name, question, data_values, key=None):
#     return _qualitative_selector(component = "qualitative",
#     name = name,
#     key=key,
#     data_values = data_values,
#     question = question)

# def qualitative_parametric(name, question, areas, key=None):
#     return _qualitative_selector(component = "parametric",
#     name = name,
#     key=key,
#     areas = areas,
#     question = question)


survey = ss.StreamlitSurvey()

st.markdown(story)
st.markdown(plan)

with st.expander("We are seeking to steer ", expanded=True):
    survey = ss.StreamlitSurvey("Home")
    pages = survey.pages(3, 
            on_submit=lambda: st.success("Your responses have been downloaded. Come again to check your results."))
    pages.submit_button = lambda pages: st.button("Download", type="primary", use_container_width=True)
    # st.write(dir(pages.submit_button))
    # pages.prev_button = lambda pages: None

    with pages:
        if pages.current == 0:
            st.write("Are you happy to play?")
            play = survey.radio(
                "play", options=["Unsure", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )

            if play == "Yes":
                st.write("To match your perspective, are you willing to share your preferences?")
                move_1 = survey.select_slider(
                    "move_1",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )
                
                if move_1 == "Yes":
                    st.success("Lovely!")
                if move_1 == "No":
                    st.error("That's alright, you will be missing out.")

            elif play == "No":
                st.write("Fair enough...")
                
        elif pages.current == 1:
            st.write('Did we already meet?')
            st.write("What is your name?")
            name = survey.text_input("_Your preferences_ are precious. Let's save them, shout outs to:", id="name")
            st.session_state["name"] = name
            
        elif pages.current == 2:
            if 'name' in st.session_state: st.success(f"Nice to meet you, {st.session_state['name']}")
            text1 = f"""
                Well...{st.session_state['name']}, _______ or not: 
                """

            text2 = f"""
                Are you Them, or are you Us, The Stella Mater + Special stars.
                You can choose one of them, or something in between if you want to know more. 
                _Refer to the black-and-white button below._


                - **(White)** ...meh, or 
                - **(Black)**  (XXX)

                For you to be mindful, ...: _wonder within_. 

                                        _Greys indicate the in-between._ 
                """

            st.markdown(text1)
            st.markdown(text2)
            # with st.spinner('...'):
                # time.sleep(15)
                
            # st.markdown('If...you are _OK_, please, go to the next (and final) stage.')
        # elif pages.current == 3:
            text3 = f"""
                    - **(White)** ...meh, or 
                    - **(Black)**  (XXX)
                """
            st.markdown(text3)
            experience = dichotomy(name = st.session_state['name'], question = "Hence...Black or White? A hint above...", key = "boundaries")
            # st.write('You picked me:', experience)
            
            if experience:
                survey.data['experience'] = {'label': 'dinner', 'value': experience}
                    
                if float(experience) < 0.1:
                    st.success("😉")
                if float(experience) > 0.9:
                    st.info("Meh. Balloons?")
                    st.balloons()

                    uploaded_file = st.file_uploader('Upload your balance sheet as a portable document (file format).', type="pdf")
                    if uploaded_file is not None:
                        st.info("Good. We let it through a few automated tests, and then we will connect.")
                        # df = extract_data(uploaded_file)
                        st.write('If data looks good, your fine. If data is corrupt, we fuck you.')
                        # st.write(uploaded_file)


                elif 0.1 < float(experience) < 0.9:
                    st.success("... something in between ...")
                    with st.spinner('It\'s a matter of time'):
                        time.sleep(15)
                        st.text('... here is the story ...')
                    
                with st.spinner('Wait for it...'):
                    time.sleep(2)
                    st.error('Your preferences are taken into account...We shall connect.')         
            # (survey.data)
            # st.json(st.session_state)

            data_values = [1, 10, 100]
            return_value = int(qualitative_parametric(name = "Spirit",
                question = "Boundaries matter, see below...",
                areas = 3,
                data_values  = data_values,
                key = "parametric"))
            st.markdown(f'You picked: {return_value}%')
            
            if return_value == int(data_values[0]):
                st.info('Small damage.')
            elif return_value == int(data_values[1]):
                st.warning('Medium damage.')
            else:
                st.error('Fatal damage.')


            st.json(survey.data, expanded = False)
