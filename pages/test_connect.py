import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from datetime import datetime, timedelta
from streamlit_authenticator.exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError
from streamlit_authenticator.hasher import Hasher
from lib.survey import CustomStreamlitSurvey
from lib.geo import get_coordinates
import hashlib
from lib.io import conn as supabase

import os

import yaml
from yaml.loader import SafeLoader

with open('pages/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

st.write('hashed_passwords', hashed_passwords)

st.subheader('config')
st.json(config, expanded=False)


if 'location' not in st.session_state:
    st.session_state.location = None  # Initial damage parameter

if 'coordinates' not in st.session_state:
    st.session_state.location = None  # Initial damage parameter

class _Authenticate(Authenticate):
    def __init__(self, credentials: dict, cookie_name: str, cookie_key: str, cookie_expiry_days: int, preauthorized: dict):
        super().__init__(credentials, cookie_name, cookie_key, cookie_expiry_days, preauthorized)
        self.supabase = supabase
    
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
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Connect')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Connect')

                login_form.subheader(form_name)
                
                self.access_key = login_form.text_input('Access key').lower()
                st.session_state['access_key'] = self.access_key
                # self.password = login_form.text_input('Password', type='password')

                if login_form.form_submit_button('Login'):
                    self._check_credentials()

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['username']

    def _check_credentials(self, inplace: bool=True) -> bool:
        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        inplace: bool
            Inplace setting, True: authentication status will be stored in session state, 
            False: authentication status will be returned as bool.
        Returns
        -------
        bool
            Validity of entered credentials.
        """

        if self.access_key in self.credentials['access_key']:
            try:
                if self._check_pw():
                    if inplace:
                        st.session_state['name'] = self.credentials['access_key'][self.username]['name']
                        self.exp_date = self._set_exp_date()
                        self.token = self._token_encode()
                        self.cookie_manager.set(self.cookie_name, self.token,
                            expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                        st.session_state['authentication_status'] = True
                    else:
                        return True
                else:
                    if inplace:
                        st.session_state['authentication_status'] = False
                    else:
                        return False
            except Exception as e:
                print(e)
        else:
            if inplace:
                st.session_state['authentication_status'] = False
            else:
                return False

    def register_user(self, form_name: str, location: str='main', preauthorization=True) -> bool:
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
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form('Register user')

        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        col1, _, col2 = st.columns([2, .1, 2])
        
        register_user_form.subheader(form_name)
        _location = register_user_form.text_input("location", help="")
        
        new_email = ''
        new_username = ''
        new_name = ''
        new_password = ''
        new_password_repeat = ''

        if register_user_form.form_submit_button('`Here` • `Now`'):
            if len(_location) > 0:
                coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
                if coordinates:
                    st.write(f"Coordinates for {_location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
                    st.session_state.location = _location
                    st.session_state.coordinates = coordinates
                    now = datetime.now()
                    st.write(now)   
                    # the access key is the hash of the current time (now) and the location
                    access_key_string = f"{now}_{_location}"
                    access_key_hash = hashlib.sha256(access_key_string.encode()).hexdigest()
                    st.write(access_key_hash)
                    self.__register_credentials(access_key_hash, new_name, new_password, new_email, preauthorization)
                # self._register_credentials(new_username, new_name, new_password, new_email, preauthorization)
                return True
            else:
                raise RegisterError('We forget the `where`, there...?')

    def __register_credentials(self, access_key: str, name: str, password: str, email: str, preauthorization: bool):
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
        # if not self.validator.validate_username(username):
        #     raise RegisterError('Username is not valid')
        # if not self.validator.validate_name(name):
        #     raise RegisterError('Name is not valid')
        # if not self.validator.validate_email(email):
        #     raise RegisterError('Email is not valid')
        
        existing_access_key = self.get_existing_access_key(access_key)
        
        if existing_access_key:
            st.warning("Access key already exists. Choose a different location or try again later.")
            return False
        data = {'access_key': access_key}
        response = self.supabase.table('access_keys').insert(data)
        # st.write(response)
        
    def get_existing_access_key(self, access_key):
        # Query the 'access_keys' table to check if the access key already exists
        query = self.supabase.table('access_keys').select('*').eq('key', access_key)
        response = query.execute()
        
        if response.data:
            return response.data[0]
        else:
            return None

authenticator = _Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Connect', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Disconnect', 'main', key='logout')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Do you already have an access key?')


try:
    if authenticator.register_user('Open connection', preauthorization=False):
        st.success('Connection successful!')
except Exception as e:
    st.error(e)
    
# try:
#     username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
#     st.write(username_of_forgotten_password)
#     if username_of_forgotten_password:
#         st.success('New password to be sent securely')
#         # Random password should be transferred to user securely
#     else:
#         st.error('Username not found')
# except Exception as e:
#     st.error(e)
    
st.json(config)