import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import streamlit_survey as ss
import time
from st_supabase_connection import SupabaseConnection
from streamlit_extras.streaming_write import write as streamwrite 
import numpy as np

import sys
sys.path.append('pages/')

from test_multicomponents import dichotomy
# qualitative, qualitative_parametric
inverse_choice = lambda x: 'OK 🥲' if x == 0 else 'junk food' if x == 1 else 'in-between ✨'
inverse_support = lambda x: 'support 🥲' if x == 1 else 'donate' if x == 2 else 'invest ✨' if x == 10 else 'in-between ✨'
dual_support = lambda x: 'connect 🥲' if x == 1 else 'receive' if x == 2 else 'propose ✨' if x == 10 else 'in-between ✨'

# st.set_page_config(
#     page_title="Data gathering: investment plans",
#     page_icon="✨",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

tabs = ["Questions Portal", "Business Plan", "Cosmic Revelations", "Minimal Gather"]

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)

# def dichotomy(name, question, key=None):
#     return _qualitative_selector(component = "dichotomy",
#     name = name,
#     key=key,
#     question = question)


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
    data_values  = [1, 2, 10],
    question = question)

def home():
    st.title("Welcome to the Home Page!")
    st.write("This is the home page content.")

def about():
    st.title("About Us")
    st.write("Learn more about our company on this page.")


def contact():
    st.title("Contact Us")
    st.write("Reach out to us through the contact page.")

# Initialize a DataFrame to store celestial responses
celestial_responses = pd.DataFrame(columns=['Star', 'Galaxy', 'Interest in Constellations', 'Stellar Feedback'])

def _stream_example(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.1)
        
if "text_streamed" not in st.session_state:
    st.session_state.text_streamed = False

# Celestial Portal
def question_portal():
    st.title('Data gathering:')
    st.write(
        "Welcome to the Data gathering. "
        "."
    )



    with st.expander("If you like to play...", expanded=False):
        survey = ss.StreamlitSurvey("Home")
        pages = survey.pages(4, 
                on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))

        # pages.prev_button = lambda pages: None

        with pages:
            if pages.current == 0:
                st.write("Have you already invested in the past?")
                dine_together = survey.radio(
                    "dine_together", options=["Yes", "No"], index=0,
                    label_visibility="collapsed", horizontal=True
                )

                if dine_together == "Yes":
                    st.write("To match your wishes, are you willing to store your preferences?")
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
                    elif move_1 == "nan":
                        st.info("If unsure, connect with us..")

                elif dine_together == "No":
                    st.write("Fair enough...")
                    
            elif pages.current == 1:
                # Question 1

                col1, col2, col3 = st.columns(3)

                # Question 1 in the first column
                with col1:
                    investment_references = survey.text_area("Would you like to share a wish?", help="Share your thoughts on investment.")

                # Question 2 in the second column
                with col2:
                    current_local_time = survey.timeinput("What is your current local time? Sorry to ask..")
                    localisation = survey.text_input("We start by showing something we have never seen...Where are you located now?", help="Enter the name of your birthplace.")

                # Question 3 and 4 in the third column
                with col3:
                    birthplace = survey.text_input("Where were you born?", help="Enter the name of your birthplace.")
                    lucky_number = survey.number_input("What's your lucky number?", min_value=0, max_value=100000000)

                st.write("----")
                name = survey.text_input("My animal spirit is...", id="name")
                st.session_state["name"] = name
                
            elif pages.current == 2:
                if 'name' in st.session_state: st.success(f"Nice to meet you, {st.session_state['name']}")
                text1 = f"""
                    Well...{st.session_state['name']}, ________ or not: how you envision this ____________ happening?
                    Take a moment to think about it, and a few seconds to read the following.
                    
                    All is a matter of arbitrary projections, numerology, and luck. Isn't it?
                    """

                # if st.button("Stream data"):
                # streamwrite(_stream_example(text1))
                if not st.session_state.text_streamed:
                    # Triggered by a button press or any other event
                    # if st.button("Stream data"):
                    streamwrite(_stream_example(text1))

                    # Mark that the text has been streamed in the current session
                    st.session_state.text_streamed = True
                else:
                    st.write(text1)
                    
                text2 = f"""
                    Two versions are possible, for tonight, for your comfort and pleasure.

                    You can choose one of them, or something in between. _Refer to the black-and-white button below._


                    - **(White)** Junk food, meh, or 
                    - **(Black)** Mystc Food Experience (XXX)

                    For you to be mindful, all shades of gray separate (White) from (Black).
                    If unsure, be creative and playful: _wonder within_. 

                                            _Greys indicate the in-between._ 
                    """

                st.markdown(text2)
                # with st.spinner('...'):
                    # time.sleep(1)

                col1, col2, col3 = st.columns([3, 1, 3])
                with col1:
                    experience = dichotomy(name = st.session_state['name'], question = "Hence...Black or White? A hint above...", key = "experience")
                
                with col3:    
                    if experience:
                        survey.data['experience'] = {'label': 'dinner', 'value': experience}
                        st.markdown(f'## Your choice <code>chooses</code> {experience}', unsafe_allow_html=True)
                        if experience:
                            st.write('Which, for us, is something like...')
                            if experience is not None:
                                st.markdown(f'## {inverse_choice(float(experience))}')

                        if float(experience) < 0.1:
                            st.success("🖤")
                        if float(experience) > 0.9:
                            st.info("Meh. Balloons?")
                            st.balloons()
                        elif 0.1 < float(experience) < 0.9:
                            st.success("... something in between ...")
                        
                        with st.spinner('Wait for it...'):
                            # time.sleep(2)
                            st.success('You have shared your preferences...Enjoy your experience!') 
                            st.json(survey.data, expanded = False)
                            
                st.markdown('If...you are _OK_, please, go to the next (and final) stage.')
            
            elif pages.current == 3:
                text3 = f"""
                        - **(White)** Yet Another Dinner...meh, or 
                        - **(Black)** A seducing, enticing, sexy, and arousing dinner event. A massage may be included. Possibly, transitioning into a mystical experience (XXX)
                    """
                st.markdown(text3)
                # st.write('You picked me:', experience)
                       
                # (survey.data)
                st.json(survey.data, expanded = False)
                st.json(st.session_state)
 
    # Add any additional cosmic content here
    return_value = dichotomy(name = "Fellow", question = " see below...", key = "boundaries")
    st.write('You picked me:', return_value)
    st.markdown("## Motivation")
    st.write(
        "The **Data gathering: investment plans** aims to provide users with a unique and immersive experience, guiding them through a cosmic journey of self-realization. The motivation behind this app is to blend the fascination of exploring the mysteries of the universe with the introspection of one's thoughts and feelings. By intertwining the celestial wonders with personal reflections, the app offers a novel approach to self-discovery."
    )












