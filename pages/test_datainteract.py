import hashlib
import random
from datetime import datetime, timedelta

import streamlit as st
import yaml
from lib.authentication import _Authenticate
from streamlit_authenticator.exceptions import RegisterError
from streamlit_extras.row import row
from yaml.loader import SafeLoader
from lib.survey import CustomStreamlitSurvey
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase
import streamlit_shadcn_ui as ui
import pandas as pd
import datetime
from streamlit_extras.mandatory_date_range import date_range_picker 
import re
import json
import webcolors
import streamlit_survey as ss
import pytz


def get_human_friendly_date(updated_at_str):
    updated_at = datetime.datetime.fromisoformat(updated_at_str.replace('Z', '+00:00')).replace(tzinfo=pytz.UTC)
    delta = datetime.datetime.now(pytz.UTC) - updated_at

    if delta.days > 21:
        return 'more than 3 weeks ago, on ' + updated_at.strftime("%b %d, %Y")
    elif delta.days > 1:
        return f"{delta.days} days ago"
    elif delta.days == 1:
        return "1 day ago"
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours} hours ago"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def _display(data):
    for entry in data:
        # st.write(f"ID: {entry['id']}")
        # st.write(f"Updated At: {entry['updated_at']}")
        human_friendly_date = get_human_friendly_date(entry['updated_at'])
        st.write(f"Updated {human_friendly_date}")
        
        st.write(f"Signature: {entry['signature']}")

        # Parse the 'personal_data' field as JSON
        # personal_data = eval(entry['personal_data'])
        try:
            personal_data = json.loads(entry['personal_data'])
            # Now personal_data is safely parsed JSON data
            # Proceed to access and use personal_data safely
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            print(f"Error parsing JSON: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            
        # Extract and st.write relevant fields from 'personal_data'
        st.write(f"Name: {personal_data['name']['value']}")
        st.write(f"Email: {personal_data['email']['value']}")
        st.write(f"Phone: {personal_data['phone']['value']}")
        st.write(f"Extra Comments: {personal_data['extra']['value']}")

        # Optionally, handle additional fields like 'athena-range-dates'
        if 'athena-range-dates' in personal_data:
            st.write("Athena Range Dates:")
            for date_obj in personal_data['athena-range-dates']:
                st.write(f"- {date_obj['year']}-{date_obj['month']}-{date_obj['day']}")

        st.write("--------------------")

def _shuffle_display(data):
    names = []
    emails = []
    phones = []
    signatures = []
    comments = []
    dates = []

    for entry in data:
        # Extract common fields
        # BUG: Possible security risk in eval()
        # personal_data = eval(entry['personal_data'])
        try:
            personal_data = json.loads(entry['personal_data'])
            # Now personal_data is safely parsed JSON data
            # Proceed to access and use personal_data safely
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            print(f"Error parsing JSON: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            
        names.append(personal_data['name']['value'])
        emails.append(personal_data['email']['value'])
        phones.append(personal_data['phone']['value'])
        signatures.append(entry['signature'])

        # # Parse the 'personal_data' field as JSON
        # personal_data = eval(entry['personal_data'])

        # Extract and append comments
        comments.append(personal_data['extra']['value'])

        # # Optionally, handle additional fields like 'athena-range-dates'
        # if 'athena-range-dates' in personal_data:
        #     for date_obj in personal_data['athena-range-dates']:
        #         dates.append(f"{date_obj['year']}-{date_obj['month']}-{date_obj['day']}")
        if 'athena-range-dates' in personal_data:

            date_objs = personal_data['athena-range-dates']
            
            # Iterate through date objects two at a time to form intervals
            for i in range(0, len(date_objs), 2):
                start_date = date_objs[i]
                end_date = date_objs[i + 1] if i + 1 < len(date_objs) else None
                
                # Format dates as needed
                start_str = f"{start_date['year']}-{start_date['month']}-{start_date['day']}"
                end_str = f"{end_date['year']}-{end_date['month']}-{end_date['day']}" if end_date else ""
                
                # Construct the interval string
                if end_str:
                    date_interval = f"{start_str} to {end_str}"
                else:
                    date_interval = start_str
                
                dates.append(date_interval)
    # Display all collected information
    st.write("Names:")
    for name in names:
        st.write(f"- {name}")

    st.write("Emails:")
    for email in emails:
        st.write(f"- {email}")

    st.write("Phones:")
    for phone in phones:
        st.write(f"- {phone}")

    st.write("Signatures:")
    for signature in signatures:
        st.write(f"- {signature}")

    st.write("Comments:")
    for comment in comments:
        st.write(f"- {comment}")

    st.write("Dates:")
    for date in dates:
        st.write(f"- {date}")

    st.write("--------------------")

def main():
    _data = None
    
    db = IODatabase(conn, "discourse-data")
    col1, col2, col3 = st.columns([1, 1.2, 1])
        
    if col1.button("Fetch Data"):
        _data = db.fetch_data(kwargs={'verbose': True})
        st.json(_data, expanded=False)
    
    if _data is not None:
        with st.expander("Display Data", expanded=False):  
            _display(_data)
        with st.expander("Display Data", expanded=True):  
            _shuffle_display(_data)
    survey = CustomStreamlitSurvey()
        
    col3.download_button(
        label="Download raw",
        data=survey.to_json(),
        file_name=f'survey_{st.session_state["access_key"]}.json',
        mime='text/json',
    )
if __name__ == '__main__':
    main()