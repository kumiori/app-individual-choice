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

st.title("Access Key Generator")

with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

class Authenticate(_Authenticate):

    def register_multiple_users(self, form_name: str, description: None, webapp=None, preauthorization=True) -> bool:
        access_key_hash = hashlib.sha256(str(description).encode()).hexdigest()
        if self.__register_credentials(access_key_hash, webapp, preauthorization):
            self.credentials['access_key'] = access_key_hash
            return access_key_hash


    def register_user(self, form_name: str, description: None, webapp=None, preauthorization=True) -> bool:
        """
        Creates a register new user widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        location: str
            The location of the register new user form i.e. main or sidebar.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """
        if preauthorization:
            if not self.preauthorized:
                raise ValueError("preauthorization argument must not be None")

        register_user_form = st.form(form_name)

        col1, _, col2 = st.columns([2, .1, 2])
        
        register_user_form.subheader(form_name)
        self._apply_css_style()
        
        if register_user_form.form_submit_button('`Generate` • `Now`'):
            
            if webapp:
                _webapp = webapp
            else:
                _webapp = self.webapp
            
            if description:
                access_key_hash = hashlib.sha256(str(description).encode()).hexdigest()
                if self.__register_credentials(access_key_hash, _webapp, preauthorization):
                    self.credentials['access_key'] = access_key_hash
                return True
            else:
                access_key_hash = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
                if self.__register_credentials(access_key_hash, _webapp, preauthorization):
                    self.credentials['access_key'] = access_key_hash
                return True

    def _apply_css_style(self):
        # with st.container(border=False):
        st.write('<span class="custom-button"/>', unsafe_allow_html=True)

        st.write("""
        <style>
            div[data-testid="stForm"]
                button {
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
            height: 5em;
            border-radius: 4px;
            }
        </style>
        """, unsafe_allow_html=True)

    def __register_credentials(self, access_key: str, webapp: str, preauthorization: bool):
        """
        Adds to credentials dictionary the new user's information.

        Parameters
        ----------
        username: str
            The username of the new user.
        name: str
            The name of the new user.
        password: str
            The password of the new user.
        email: str
            The email of the new user.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        """

        existing_access_key = self.get_existing_access_key(access_key)
        
        if existing_access_key:
            st.write("Access key already exists. Choose a different location or try again later.")
            return False
        
        data = {'key': access_key, 'webapp': webapp}
        response = self.supabase.table('access_keys').insert(data).execute()
        st.write(data, response)
        if response:
            return True

if "key_description" not in st.session_state:
    st.session_state['key_description'] = ""

if "domain_name" not in st.session_state:
    st.session_state['domain_name'] = ""

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['cookie']['expiry_minutes'],
    config['preauthorized'],
    webapp = 'discourse-authors'
)



# Input fields for domain name and description
domain_name = st.text_input("Enter Domain Name (webapp):")
description = st.text_input("Enter Description:")

st.session_state['domain_name'] = domain_name
st.session_state['key_description'] = description

try:
    if authenticator.register_user(' Generate • One ', description = description, webapp=domain_name,  preauthorization=False):
        st.success(f'Very good 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
            💨 Here is one for your access ✨ <`{ authenticator.credentials["access_key"] }`> ✨.        \
            Keep it in your pocket, add it to your wallet...keep it safe 💭. You will use it to access to the authors mainframe 💫 at the top of the page.')
except Exception as e:
    st.error(e)


st.title("Several Keys Generator")

st.write(st.session_state['key_description'])
num_keys = st.number_input("Enter the number of keys to generate:", min_value=1, value=1, step=1)
# Dictionary to store domain names and descriptions for each key
key_info = {}

# Loop to display input fields for domain name and description based on the number of keys
for i in range(num_keys):
    st.write(f"Key {i+1}")
    col1, _, col2 = st.columns([1, .3, 1])
    _domain_name = col1.text_input(f"Enter Domain Name (webapp) for Key {i+1}:", value=st.session_state['domain_name'])
    _description = col2.text_input(f"Enter _Description for Key {i+1}:", value=f"{st.session_state['key_description']}_{i}")
    st.divider()

    key_info[f"Key {i+1}"] = {"Domain Name": _domain_name, "Description": _description}

if st.button("Generate Keys"):
    try:
        for key, info in key_info.items():
            st.write(info["Description"], info["Domain Name"])
            if authenticator.register_multiple_users(' Check • Point ', description=info["Description"], webapp=info["Domain Name"], preauthorization=False):
                st.success(f'Very good 🎊.  🗝️ & ✨ <`{authenticator.credentials["access_key"]}, {info["Description"]}, {info["Domain Name"]}`> ✨')
    except Exception as e:
        st.error(e)