# questions
# you are taking part to a scientific experiment of careful observation
# of trends, preferences, and behaviours
# do you trust science?
# we are curious scientists,
# we guarantee: no data will be shared with third parties
# we will show you the results of the experiment
# and you will see something we have never seen before
# help us position so you can best receive our results
# where are you currently located?
# coordinates
# global map
# what are your current sky conditions?
# imagine science as a game. a competitive game, like basketball - some say
# it's the worst game. You know why?
# imagine science as a basketball game.
# where are your best skills, in defence or in attack?
# we need to count so that we update our team's strategy
# 











# Business Plan Section
def business_plan():
    st.header('enVision Business: Our Plans')
    st.write(
        "Embark on a celestial odyssey through the cosmos. "
        "Explore the mysteries of stars, galaxies, and the poetry written in the language of the universe."
    )
    
    st.write("1: Introduction 2: Business Description, 10: Products and Services, 11: Financial Plan, 25: Exit Strategy")
    return_value = qualitative(name = "Interested Reader", question = "What would you like to know more ?", data_values = [1, 2, 10, 11, 25], key = "qualitative")
    st.write('You picked me:', return_value)

    col1, col2, col3 = st.columns([1, .1, 1])

    
    with col1:
        st.markdown("## Scope")
        st.write(
            "The Data gathering: investment plans consists of three main sections:"
            "\n\n"
            "1. **Celestial Portal:** Embark on a cosmic journey, exploring the wonders of the universe. Users can engage in a dichotomy to understand their spiritual boundaries, offering a glimpse into their cosmic inclinations."
            "\n\n"
            "2. **Business Plan:** Delve deeper into the mysteries of stars and galaxies. Users are prompted to provide qualitative responses, reflecting their understanding of cosmic quantities and the intricacies of the celestial realm."
            "\n\n"
            "3. **Cosmic Revelations:** Unveil the secrets discovered during the celestial odyssey. This section prompts users to share their insights through qualitative parametric responses, allowing for a nuanced exploration of their perceptions."
        )

    with col3:
        st.markdown("## We Have an Advantage")
        st.write(
            "- **Immersive Cosmic Experience:** Unlike traditional self-realization apps, the Data gathering: investment plans provides a unique blend of cosmic exploration and personal reflection. Users are not only guided through celestial wonders but also encouraged to introspect based on cosmic themes."
            "\n\n"
            "- **Diverse Interaction:** The app offers various interaction components, including dichotomies, qualitative responses, and parametric inputs. This diversity ensures that users can express their thoughts in nuanced ways, capturing the intricacies of their cosmic journey."
            "\n\n"
            "- **Personalized Celestial Profiles:** As users engage with the app, their responses contribute to the creation of personalized celestial profiles. These profiles reflect the user's unique cosmic perspective and serve as a testament to their celestial voyage."
            "\n\n"
            "- **Seamless Navigation:** The use of Streamlit and tabs ensures a seamless and intuitive navigation experience. Users can effortlessly transition between different cosmic sections, enhancing overall usability."
        )

