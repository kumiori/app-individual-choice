import streamlit as st

if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Test - Stability",
        page_icon="✨",
        # layout="wide",
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

st.write(st.secrets["runtime"]["STATUS"])

# Standard library imports
import datetime
from datetime import datetime, timedelta
import hashlib
import random
import string
import time

# Third-party imports
import numpy as np
import json
import pandas as pd
import streamlit_survey as ss
from streamlit_authenticator.exceptions import RegisterError
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
from streamlit_extras.streaming_write import write as streamwrite
import yaml
from yaml.loader import SafeLoader

# Local application/library-specific imports
from lib.authentication import _Authenticate
from lib.dictionary_manip import display_dictionary, display_dictionary_by_indices, display_details_description
from lib.geo import reverse_lookup, get_coordinates
from lib.io import (
    create_button, create_checkbox, create_dichotomy, create_equaliser, create_equaliser,
    create_globe, create_next, create_qualitative, create_textinput,
    create_yesno, create_yesno_row, fetch_and_display_data, conn
)
from lib.matrices import generate_random_matrix, encode_matrix, display_matrix
from lib.presentation import PagedContainer
from lib.survey import CustomStreamlitSurvey
from lib.texts import (
    _stream_example, corrupt_string, friendly_time, match_input
)
from pages.test_geocage import get_coordinates

# Constants
update_frequency = 500  # in milliseconds

if "access_key" not in st.session_state:
    st.session_state['access_key'] = ''
    

