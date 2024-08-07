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

import philoui as ph
from philoui.texts import hash_text, stream_text, _stream_once

import os
import random

# from pages.test_alignment import get_next_image

import time
import string

if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

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
        

with st.expander("Questions, practical philosophy", expanded=False, icon=":material/step_over:"):
    pages_total = 10
    pages = survey.pages(pages_total, 
            # on_submit=lambda: st.success("Thank you!")
            on_submit=lambda: _submit,
            )
    st.markdown("### Welcome to the Question Map")
    st.progress(float((pages.current + 1) / pages_total))
    with pages:
        if pages.current == 0:
            stream_once_then_write('### Asking questions is a difficult business...')
            stream_once_then_write('### Questions are like problems, sometimes they do not seem to have an answer, or a solution.')
            
            st.write(st.session_state["read_texts"])

            st.markdown("### Are you happy to go forward?")

            go_forward = survey.radio(
                "go_forward", options=["Neither Yes nor No", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )
        elif pages.current == 1:
            st.markdown("### Can we align?")
            stream_once_then_write("### To ensure everyone’s travel preferences are accommodated, we need to know how you plan to get to Athens.")
            stream_once_then_write("What type of transportation do you wish to use to travel to Athens? (e.g., plane, train, bus, car)")
            options = ["Plane", "Train", "Bus", "Car", "Bike", "Other"]
            survey.multiselect("Travel modes:", options=options)
        elif pages.current == 2:
            st.markdown("### Departure Location")
            stream_once_then_write("### Knowing your departure point helps us coordinate travel logistics and support.")
            stream_once_then_write("Where will you be departing from to reach Athens?")
            survey.text_input("Departure location:")

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
            stream_once_then_write("How much do you like each of them? (Please rate from 0 to 1.)")
        elif pages.current == 6:
            st.markdown("### Session Participation")
            stream_once_then_write("### This may be the most difficult question today. We can carve an opportunity to present our results in a parallel session talk by Ruth Wodak. Your opinion matters.")
            stream_once_then_write("Do you think it is a good idea to connect and propose to present some of our results in the parallel session entitled:")
            stream_once_then_write("### _\"Coping with crises, fear, and uncertainty. Analyzing appeals to “normality” and “common-sense”\"_?")

general = CustomStreamlitSurvey('General map')
with st.expander("Questions, general perspectives", expanded=False, icon=":material/step_over:"):
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
            stream_once_then_write('### Please, pardon the generality of the question ^ Without going into the details, how do you feel about what’s happening in the world today?.')
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