# Cosmic Revelations Section
def visualisation():
    st.header('Cosmic Revelations')
    st.write(
        "Reveal the celestial secrets unveiled during the Celestial Verse Odyssey. "
        "Journey through the profiles of cosmic poets, delve into their verses, and witness the dawn of new astronomical revelations."
    )

    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        support_value = qualitative_parametric(name = "## may be our lucky number",
            question = "Support, Donate, or Invest?",
            areas = 3,
            key = "parametric")
        # st.write('You picked:', support_value)
    with col3:
        st.markdown("## You are happy to " + inverse_support( int(support_value)) if support_value is not None else '')
        st.markdown("## We are happy to " + dual_support( int(support_value)) if support_value is not None else '')

    st.markdown("## Explore the Cosmos Within")
    st.write(
        "The Data gathering: investment plans invites users to embark on a journey of cosmic self-realization. By fusing the marvels of the universe with personal reflections, this app promises an unparalleled experience of discovering the cosmos within. Whether you're pondering spiritual boundaries, contemplating cosmic quantities, or unveiling profound revelations, the Data gathering: investment plans is your guide to a celestial odyssey of self-discovery. ✨"
    )

def minimalgather():
    col1, col2, col3 = st.columns([2, 1, 2])
    

    with col1:
        with st.expander("If you like to play...", expanded=False):
            survey = ss.StreamlitSurvey("Minimal")
            pages = survey.pages(3, 
                    on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))

            # pages.prev_button = lambda pages: None

            with pages:
                if pages.current == 0:
                    st.write("If you trust us?")
                    dine_together = survey.radio(
                        "dine_together", options=["Yes", "No"], index=0,
                        label_visibility="collapsed", horizontal=True
                    )

                    if dine_together == "Yes":
                        st.write("To match your wishes, are you willing to store your preferences?")
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
                        elif move_1 == "nan":
                            st.info("If unsure, connect with us..")

                    elif dine_together == "No":
                        st.write("Fair enough...")
                        
                elif pages.current == 1:
                    # Question 1

                    col1, col2, col3 = st.columns(3)

                    # Question 1 in the first column
                    with col1:
                        investment_references = survey.text_area("Would you like to share a wish?", help="Share your thoughts on investment.")

                    # Question 2 in the second column
                    with col2:
                        current_local_time = survey.timeinput("What is your current local time? Sorry to ask..")
                        localisation = survey.text_input("We start by showing something we have never seen...Where are you located now?", help="Enter the name of your birthplace.")

                    # Question 3 and 4 in the third column
                    with col3:
                        birthplace = survey.text_input("Where were you born?", help="Enter the name of your birthplace.")
                        lucky_number = survey.number_input("What's your lucky number?", min_value=0, max_value=100000000)
                
                elif pages.current == 2:
                        st.write()

        support_value = qualitative_parametric(name = "## may be our lucky number",
            question = "Support, Donate, or Invest?",
            areas = 3,
            key = "parametric3")
        # st.write('You picked:', support_value)
    with col3:
        st.markdown("## You are happy to " + inverse_support( int(support_value)) if support_value is not None else '')
        st.markdown("## We are happy to " + dual_support( int(support_value)) if support_value is not None else '')

    st.markdown("## Explore the Cosmos Within")
    st.write(
        "The Data gathering: investment plans invites users to embark on a journey of cosmic self-realization. By fusing the marvels of the universe with personal reflections, this app promises an unparalleled experience of discovering the cosmos within. Whether you're pondering spiritual boundaries, contemplating cosmic quantities, or unveiling profound revelations, the Data gathering: investment plans is your guide to a celestial odyssey of self-discovery. ✨"
    )

# Streamlit app with cosmic tabs
def main():
    st.title('Data gathering: investment plans')

    # Create tabs
    _tabs = st.tabs(tabs)

    # Display content based on selected tab
    # Traverse through cosmic tabs and unveil celestial wonders
    for i, selected_tab in enumerate(tabs):
        with _tabs[i]:
            if selected_tab == "Questions Portal":
                question_portal()
            elif selected_tab == "Business Plan":
                business_plan()
            elif selected_tab == "Cosmic Revelations":
                visualisation()
            elif selected_tab == "Minimal Gather":
                minimalgather()

# Run the cosmic app
if __name__ == "__main__":
    main()
