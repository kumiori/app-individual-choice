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

from typing import Callable, Dict, List, Optional

class AuthenticateWithKey(Authenticate):
    def login(self, location: str='main', max_concurrent_users: Optional[int]=None,
              max_login_attempts: Optional[int]=None, fields: Optional[Dict[str, str]]=None,
              captcha: bool=False, clear_on_submit: bool=False, key: str='Login',
              callback: Optional[Callable]=None, sleep_time: Optional[float]=None) -> tuple:
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
        if fields is None:
            fields = {'Form name':'Connect', 'Key': 'Access key', 
                      'Login':'Login', 'Captcha':'Captcha'}

        if not st.session_state['authentication_status']:
            token = self.cookie_controller.get_cookie()
            st.write(f"token: {token}")
            if token:
                self.authentication_controller.login(token=token)
            login_form = st.form('Connect')
            login_form.subheader(fields['Form name'])
            
            self.access_key = login_form.text_input('Access key').lower()
            st.session_state['access_key'] = self.access_key

            if login_form.form_submit_button('Open with key 🔑'):
                # self._check_credentials()
                if self.authentication_controller.login(username, password,
                                                        max_concurrent_users,
                                                        max_login_attempts,
                                                        callback=callback, captcha=captcha,
                                                        entered_captcha=False):
                    self.cookie_controller.set_cookie()

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['username']
    
authenticator = AuthenticateWithKey(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)



if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main')
    st.warning('Please enter your username and password')
