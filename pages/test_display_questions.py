import streamlit as st
if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Questions and Perspectives",
        page_icon="👋",
        initial_sidebar_state="collapsed"
    )
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        [data-testid="stHeader"] {
            display: none
            }
    </style>
    """,
        unsafe_allow_html=True,
    )
import matplotlib.pyplot as plt
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
from philoui.survey import create_flag_ui
# from philoui.io import check_existence
from philoui.survey import date_decoder
from collections import defaultdict

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
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()
    
if 'serialised_data' not in st.session_state:
    st.session_state.serialised_data = {}
    

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


db = IODatabase(conn, "discourse-data")

def extend_date_range(date_counts, days_before=3, days_after=5):
    # Convert string dates to datetime objects for manipulation
    date_keys = [datetime.strptime(date, "%Y-%m-%d") for date in date_counts.keys()]
    min_date = min(date_keys)
    max_date = max(date_keys)

    # Create a new dictionary to store the extended dates
    extended_dates = {}

    # Add the days before the minimum date
    for x in range(1, days_before + 1):
        new_date = min_date - timedelta(days=x)
        extended_dates[new_date] = 0

    # Add the original date counts
    for date, count in date_counts.items():
        extended_dates[datetime.strptime(date, "%Y-%m-%d")] = count

    # Add the days after the maximum date
    for x in range(1, days_after + 1):
        new_date = max_date + timedelta(days=x)
        extended_dates[new_date] = 0

    # Convert the extended dates back to strings for the nivo bump chart
    extended_date_counts = {date.strftime("%Y-%m-%d"): count for date, count in extended_dates.items()}

    # Sort the dictionary by date
    extended_date_counts = dict(sorted(extended_date_counts.items()))

    return extended_date_counts

def fetch_and_display_personal_data(conn, kwargs):
    # Fetch all data from the "questionnaire" table
    table_name = kwargs.get('database')
    signature = kwargs.get('key')
    
    if 'path' in kwargs:
        path = kwargs.get('path')
        st.write(f"Fetching {path} data from the {table_name} table.")
        response = conn.table(table_name).select(path).eq('signature', signature).execute()
        updated_at = conn.table(table_name).select("updated_at").eq('signature', signature).execute()
    else:
        st.write(f"Fetching all data from the {table_name} table.")
        response = conn.table(table_name).select("*").eq('signature', signature).execute()

    # Check if there is any data in the response
    if response and response.data:
        data = response.data
        _data = []
        # Display the dataset
        # for item in data:
            # st.write(f"ID: {item['id']}")
            # updated_at = datetime.fromisoformat(item['updated_at'][:-6])
            # st.write(f"Preferences updated at: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            # st.write(f"Updated At: {item['updated_at']}")
            # st.write(data)
            # st.write(f"Signature: {item['signature']}")

            # # Parse and display personal data
            # personal_data = json.loads(item['personal_data'])
            # st.write("Personal Data:")
            # for key, value in personal_data.items():
            #     if key == "athena-range-dates":
            #         continue  # Skip displaying this key-value pair
            #     if isinstance(value, dict):
            #         st.write(f"- {key}: {value['value']}")
            #     else:
            #         st.write(f"- {key}: {value}")

            # # Convert and display datetime objects
            # if 'athena-range-dates' in personal_data:
            #     st.write("Athena stay - range dates:")
            #     for date_obj in personal_data['athena-range-dates']:
            #         date = datetime.datetime(date_obj['year'], date_obj['month'], date_obj['day'])
            #         st.write(date.strftime("%Y-%m-%d"))

            # # st.write("Path 001:", item['path_001'])
            # st.write("Created At:", item['created_at'])
    else:
        st.write(f"No data found in the {table_name} table.")
    return data

signature = st.session_state["username"]

intro_text = """
"""

if st.session_state['authentication_status'] is None:
    st.markdown("### Towards our conference in Athens _Europe in Discourse_")
    
    cols = st.columns([1,3,1])
    with cols[1]:
        st.markdown(intro_text)

if st.session_state['authentication_status']:
    st.toast('Initialised authentication model')
    authenticator.logout()
    st.write(f'`Your signature is {st.session_state["username"][0:4]}***{st.session_state["username"][-4:]}`')

    dataset = fetch_and_display_personal_data(conn, 
                                    {'database': 'discourse-data',
                                        'key': signature,
                                        'index': 'signature',
                                        'path': "practical_questions_01"})
    st.write(dataset)
    
    # Parse the JSON object within the dataset
    practical_questions = json.loads(dataset[0]["practical_questions_01"])

    from datetime import date
    # Extract values
    departure = practical_questions["departure_location"]["value"]
    travel_modes = ', '.join(practical_questions["Travel modes:"]["value"])
    date_from = date(practical_questions["athena-range-dates"][0]["year"], practical_questions["athena-range-dates"][0]["month"], practical_questions["athena-range-dates"][0]["day"]).strftime("%B %d, %Y")
    date_to = date(practical_questions["athena-range-dates"][1]["year"], practical_questions["athena-range-dates"][1]["month"], practical_questions["athena-range-dates"][1]["day"]).strftime("%B %d, %Y")
    resonance = float(practical_questions["executive"]["value"])
    financial_support = practical_questions["Financial support"]["value"]
    financial_details = ', '.join(practical_questions["Financial details"]["value"])
    accommodation_feedback = practical_questions["accommodation_feedback"]["value"]
    liking = ["despise", "dislike", "am neutral with respect to", "like", "love"]
    # Map resonance value to corresponding text
    if resonance == 0:
        resonance_text = "yes, it's a good idea"
    elif resonance == 1:
        resonance_text = "no, it's not a good idea"
    elif 0 < resonance <= 0.5:
        resonance_text = "kinda good"
    else:
        resonance_text = "could be better"

    go_forward = practical_questions["go_forward"]["value"] == "Yes"

    # Generate the discursive text
    discursive_text = (
        f"Hello _Fellows_, I am planning to join the Athens conference departing from `{departure}` and using `{str.lower(travel_modes)}`, staying in Athens from `{date_from}` to `{date_to}`. During my stay, `I {'' if financial_support == 'Yes' else 'do not'} wish` for financial support, which includes `{financial_details}`. I `{liking[accommodation_feedback]}` the proposed accommodations (with a rating of `{accommodation_feedback} out of 5`). Finally, `{resonance_text}` to connect to the plenary session. I `am {'' if go_forward else 'not '}happy` to go forward."
    )

    st.write(discursive_text)    
    st.write(f'`My signature is {st.session_state["username"][0:4]}***{st.session_state["username"][-4:]}`')
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    if col1.button("Fetch all data"):
        # data = db.fetch_data(kwargs={'verbose': True})
        # data = conn.table('discourse-data').select("*").execute()
        response = conn.table('discourse-data').select('signature', 'updated_at', 'personal_data', 'practical_questions_01').execute()

        athena_dates = []

        if response and response.data:
            data = response.data
            for entry in data:
                # st.write(entry['signature'])

                for key in ['personal_data', 'practical_questions_01']:
                    if entry[key]:
                        parsed_data = json.loads(entry[key])
                        if "athena-range-dates" in parsed_data:
                            # st.write(parsed_data["athena-range-dates"])
                            athena_dates.append(
                                {'signature': entry['signature'], 'dates': parsed_data["athena-range-dates"]})
                
                # if entry['practical_questions_01'] is not None:
                #     practical_questions = json.loads(entry['practical_questions_01'])

                # else:
                    # practical_questions = None
                # st.write(practical_questions)
                # st.write(entry['practical_questions_01']["go_forward"]["value"])
            # st.write(athena_dates)
            st.json(data, expanded=False)
            date_ranges = []
            for entry in athena_dates:
                start_date = date(entry['dates'][0]['year'], entry['dates'][0]['month'], entry['dates'][0]['day'])
                end_date = date(entry['dates'][1]['year'], entry['dates'][1]['month'], entry['dates'][1]['day'])
                date_ranges.append((start_date, end_date, entry['signature']))

            # Plot the date ranges
            # plt.figure(figsize=(10, 6))

            # for i, (start_date, end_date, signature) in enumerate(date_ranges):
            #     plt.plot([start_date, end_date], [i, i], marker='o', label=signature)

            # plt.yticks(range(len(date_ranges)), [signature for _, _, signature in date_ranges])
            # plt.xlabel('Date')
            # plt.ylabel('Signatures')
            # plt.title('Athena Date Ranges')
            # plt.grid(True)
            # plt.legend()
            # plt.show()
    
    
            date_counts = defaultdict(int)
            for entry in athena_dates:
                start_date = date(entry['dates'][0]['year'], entry['dates'][0]['month'], entry['dates'][0]['day'])
                end_date = date(entry['dates'][1]['year'], entry['dates'][1]['month'], entry['dates'][1]['day'])

                current_date = start_date
                while current_date <= end_date:
                    date_counts[current_date.isoformat()] += 1
                    current_date = current_date.fromordinal(current_date.toordinal() + 1)

            # Step 2: Calculate cumulative presence
            cumulative_counts = []
            sorted_dates = sorted(date_counts.keys())
            # print(sorted_dates)
            # st.write("sorted dates")
            # st.write(sorted_dates)
            # st.write("date counts")
            # st.write(date_counts)
            sorted_date_counts = dict(sorted(date_counts.items()))
            # st.write('sorted_date_counts')
            # st.write(sorted_date_counts)
            max_y = 17
            cumulative_sum = 0
            extended_counts = extend_date_range(date_counts, days_before=3, days_after=5)
            
            for d in extended_counts:
                # cumulative_sum += date_counts[d]
                cumulative_counts.append({"x": d, "y": max_y - extended_counts[d]})

            # Step 3: Format for Nivo Bump Chart

            nivo_bump_data = [{"id": "presence", "data": cumulative_counts}]
            # st.write(nivo_bump_data)
            
            
            with elements("nivo_charts"):
                    # Third element of the dashboard, the Media player.
                with mui.Box(sx={"height": 500}):
                        nivo.Bump(
                            data=nivo_bump_data,
                            colors={ "scheme": "spectral" },
                            lineWidth=3,
                            width=500,
                            height=300,
                            activeLineWidth=6,
                            inactiveLineWidth=3,
                            inactiveOpacity=0.15,
                            pointSize=10,
                            activePointSize=16,
                            inactivePointSize=0,
                            pointColor={ "theme": "background" },
                            pointBorderWidth=3,
                            activePointBorderWidth=3,
                            pointBorderColor={ "from": "serie.color" },
                            axisTop={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "",
                                "legendPosition": "middle",
                                "legendOffset": -36
                            },
                            axisBottom={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "",
                                "legendPosition": "middle",
                                "legendOffset": 32
                            },
                            axisLeft={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "ranking",
                                "legendPosition": "middle",
                                "legendOffset": -40
                            },
                            margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                            axisRight=None,
                        )
   
            
            
            
            
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main', fields = fields_connect)
    st.warning('Please use your access key')
    
