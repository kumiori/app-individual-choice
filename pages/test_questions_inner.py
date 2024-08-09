import streamlit as st
import numpy as np
import streamlit_survey as ss
from lib.survey import CustomStreamlitSurvey
from lib.io import (
    create_button, create_checkbox, create_dichotomy, create_equaliser, create_equaliser,
    create_globe, create_next, create_qualitative, create_textinput,
    create_yesno, create_yesno_row, fetch_and_display_data, conn
)
# from lib.texts import stream_text, _stream_once
from datetime import datetime, timedelta
from streamlit_extras.stateful_button import button as stateful_button 
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import philoui as ph
from philoui.texts import hash_text, stream_text, _stream_once
from philoui.geo import get_coordinates, reverse_lookup
from philoui.authentication_v2 import AuthenticateWithKey

import json
import os
import random
# from streamlit_authenticator import Authenticate
from philoui.authentication_v2 import AuthenticateWithKey

# from pages.test_alignment import get_next_image
import streamlit_shadcn_ui as ui
import yaml
from yaml import SafeLoader

import time
import string
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase

if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()
    
    
# ============================== AUTH ===========================
with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = AuthenticateWithKey(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
fields_connect = {'Form name':'Connect', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}
fields_forge = {'Form name':'Forge access key', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}

# ===============================================================

@st.dialog('Cast your preferences')
def _submit():
    st.write('Thanks, expand below to see your data')    
    st.json(survey.data, expanded=False)

survey = CustomStreamlitSurvey('Question map')

def stream_once_then_write(text):
    text_hash = hash_text(text)
    if text_hash not in st.session_state["read_texts"]:
        stream_text(text)
        st.session_state["read_texts"].add(text_hash)
    else:
        st.markdown(text)
        

cols = st.columns(4)
db = IODatabase(conn, "discourse-data")

data = db.fetch_data()
df = pd.DataFrame(data)

item_count = len(df)

with cols[0]:
    ui.metric_card(title="Total count", content=item_count, description="Participants, so far.", key="card1")
with cols[1]:
    ui.metric_card(title="Total GAME", content="0.1 €", description="Since  _____ we start", key="card2")
with cols[2]:
    ui.metric_card(title="Pending invites", content="14", description="...", key="card3")
with cols[3]:
    st.markdown("### Questions")
    ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")
    ui.badges(badge_list=[("production", "primary")], class_name="flex gap-2", key="viz_badges3")
    



if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["username"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main', fields = fields_connect)
    st.warning('Please use your access key')
    # # try:
    # #     match = True
    # #     success, access_key, response = authenticator.register_user(data = match, captcha=True, pre_authorization=False, 
    # #                                                                 fields = fields_forge)
    # #     if success:
    # #         st.success('Registered successfully')
    # #         st.toast(f'Access key: {access_key}')
    # #         st.write(response)
    # except Exception as e:
    #     st.error(e)


with st.expander("Questions, practical philosophy", expanded=True, icon=":material/step_over:"):
    pages_total = 10
    pages = survey.pages(pages_total, 
            # on_submit=lambda: st.success("Thank you!")
            on_submit=lambda: _submit,
            )
    st.markdown("### $\mathcal{W}$elcome to the $\mathcal{Q}$uestion Map")
    st.progress(float((pages.current + 1) / pages_total))
    with pages:
        if pages.current == 0:
            stream_once_then_write('### Asking questions is a difficult business...')
            stream_once_then_write('### Questions are like problems, sometimes they do not seem to have an answer, or a solution.')
            
            # st.write(st.session_state["read_texts"])

            st.markdown("### Are you happy to go forward?")

            go_forward = survey.radio(
                "go_forward", options=["Neither Yes nor No", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )
            if go_forward == "Yes":
                st.balloons()
            elif go_forward == "No":
                st.info("Wonderful, we'll meet another time.")
            elif go_forward == "Neither Yes nor No":
                st.warning("Please, take your time to choose.")
                
        elif pages.current == 1:
            st.markdown("### Can we align?")
            stream_once_then_write("### To ensure everyone\'s travel preferences are accommodated, we need to know how you plan to get to Athens.")
            stream_once_then_write("What type of transportation do you wish to use to travel to Athens? (e.g., plane, train, bus, car)")
            options = ["Plane", "Train", "Bus", "Car", "Bike", "Other"]
            survey.multiselect("Travel modes:", options=options)
        elif pages.current == 2:
            st.markdown("### Departure Location")
            stream_once_then_write("### Knowing your departure point helps us coordinate travel logistics and support.")
            stream_once_then_write("Where will you be departing from to reach Athens?")
            location = survey.text_input("Departure location", id='departure_location', help="My departure location.")

            if location:
                coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
                with st.spinner():
                    _lookup = reverse_lookup(st.secrets.opencage["OPENCAGE_KEY"], coordinates)
                if _lookup:
                    st.write(f"Oh! We think we understand where you will be coming from: {_lookup[0][0]['annotations']['flag']}@{coordinates}")
                    # st.write(f"Coordinates: {coordinates}")
                survey.data["departure_location_coordinates"] = {"label": "departure_location_coordinates", "value": coordinates}
                
        elif pages.current == 3:
            st.markdown("### Financial Support Needs")
            stream_once_then_write("### We all have different conditions and arrangements. To provide assistance where needed, we need to know if you require financial support for the trip.")
            stream_once_then_write("Is this the case?")
            financial_support = st.radio("Financial support", horizontal=True, options=["Yes", "No"], index=1)
            if financial_support ==  "Yes":
                stream_once_then_write("Please specify the kind of support you require.")
                # travel, accommodation, or food
                options = ["Travel", "Accommodation", "Food", "Other"]
                survey.multiselect("Financial Support:", options=options, key = "kind_financial_support")
        elif pages.current == 4:
            st.markdown("### Stay Duration")
            stream_once_then_write("### To arrange and coordinate accommodations and other logistics effectively, we need to know our travel dates.")
            stream_once_then_write("What are the dates of your stay in Athens?")
            default_start = datetime(2024, 9, 24)
            default_end = default_start + timedelta(days=5)
            date_range = survey.mandatory_date_range(name = "Which days to stay in Athena?",
                                                                 label = "athena-dates", 
                                                                 id='athena-range-dates', 
                                                                 default_start=default_start, 
                                                                 default_end=default_end
                                                                 )
        elif pages.current == 5:
            st.markdown("### Accommodation Preferences")
            stream_once_then_write("### We've compiled a list of potential accommodations and want to ensure everyone's preferences are accounted for and everyone is comfortable with the options.")
            # stream_once_then_write("How much do you like each of them? (Please rate from 0 to 1.)")
            st.page_link("https://www.airbnb.com/wishlists/1557728571",
                         label="> Open accommodation options wishlist (external link)", icon="🌎")
            st.markdown("### Is there anything you liked?") 
            sentiment_mapping = ["one", "two", "three", "four", "five"]
            selected = st.feedback("faces")
            responses = [
                "Great insight! Let's move forward.",
                "Lovely, thanks for sharing! Let's take the next step.",
                "Glad to hear it! Onward to the next step.",
                "Perfect, that\'s helpful! Let's continue our journey.",
                "Thank you for feedback! Ready to proceed?"
            ]
            if selected is not None:
                random.shuffle(responses)
                st.markdown(f"{responses[selected]}")
                # st.markdown(f"You selected: {sentiment_mapping[selected]}")            
                survey.data["accommodation_feedback"] = {"label": "accommodation_feedback", "value": selected}
            
        elif pages.current == 6:
            st.markdown("### Session Participation 1/2")
            stream_once_then_write("### This may be the most difficult question today. Your opinion matters...")
            stream_once_then_write("""### to find alignment and testing a tangible way to coordinate.""")
            
            with st.spinner("Let's phrase this properly..."):
                time.sleep(3)
            txt_1 = """We\'ve been presented with the opportunity to integrate our work into a plenary session during the conference. Specifically, Ruth Wodak\'s talk on _“Coping with crises, fear, and uncertainty. Analyzing appeals to \'normality\' and \'common-sense\'_” aligns strikingly with our discussions and ideas."""
            txt_2 = """Ruth Wodak is a renowned linguist and professor, and bringing our “results” into her plenary could significantly amplify our exposure and trace. This requires enthusiasm and collaboration to connect with Ruth Wodak and the University’s Provost, Themis P. Kaniklidou, to present our ideas compellingly."""
            stream_once_then_write(txt_1)
            stream_once_then_write(txt_2)
            stream_once_then_write("#### Let's find out together whether this is a good idea...")
            st.markdown("Here are a few references, if you want to have more elements, before going _Next_:")
            st.page_link("https://en.wikipedia.org/wiki/Ruth_Wodak",
                label="> Ruth Wodak on wikipedia (external link)", icon="📣")
            st.page_link("https://www.youtube.com/results?search_query=Ruth+Wodak",
                label="> Ruth Wodak on youtube (external link)", icon="📺")
            st.page_link("https://www.youtube.com/results?search_query=Ruth+Wodak",
                label="> University\'s Provost, Themis P. Kaniklidou (external link)", icon="🎓")

        elif pages.current == 7:
            st.markdown("### Session Participation 2/2")
            txt_1 = """### $\mathcal{Q}$uestion: Do you feel confident about pursuing this opportunity, and do you think it\'s a good idea?"""
            stream_once_then_write(txt_1)
            with st.spinner("Use this new strange interface below to tell..."):
                time.sleep(5)
                stream_once_then_write("### Black or White - plus all the shades of gray.")
            executive = create_dichotomy(key = "executive", id= "executive",
                                          kwargs={'survey': survey,
                                            'label': 'resonance', 
                                            'question': 'Click to express your viewpoint: the gray area represents uncertainty, the extremes: clarity.',
                                            'gradientWidth': 50,
                                            'height': 250,
                                            'title': 'I think',
                                            'name': 'intuition',
                                            'messages': ["Yes, it's a good idea", "No, it's not a good idea", "I'm not sure"],
                                            'inverse_choice': lambda x: '',
                                            'callback': lambda x: ''}
            )
        elif pages.current == 8:
            # we have collected the data
            from lib.survey import date_decoder
            
            st.markdown("### Thank you for your participation!")
            stream_once_then_write("### _You_ have collected _your_ preferences, to be  integrated for the best _collective_ decisions.")
            current_date = datetime.now().strftime("%Y-%m-%d")
            raw_data = survey.data
            serialised_dates = [date_decoder(date_obj) for date_obj in raw_data['athena-range-dates']['value']]
            serialised_data = {**raw_data, 'athena-range-dates': serialised_dates}
            stream_once_then_write("### Below are your responses. Download them - if anything happens, they are in a safe place.")
            st.json(serialised_data, expanded=False)
            # survey.download_button("Export Survey Data", use_container_width=True)
            csv_filename = f"my_responses_question_map_1_{current_date}.data"

            if st.download_button(label=f"Download datafile", use_container_width=True, data=json.dumps(serialised_data), file_name='my_responses_question_map_1.csv', mime='text/csv', type='primary'):
            # if st.download_button(label=f"Download: {csv_filename}", use_container_width=True, data=json.dumps(serialised_data), file_name='my_responses_question_map_1.csv', mime='text/csv', type='primary'):
                st.success(f"Saved {csv_filename}")
                stream_once_then_write("The file may not be friendly to read, but it's there ;)")
                
        elif pages.current == 9:
            st.markdown("### Thank you again! ")
            stream_once_then_write("### Time now to integrate your preferences with the others.")
            stream_once_then_write("### Submit your raw preferences and let's see if we can make sense of all ours.")
            st.divider()
            stream_once_then_write("### _In the next episode..._")
            stream_once_then_write("### We will share more _general_ questions and perspectives.")
            

general = CustomStreamlitSurvey('General map')
with st.expander("Questions, general perspectives", expanded=False, icon=":material/recenter:"):
    pages_total = 10
    pages = general.pages(pages_total, 
            # on_submit=lambda: st.success("Thank you!")
            on_submit=lambda: _submit,
            )
    st.markdown("### Global Perspectives")
    st.progress(float((pages.current + 1) / pages_total))
    with pages:
        if pages.current == 0:
            stream_once_then_write('### Understanding how the collective feels about global questions can shape our discussions and presentations.')
            stream_once_then_write('### A birds\' eye view of our views can help us warm up and get ready for the journey ahead.')
            stream_once_then_write('### Please, pardon the generality of the question ^ Without going into the details, how do you feel about what\'s happening in the world today?.')
            options = ["Positive", "Neutral", "Negative", "Hopeful", "Anxious", "Indifferent", "Other"]
            general.multiselect("Feeling mode:", options=options)
        if pages.current == 1:
            stream_once_then_write('### Your energy and mood levels are important for our collaborative activities and ensuring a supportive environment.')
            stream_once_then_write('### How do you feel right now?')
            stream_once_then_write('Are you experiencing high or low energy? Are you feeling positive or negative?')

            
            col1, _, col2 = st.columns([1, .1, 1])
                
            with col1:
                st.markdown('## <center> Negative </center>', unsafe_allow_html=True)

                with stylable_container(key="play_button", css_styles="""
                {
                    [data-testid="baseButton-primary"] {
                        box-shadow: 0px 10px 14px -7px #3e7327;
                        background-image:url("data/qrcode_1.png") fixed center;
                        border-radius:4px;
                        border:1px solid #4b8f29;
                        display:inline-block;
                        cursor:pointer;
                        color:#ffffff;
                        font-family:Arial;
                        font-size:13px;
                        font-weight:bold;
                        padding:14px 31px;
                        height: 150px;
                        text-decoration:none;
                        text-shadow:0px 1px 0px #5b8a3c;
                    }
                    [data-testid="baseButton-primary"]:hover {
                        # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                        background-color:#72b352;
                        cursor: arrow;
                    }
                    [data-testid="baseButton-primary"]:active {
                        position:relative;
                        background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                        top:1px;
                    }
                }
                """,):
                    # general.button("button", type='primary', on_click=foo, use_container_width=True, key="_payment")
                    open_play = general.button("High energy / Negative", type='primary', use_container_width=True, key="play2")
                with stylable_container(key="bet_button", css_styles="""
                {
                    [data-testid="baseButton-primary"] {
                        box-shadow: 0px 10px 14px -7px #3e7327;
                        background-image:url("data/qrcode_1.png") fixed center;
                        background-color: gray;
                        border-radius:4px;
                        border:1px solid #4b8f29;
                        display:inline-block;
                        cursor:pointer;
                        color:#ffffff;
                        font-family:Arial;
                        font-size:13px;
                        font-weight:bold;
                        padding:14px 31px;
                        height: 150px;
                        text-decoration:none;
                        text-shadow:0px 1px 0px #5b8a3c;
                    }
                    [data-testid="baseButton-primary"]:hover {
                        # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                        background-color:#72b352;
                        background-color: red;
                        cursor: arrow;
                    }
                    [data-testid="baseButton-primary"]:active {
                        position:relative;
                        background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                        top:1px;
                    }
                }
                """,):
                    open_bet = general.button("Low energy / Negative", type='primary', use_container_width=True, key="bet")

                # if open_bet:
                #     modal.open(src=src_bet)

                # if open_play:
                #         modal.open(src=src_101)
                
            with col2:
                st.markdown('## <center> Positive </center>', unsafe_allow_html=True)
                with stylable_container(key="betray_button", css_styles="""
                {
                    [data-testid="baseButton-primary"] {
                        box-shadow: 0px 10px 14px -7px #3e7327;
                        border-radius:4px;
                        border:1px solid #4b8f29;
                        background-color: black;
                        display:inline-block;
                        cursor:pointer;
                        color:#ffffff;
                        font-family:Arial;
                        font-size:13px;
                        font-weight:bold;
                        padding:14px 31px;
                        height: 150px;
                        text-decoration:none;
                        text-shadow:0px 1px 0px #5b8a3c;
                    }
                    [data-testid="baseButton-primary"]:hover {
                        # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                        background-color:#72b352;
                        background-color: black;
                        cursor: arrow;
                    }
                    [data-testid="baseButton-primary"]:active {
                        position:relative;
                        background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                        top:1px;
                    }
                }
                """,):
                    open_betray = general.button("High energy / Positive", type='primary', use_container_width=True, key="betray")
                with stylable_container(key="move_button", css_styles="""
                {
                    [data-testid="baseButton-primary"] {
                        box-shadow: 0px 10px 14px -7px #3e7327;
                        border-radius:4px;
                        border:1px solid #4b8f29;
                        background-color: green;
                        display:inline-block;
                        cursor:pointer;
                        color:#ffffff;
                        font-family:Arial;
                        font-size:13px;
                        font-weight:bold;
                        padding:14px 31px;
                        height: 150px;
                        text-decoration:none;
                        text-shadow:0px 1px 0px #5b8a3c;
                    }
                    [data-testid="baseButton-primary"]:hover {
                        # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                        background-color:#72b352;
                        background-color: green;
                        cursor: arrow;
                    }
                    [data-testid="baseButton-primary"]:active {
                        position:relative;
                        background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                        top:1px;
                    }
                }
                """,):
                    open_move = general.button("Low energy / Positive", type='primary', use_container_width=True, key="move")

                if open_betray:
                    betray.open()
                    
                if open_move:
                    modal.open(src=src_100K)

