import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from lib.io import conn as auth_database
import hashlib
import random
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
from streamlit_authenticator.utilities import Helpers, Validator, RegisterError

class _AuthenticationModel(AuthenticationModel):
    def __init__(self, credentials: dict, pre_authorized: Optional[List[str]]=None,
                 validator: Optional[Validator]=None, auto_hash: bool=True):
        self.credentials = credentials
        self.participants = {}
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
            st.toast(f'Access key: {username}')
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
            st.write(f"token: {token}")
            # if not token['username'] in self.credentials['usernames']:
            if not self._valid_access_key(token['username']):
                st.info('User not authorized')
                # raise LoginError('User not authorized')
            st.session_state['username'] = token['username']
            # st.session_state['name'] = self.credentials['usernames'][token['username']]['name']
            st.session_state['authentication_status'] = True
            # self.credentials['usernames'][token['username']]['logged_in'] = True
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
            return response.data[0]
        else:
            return None

    def _access_key_exists(self, access_key: str) -> bool:
        return self._valid_access_key(access_key)
    
    def logout(self):
        """
        Clears the cookie and session state variables associated with the logged in user.
        """
        # self.credentials['usernames'][st.session_state['username']]['logged_in'] = False
        st.session_state['logout'] = True
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.session_state['authentication_status'] = None
    def register_user(self, access_key: str, pre_authorization: bool,
                      callback: Optional[Callable]=None) -> tuple:
        if callback:
            callback({'access_key': access_key})
        self._register_credentials(access_key)

    def _register_credentials(self, access_key: str):
        existing_access_key = self._access_key_exists(access_key)
        st.toast(f'Existing access key: {existing_access_key}')
        if existing_access_key:
            return False
        
        data = {'key': access_key}
        response = self.auth_database.table('access_keys').insert(data).execute()
        # st.write(data, response)
        if response:
            return True


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

    def register_user(self, access_key: str, pre_authorization: bool,
                      domains: Optional[List[str]]=None, callback: Optional[Callable]=None,
                      captcha: bool=False, entered_captcha: Optional[str]=None, webapp: Optional[List[str]]=None) -> tuple:
        if captcha:
            if not entered_captcha:
                raise RegisterError('Captcha not entered')
            entered_captcha = entered_captcha.strip()
            self._check_captcha('register_user_captcha', RegisterError, entered_captcha)
        return self.authentication_model.register_user(access_key, pre_authorization,
                                                       callback)
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
    def register_user(self, data = True, pre_authorization: bool=True,
                      domains: Optional[List[str]]=None, fields: Optional[Dict[str, str]]=None,
                      captcha: bool=True, clear_on_submit: bool=False, key: str='Register user',
                      callback: Optional[Callable]=None) -> tuple:
        """
        Creates a register new user widget.

        Parameters
        ----------
        location: str
            Location of the register new user widget i.e. main or sidebar.
        pre-authorization: bool
            Pre-authorization requirement, 
            True: user must be pre-authorized to register, 
            False: any user can register.
        domains: list, optional
            Required list of domains a new email must belong to i.e. ['gmail.com', 'yahoo.com'], 
            list: required list of domains, 
            None: any domain is allowed.
        fields: dict, optional
            Rendered names of the fields/buttons.
        captcha: bool
            Captcha requirement for the register user widget, 
            True: captcha required,
            False: captcha removed.
        clear_on_submit: bool
            Clear on submit setting, 
            True: clears inputs on submit, 
            False: keeps inputs on submit.
        key: str
            Unique key provided to widget to avoid duplicate WidgetID errors.
        callback: callable, optional
            Optional callback function that will be invoked on form submission.

        Returns
        -------
        str
            Email associated with the new user.
        str
            Username associated with the new user.
        str
            Name associated with the new user.
        """
        if fields is None:
            fields = {'Form name':'Register user', 'Email':'Email', 'Username':'Username',
                      'Password':'Password', 'Repeat password':'Repeat password',
                      'Register':'Register', 'Captcha':'Captcha'}

        register_user_form = st.form(key=key, clear_on_submit=clear_on_submit)
        register_user_form.subheader('Register user' if 'Form name' not in fields
                                     else fields['Form name'])

        entered_captcha = None
        if captcha:
            entered_captcha = register_user_form.text_input('Captcha' if 'Captcha' not in fields
                                                            else fields['Captcha']).strip()
            register_user_form.image(Helpers.generate_captcha('register_user_captcha'))

        access_key_hash = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
        st.toast(f'Created access key: {access_key_hash}, waiting for participant to authorise')
        if register_user_form.form_submit_button('`Here` • `Now`' if 'Register' not in fields
                                                 else fields['Register']):
            return self.authentication_controller.register_user(access_key_hash,
                                                                pre_authorization, domains,
                                                                callback, captcha, entered_captcha)
        return None, None, None
authenticator = AuthenticateWithKey(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["username"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main')
    st.warning('Please use your access key')
    try:
        match = True
        fields = {'Form name':'Register user', 'Email':'Email', 'Username':'Username',
                  'Password':'Password', 'Repeat password':'Repeat password',
                  'Register':' Here • Now ', 'Captcha':'Captcha'}
        authenticator.register_user(data = match, captcha=False, pre_authorization=False, fields = fields)
            # st.success(f'Very good 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
            #     💨 Here is one for your access ✨ <` `> ✨.        \
            #     Keep it in your pocket, add it to your wallet...keep it safe 💭. You will use it to access to the authors mainframe 💫 at the top of the page.')
    except Exception as e:
        st.error(e)
