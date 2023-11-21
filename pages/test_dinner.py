import streamlit.components.v1 as components
import streamlit as st
import streamlit_survey as ss
import time

st.header("🧊 Hello 🍴")

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)


def dichotomy(name, question, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    key=key,
    question = question)


def qualitative(name, question, data_values, key=None):
    return _qualitative_selector(component = "qualitative",
    name = name,
    key=key,
    data_values = data_values,
    question = question)

def qualitative_parametric(name, question, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    key=key,
    areas = areas,
    question = question)


survey = ss.StreamlitSurvey()


with st.expander("Some questions:", expanded=True):
    survey = ss.StreamlitSurvey("Home")
    pages = survey.pages(3, 
            on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))

    # pages.prev_button = lambda pages: None


    with pages:
        if pages.current == 0:
            st.write("Are you happy to dine?")
            dine_together = survey.radio(
                "dine_together", options=["nan", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )

            if dine_together == "Yes":
                st.write("To match your wishes, are you willing to share your preferences?")
                move_1 = survey.select_slider(
                    "move_1",
                    value = "nan",
                    options=["Yes", "nan", "No"],
                    label_visibility="collapsed",
                )
                
                if move_1 == "Yes":
                    st.success("Lovely!")
                if move_1 == "No":
                    st.error("That's alright, everybody likes surprises..")

            elif dine_together == "No":
                # pages.submit_button = lambda pages: st.button("See you next", type="primary", use_container_width=True)
                st.write("Fair enough...")
                
        # elif pages.current == 1:
            st.write('Share something about your preferences tonight...')
            st.write("What shall be your name?")
            name = survey.text_input("_During dinner_ I'd like to be called...", id="Q3")
            
            if name: st.success(f"Nice to meet you,  {name}")
            text1 = f"""
Well...{name}, coming or not: how you envision this dinner happening?

All is a matter of transitions, smoothness, and curiosity, isn't it?
"""

            text2 = f"""
Two versions are possible, for tonight, for your comfort and pleasure.

You can choose one of them, or something in between. _Refer to the black-and-white button below._


- **(White)** Yet Another Dinner...meh, or 
- **(Black)** A seducing, enticing, sexy, and arousing dinner event. A massage may be included. Possibly, transitioning into a mystical experience (XXX)

For you to be mindful, because all shades of gray separate (White) from (Black).
If unsure, be creative and playful: _wonder within_. 

                        _Greys indicate the in-between._ 
"""

        # elif pages.current == 2:
            st.markdown(text1)
            st.markdown(text2)
            experience = dichotomy(name = name, question = "Black or White dinner event? A hint above...", key = "boundaries")
            st.write('You picked me:', experience)
            
            if experience:
                survey.data['experience'] = {'label': 'dinner', 'value': experience}
                    
                if float(experience) < 0.1:
                    st.success("🖤")
                if float(experience) > 0.9:
                    st.info("Meh. Balloons?")
                    st.balloons()
                elif 0.1 < float(experience) < 0.9:
                    st.success("... something in between ...")
                    
            # (survey.data)
            st.json(survey.data)
            # st.json(st.session_state)
            