with open('data/stability_credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
class Authenticate(_Authenticate):
    def __register_credentials(self, access_key: str, data: dict, preauthorization: bool):
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
    

        existing_access_key = self.get_existing_access_key(access_key)
        
        if existing_access_key:
            st.write("Access key already exists. Choose a different location or try again later.")
            return False
        
        # data['access_key'] = access_key
        _data = {'key': access_key}
        response = self.supabase.table('access_keys').insert(_data).execute()
        # st.write(data, response)
        if response:
            return True
        
    def register_user(self, form_name: str,
                      data: {}, preauthorization=True) -> bool:
        """
        Creates a register new user widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        data: dictionary
            The data of the new user
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
        if not data:
            raise ValueError("Data must be'")
        register_user_form = st.form('OpenConnection')

        col1, _, col2 = st.columns([2, .1, 2])
        
        register_user_form.subheader(form_name)

        new_email = ''
        new_username = ''
        new_name = ''
        new_password = ''
        new_password_repeat = ''
        
        if not self.validator.validate_email(data.get('# email')['value']):
            raise RegisterError('The email doesn\'t look valid. Please, go back and insert a valid email.')
        
        if register_user_form.form_submit_button('`Integrate` • `Data`', use_container_width=True):
            now = datetime.now()
            # st.write(now) 
            location = data.get('location')['value']
            if len(location) > 0:
                # coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
                if st.session_state.coordinates:
                    # st.write(f"Coordinates for {location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
                    # st.session_state.location = location
                    # st.session_state.coordinates = coordinates
                    # the access key is the hash of the current time (now) and the location
                    data_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
                    access_key_string = f"{now}_{location}_{data_hash}"
                    st.info('TX: 000' + access_key_string)
                    access_key_hash = hashlib.md5(access_key_string.encode()).hexdigest()
                    # st.write(access_key_hash)
                    if self.__register_credentials(access_key_hash, self.webapp, preauthorization):
                        self.credentials['access_key'] = access_key_hash
                return True
            else:
                raise RegisterError('We forget the `where`. Please, go back to insert your location.')

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
            st.warning("Access key already exists. Choose a different location or try again later.")
            return False
        
        data = {'key': access_key, 'webapp': webapp}
        response = self.supabase.table('access_keys').insert(data).execute()
        # st.write(data, response)
        if response:
            return True

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    0,
    config['preauthorized'],
    webapp = 'stability-gathering'
)
            
survey = CustomStreamlitSurvey()


if 'done_reading' not in st.session_state:
    st.session_state.done_reading = set()

if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0

if "min_page" not in st.session_state:
    st.session_state["min_page"] = 0


if 'no_clicked' not in st.session_state:
    st.session_state["no_clicked"] = False

def no_clicked():
    st.session_state.no_clicked = True


def create_connection(key, kwargs = {}):
    authenticator = kwargs.get('authenticator')
    survey = kwargs.get('survey')
    _location = survey.data['location']['value']
    if not survey.data['location']['value']:
        st.warning('Please, go back and enter your location to continue.')
    with st.expander('Your data'):
        st.json(survey.data, expanded=True)
    
    if st.session_state["authentication_status"] is None:
        try:
            if authenticator.register_user(' Check • Point ', data = survey.data,  preauthorization=False):
                st.success(f'Very good 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
                    💨 Here is one for your access ✨')
                st.markdown(f"## <{ authenticator.credentials['access_key'] }>")
                add_vertical_space(13)
        except Exception as e:
            st.error(e)
            
    else:
    # if st.session_state["authentication_status"] is True:
        st.info(f"Connected, entering using your key. AUTHENTICATION STATUS: {st.session_state['authentication_status']}")
        

def create_access(key, kwargs = {}):
    
    MILESTONE_KEY_CHAPTER = 0
    
    if st.session_state.current_page >= MILESTONE_KEY_CHAPTER:
        authenticator.login('Do you already have a key?')

    pass

def enter_location(label):
    if survey.data.get(label):
        location = survey.data.get(label)["value"]
        st.session_state.location = location
    else:
        return
    coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
    if coordinates:
        # st.info(f"Coordinates for {location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
        st.session_state.location = location
        st.session_state.coordinates = coordinates

intro_text = """
## How can international cooperation be effective?
## Our questions are simple. This is why we connect.


### Today, the scale of the challenges that enter into our awareness questions traditional schemes of international cooperation. 

# `This is your access token:` :checkered_flag: `{access_key}`

### (if empty, it has to be generated)
""".format(access_key=st.session_state.access_key)

location_text = """
## Enter your location to continue.
### {location}
### We will use this information to harmonise timezones.

""".format(location=st.session_state.get("location", "No location entered."))

profile = [
    ("Analysis", ""),
    ("Mechanics", ""),
    ("Experiments", ""),
    ("Numerics", ""),
    ("Other", ""),
]
profile_dimensions = [item[0] for item in profile[0:5]]

try:
    default_values = [survey.data[label]['value'] for label in profile_dimensions]
except:
    default_values = [0 for _ in range(5)]

profile_text = """
## Understood, you connect from {location}.
## Let's triangulate our profiles.
### We will use this data just to have an idea of the landscape.
""".format(location = st.session_state.get("location", "No location entered."),data=default_values, data2=default_values)



globe_text = """
## The globe is a visual representation of the data we have gathered.
### It is a snapshot of the world, a snapshot of the data we have collected.
"""

total_value = sum(default_values)

# personal info text
info_text = """
{total_value}
{coeff}
## Extra information.
### We will use this information to communicate.
""".format(total_value='We will renormalise later, your coefficient is:' if total_value>100 else 'as', coeff=total_value/100)

panel = [intro_text, location_text, profile_text, info_text, globe_text, ""]


def no_clicked():
    st.session_state.no_clicked = True

def yes_forward():
    st.session_state["current_page"] = min(st.session_state.current_page + 1, st.session_state.total_page - 1)

def create_name_and_email(key, kwargs = {}):
    survey = kwargs.get('survey')
    cols = st.columns(2)
    with cols[0]:   
        name = survey.text_input(key+' name', help="Help us best route your communication.")
    with cols[1]:
        email = survey.text_input(key+' email', help="Help us best route our communication.")
    
    
    # if survey.data.get("name"):
    #     name = survey.data.get("name")["value"]
    # else:
    #     name = None
    # if survey.data.get("email"):
    #     email = survey.data.get("email")["value"]
    # else:
    #     email = None
    # if name:
    #     st.write(f"Name: {name}")
    # if email:
    #     st.write(f"Email: {email}")
    pass

widget_info = [
    {"type": None, "key": None},
    {"type": "textinput", 
        "key": "location",
        "kwargs": {"survey": survey},
        "callback": enter_location("location")
     },
    {"type": "equaliser", "key": "equaliser", "kwargs": {"data": profile[0:5], "survey": survey, "default_values": default_values}},
    {"type": "name_and_email", "key": "#", "kwargs": {"survey": survey}},
    {"type": "openconnection", "key": "`Here` • `Now`", "kwargs": {"survey": survey, "authenticator": authenticator}},
    {"type": "globe", "key": "Singular Map", "kwargs": {"survey": survey, "database": "stability-gathering"}},
    {"type": "yesno", "key": "button_0", "kwargs": 
        {"survey": survey, "callback": (yes_forward, no_clicked), "labels":["Yes, tell me more", "Not really, you don't make sense."]}},
]
widget_dict = {}



# Dictionary mapping widget types to creation functions
widget_creators = {
    "button": create_button,
    "next": create_next,
    "dichotomy": create_dichotomy,
    "yesno": create_yesno_row,
    # "projectionmap": create_map,
    "checkbox": create_checkbox,
    "qualitative": create_qualitative,
    "name_and_email": create_name_and_email,
    "equaliser": create_equaliser,
    "openconnection": create_connection,
    "textinput": create_textinput,
    "globe": create_globe,
    None: lambda x, kwargs: st.write(x)
}


placeholders = [{"type": None, "key": None} for _ in range(len(panel)-len(widget_info))]


class WidgetyContainer(PagedContainer):
    def display_page(self, page):
        page_item = list(self.items)[page]
        (panel, widget_info) = page_item
        st.markdown(panel, unsafe_allow_html=True)
        widget_key = widget_info["key"]
        widget_type = widget_info["type"]
        widget_kwargs = widget_info["kwargs"] if "kwargs" in widget_info else {}
        if widget_type in widget_creators:
            widget_dict[widget_key] = widget_creators[widget_type](widget_key, kwargs = widget_kwargs)
        pass



def blurscape():
  """docstring for blurscape"""

  # Embed custom HTML, CSS, and JavaScript using st.markdown
  st.markdown("""
      <div class="card">
        <svg 
            viewBox="0 0 100% 100%"
            xmlns='http://www.w3.org/2000/svg'
            class="noise"
            >
          <filter id='noiseFilter'>
            <feTurbulence 
                          type='fractalNoise' 
                          baseFrequency='0.85' 
                          numOctaves='6' 
                          stitchTiles='stitch' />
          </filter>
          <rect
                width='100%'
                height='100%'
                preserveAspectRatio="xMidYMid meet"
                filter='url(#noiseFilter)' />
        </svg>
        <div class="content">
          <center><h1>Cooperation</h1></center>
          <center><h2>Bilateral? Triangular?</h2></center>
          <center><h3>or n-lateral?</h3></center>
          <br />
          <h3>Cooperation is a historic product</h3>
          <h4>We aim to stimulate an explicit exchange of perceptions and visions,
          themselves a product of the evolution of human society.</h4>
          <p>Find the `Forward >` button below.</p> 
        </div>
      </div>
      <div class="gradient-bg">
        <svg 
            viewBox="0 0 100vw 100vw"
            xmlns='http://www.w3.org/2000/svg'
            class="noiseBg"
            >
          <filter id='noiseFilterBg'>
            <feTurbulence 
                          type='fractalNoise'
                          baseFrequency='0.6'
                          stitchTiles='stitch' />
          </filter>
          <rect
                width='100%'
                height='100%'
                preserveAspectRatio="xMidYMid meet"
                filter='url(#noiseFilterBg)' 
          />
        </svg>
        <svg xmlns="http://www.w3.org/2000/svg" class="svgBlur">
          <defs>
            <filter id="goo">
              <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
              <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
              <feBlend in="SourceGraphic" in2="goo" />
            </filter>
          </defs>
        </svg>
        <div class="gradients-container">
          <div class="g1"></div>
          <div class="g2"></div>
          <div class="g3"></div>
          <div class="g4"></div>
          <div class="g5"></div>
        </div>
      </div>

      <script type="text/javascript">
        console.log('DOM loaded');
        document.addEventListener('DOMContentLoaded', () => {
            const interBubble = document.querySelector('.interactive');
            let curX = 0;
            let curY = 0;
            let tgX = 0;
            let tgY = 0;

            const move = () => {
                curX += (tgX - curX) / 20;
                curY += (tgY - curY) / 20;
                interBubble.style.transform = `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`;
                requestAnimationFrame(move);
            };

          window.addEventListener('mousemove', (event) => {
                tgX = event.clientX;
                tgY = event.clientY;
                console.log(tgX, tgY);
            });

            move();
        });
      </script>
  """, unsafe_allow_html=True)

  
# Run the Streamlit app
if __name__ == "__main__":
    with open("pages/stability_effects.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    blurscape()
    
    from streamlit_extras.stylable_container import stylable_container
    
    now = datetime.now()
    st.markdown(f"## _Today_ is {now.strftime('%A')}, {now.strftime('%-d')} {now.strftime('%B')} {now.strftime('%Y')}")


    create_access(key = '', kwargs = {})
    
    st.markdown("# <center>Introduction<center>", unsafe_allow_html=True)
    with stylable_container(key="card",css_styles=""" """):
        with stylable_container(key="content",css_styles="""
                                """):
            st.markdown(intro_text)
            st.markdown("# <center>Experimental<center>", unsafe_allow_html=True)

        with stylable_container(key="card",css_styles="""
                                """):
            with stylable_container(key="content",css_styles="""
                                    """):
                st.markdown("# <center>The idea.<center>", unsafe_allow_html=True)
                """
                ### The need for cooperation has never been greater.
                
                `In an infinite-dimensional energy space there are N bodies. They play according to one simple rule: they interact with each other.`
                
                ### We set up an simple data hub to visualise, to uncover, and analyse how complex interactions and adaptive behaviors emerge in social systems. 
                                
                """
                
    st.divider()

    if 'location' not in st.session_state:
        st.session_state['location'] = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state['coordinates'] = None  # Initial damage parameter

    # st.markdown(f"`Now is {now.strftime('%s')}-{now.strftime('%f')}~` max is {st.session_state.range if st.session_state.range else ''}")
    st.markdown(f"# <center>Chapter {float(st.session_state.current_page/st.session_state.range) if hasattr(st.session_state, 'range') and st.session_state.range != 0 else '0'}</center> ", unsafe_allow_html=True)

    st.markdown(f"""
                ### We call for shaping new narratives through lasting collective exchange, fostering enriching activity across generations and cultural backgrounds, to address problems of architecture, analysis, agency, adaptiveness, accountability, allocation, value, and access.
                """)
    
    
    if st.session_state["authentication_status"]:
        st.info('🐉 Some content is new')
        st.write(f'Welcome, your key is `<{st.session_state["access_key"]}>` 💭 keep it safe.')
        
        authenticator.logout('Disconnect', 'main', key='disconnect')
        add_vertical_space(13)
        st.divider()

                
    st.divider()
    add_vertical_space(13)
    st.divider()
    st.markdown(f"# <center>Chapter 1</center> ", unsafe_allow_html=True)
    st.markdown(f"""
    ### We aim to stimulate an explicit exchange of perceptions and visions, to address questions that are rarely asked and therefore lack systematic, clear, and tangible answers.
    """)
    paginator = WidgetyContainer(items = list(zip(panel, widget_info)), items_per_page=1)
    st.divider()

    st.markdown("# <center>Gathering data<center>", unsafe_allow_html=True)
    with stylable_container(key="card",css_styles=""" """):
        with stylable_container(key="content",css_styles="""
                                """):

            with st.container():
                paginator.display_page(st.session_state.current_page)
                col1, _, col2 = st.columns([2, 10, 3])
                with col2:
                    if st.button("Forward >", key="next_page"):
                        if st.session_state.current_page < paginator.get_total_pages()-1:
                            st.session_state.current_page += 1
                            st.rerun()
                            
                with col1:
                    if st.button("• Back", key="prev_page"):
                        if st.session_state.current_page >= 1:
                            st.session_state.current_page -= 1
                            st.rerun()
                with _:
                    st.write(f"Page {st.session_state.current_page}/{paginator.get_total_pages()}")
                    st.progress((st.session_state.current_page) / paginator.get_total_pages(), text=None)
