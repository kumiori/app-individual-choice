import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from lib.io import conn as auth_database

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
from streamlit_authenticator.controllers import AuthenticationController, CookieController

from streamlit_authenticator.models import AuthenticationModel
from streamlit_authenticator.utilities import Validator

class _AuthenticationModel(AuthenticationModel):
    def __init__(self, credentials: dict, pre_authorized: Optional[List[str]]=None,
                 validator: Optional[Validator]=None, auto_hash: bool=True):
        self.credentials = credentials
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
        if 'name' not in st.session_state:
            st.session_state['name'] = None
        self.credentials['usernames'] = {}
        self.auth_database = auth_database
        st.toast('Initialised authentication model')
        
    def login(self, username: str, password: str, max_concurrent_users: Optional[int]=None,
              max_login_attempts: Optional[int]=None, token: Optional[Dict[str, str]]=None,
              callback: Optional[Callable]=None) -> bool:
        # st.toast('Initialised login logic')
        
        if username:
            st.toast(f'username: {username}')
            if self.check_credentials(username, password, max_concurrent_users, max_login_attempts):
                st.session_state['username'] = username
                st.session_state['authentication_status'] = True
                # self._record_failed_login_attempts(username, reset=True)
                # self.credentials['usernames'][username]['logged_in'] = True
                if callback:
                    callback({'username': username})
                return True
            st.info('Incorrect credentials')
            st.session_state['authentication_status'] = False
            return False
        if token:
            if not token['username'] in self.credentials['usernames']:
                st.info('User not authorized')
                # raise LoginError('User not authorized')
            st.session_state['username'] = token['username']
            st.session_state['name'] = self.credentials['usernames'][token['username']]['name']
            st.session_state['authentication_status'] = True
            self.credentials['usernames'][token['username']]['logged_in'] = True
        return None

    def check_credentials(self, username: str, password: str,
                          max_concurrent_users: Optional[int]=None,
                          max_login_attempts: Optional[int]=None) -> bool:
        st.write(self.credentials)
        try:
            if self._valid_access_key(username):
                return True
        except Exception as e:
            st.error(e)
        return None

    def _valid_access_key(self, access_key):
        # Query the 'access_keys' table to check if the access key already exists
        query = self.auth_database.table('access_keys').select('*').eq('key', access_key)
        response = query.execute()
        
        if response.data:
            st.info('Access key exists')
            return response.data[0]
        else:
            return None
class _AuthenticationController(AuthenticationController):
    def __init__(self, credentials: dict, pre_authorized: Optional[List[str]]=None,
                 validator: Optional[Validator]=None, auto_hash: bool=True):

        """
        Create a new instance of "AuthenticationController".

        Parameters
        ----------
        credentials: dict
            Dictionary of usernames, names, passwords, emails, and other user data.
        pre-authorized: list, optional
            List of emails of unregistered users who are authorized to register.        
        validator: Validator, optional
            Validator object that checks the validity of the username, name, and email fields.
        auto_hash: bool
            Automatic hashing requirement for the passwords, 
            True: plain text passwords will be automatically hashed,
            False: plain text passwords will not be automatically hashed.
        """
        self.authentication_model = _AuthenticationModel(credentials,
                                                        pre_authorized,
                                                        validator,
                                                        auto_hash)
        self.validator = Validator()

class AuthenticateWithKey(Authenticate):
    def __init__(self, credentials: dict, cookie_name: str, cookie_key: str,
                 cookie_expiry_days: float=30.0, pre_authorized: Optional[List[str]]=None,
                 validator: Optional[Validator]=None, auto_hash: bool=True):
        self.cookie_controller  =   CookieController(cookie_name,
                                                     cookie_key,
                                                     cookie_expiry_days)
        self.authentication_controller  =   _AuthenticationController(credentials,
                                                                     pre_authorized,
                                                                     validator,
                                                                     auto_hash)

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
            
            access_key = login_form.text_input('Access key').lower()
            st.session_state['access_key'] = access_key

            if login_form.form_submit_button('Open with key 🔑'):
                # self._check_credentials()
                if self.authentication_controller.login(access_key, '',
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
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main')
    st.warning('Please use your access key')
