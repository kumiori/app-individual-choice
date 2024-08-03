import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from datetime import datetime, timedelta

import os

import yaml
from yaml.loader import SafeLoader

with open('pages/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

st.write('hashed_passwords', hashed_passwords)

st.subheader('config')
st.json(config, expanded=False)

st.markdown("## Custom authentication")

with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
st.json(config)
# with open('pages/credentials.yml') as file:
#     config = yaml.load(file, Loader=SafeLoader)
# st.json(config)
    
class AuthenticateWithKeys(Authenticate):

    def login(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            Username of the authenticated user.
        """
        if not st.session_state['authentication_status']:
            token = self.cookie_controller.get_cookie()
            st.write(f"token: {token}")
            if token:
                self.authentication_controller.login(token=token)
            login_form = st.form('Connect')
            login_form.subheader(form_name)
            
            self.username = login_form.text_input('Username').lower()
            st.session_state['username'] = self.username
            self.password = login_form.text_input('Password', type='password')

            if login_form.form_submit_button('Login'):
                self._check_credentials()

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['username']
    
authenticator = AuthenticateWithKeys(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


authenticator.login('Connect', 'main')
