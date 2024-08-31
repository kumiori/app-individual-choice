import streamlit as st
import numpy as np
import streamlit_survey as ss
from lib.survey import CustomStreamlitSurvey
from lib.io import (
    create_button,
    create_checkbox,
    create_dichotomy,
    create_equaliser,
    create_equaliser,
    create_globe,
    create_next,
    create_qualitative,
    create_textinput,
    create_yesno,
    create_yesno_row,
    fetch_and_display_data,
    conn,
)
from streamlit_elements import elements, mui, nivo
from pathlib import Path

# from lib.texts import stream_text, _stream_once
from datetime import datetime, timedelta
from streamlit_extras.stateful_button import button as stateful_button
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import philoui as ph
from philoui.texts import hash_text, stream_text, _stream_once
from philoui.geo import get_coordinates, reverse_lookup
from philoui.authentication_v2 import AuthenticateWithKey

# from philoui.io import check_existence
from philoui.survey import date_decoder

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

if "read_texts" not in st.session_state:
    st.session_state.read_texts = set()

if "serialised_data" not in st.session_state:
    st.session_state.serialised_data = {}


# ============================== AUTH ===========================
with open("data/credentials.yml") as file:
    config = yaml.load(file, Loader=SafeLoader)

config["credentials"]["webapp"] = "blur"
config["cookie"]["key"] = "blur_cookie"
config["cookie"]["name"] = "blur_cookie"
config["credentials"]["usernames"] = {}

st.write(config)

authenticator = AuthenticateWithKey(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)
fields_connect = {
    "Form name": "Connect",
    "Email": "Email",
    "Username": "Username",
    "Password": "Password",
    "Repeat password": "Repeat password",
    "Register": " Here • Now ",
    "Captcha": "Captcha",
}
fields_forge = {
    "Form name": "Forge access key",
    "Email": "Email",
    "Username": "Username",
    "Password": "Password",
    "Repeat password": "Repeat password",
    "Register": " Here • Now ",
    "Captcha": "Captcha",
}

# ===============================================================

# db = IODatabase(conn, "blur-data")

cols = st.columns(4, vertical_alignment="bottom")
# data = db.fetch_data()
# df = pd.DataFrame(data)

# mock pandas dataframe
df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4],
        "B": [10, 20, 30, 40],
        "C": [100, 200, 300, 400],
    }
)

item_count = len(df)

with cols[0]:
    ui.metric_card(title="Total count", content=item_count, description="Participants, so far.", key="card1")
with cols[1]:
    ui.metric_card(title="Total GAME", content="0.1 €", description="Since  _____ we start", key="card2")
with cols[2]:
    ui.metric_card(title="Pending invites", content="10k", description="...", key="card3")
with cols[3]:
    st.markdown("### Join the waitlist")
    ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")
    ui.badges(badge_list=[("production", "primary")], class_name="flex gap-2", key="viz_badges3")

intro_text = """
Can you navigate a post-apocalyptic world where society has collapsed? This is a question of being part of a group rebuilding it from the ruins. 

Your environment is a mix of decayed urban landscapes, overgrown nature, and remnants of old institutions. Will collective life go on? This is for all to figure out. But how?

Encounters are scenarios where you must make decisions that shape the future of this new world.

How is everything connected? Can you read signs? Can you make sense of _this_ chaos? You will find the way to a new beginning.
"""

if st.session_state['authentication_status'] is None:
    st.markdown("### <center>Convergence or collapse, chaos or renaissance?</center>", unsafe_allow_html=True)
    
    cols = st.columns([1,3,1])
    with cols[1]:
        st.markdown(intro_text)

    
    # with elements("nivo_charts"):
    #         # Third element of the dashboard, the Media player.
    #     st.markdown("### Presence forecast in Athens")
    #     with mui.Box(sx={"height": 300}):
    #         nivo.Bump(
    #             data=json.loads(Path('data/presence_data.json').read_text()),
    #             colors={ "scheme": "nivo" },
    #             lineWidth=7,
    #             width=700,
    #             height=300,
    #             activeLineWidth=6,
    #             inactiveLineWidth=3,
    #             inactiveOpacity=0.15,
    #             pointSize=10,
    #             activePointSize=16,
    #             inactivePointSize=0,
    #             pointColor={ "theme": "background" },
    #             pointBorderWidth=3,
    #             activePointBorderWidth=3,
    #             pointBorderColor={ "from": "serie.color" },
    #             axisTop=None,
    #             enableGridX=False,
    #             enableGridY=False,
    #             axisBottom={
    #                 "tickSize": 5,
    #                 "tickPadding": 5,
    #                 "tickRotation": 0,
    #                 "legend": "Days in Athens",
    #                 "legendPosition": "middle",
    #                 "legendOffset": 32,
    #                 "tickValues": ["2024-09-24", "2024-09-26", "2024-09-28", "2024-10-01"],

    #             },
    #             axisLeft={
    #                 "tickSize": 5,
    #                 "tickPadding": 5,
    #                 "tickRotation": 0,
    #                 "legend": "missing",
    #                 "legendPosition": "middle",
    #                 "legendOffset": -40
    #             },
    #             margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
    #             axisRight=None,
    #             # tooltip=custom_tooltip,
    #         )
            
    with elements("nivo_chord"):
        # st.markdown("### Chord")
        DATA = json.loads(Path('data/chord_data.json').read_text())
        
        with mui.Box(sx={"height": 400}, key="chord_presence"):
            nivo.Chord(
                data=DATA,
                colors={ "scheme": "greys" },
                keys=[ 'The People', 'A New Leader', 'Survival', 'Technology', 'Nature' ],
                margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                theme={
                    "tooltip": {
                        "container": {
                            "background": "white",
                            "color": "black",
                            "fontSize": "14px",
                            "boxShadow": "0 1px 2px rgba(0, 0, 0, 0.1)",
                            "borderRadius": "4px",
                        },
                    }
                    },
            )
