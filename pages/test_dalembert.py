import streamlit as st
# import datetime
from datetime import datetime, timedelta

import time
from streamlit_extras.add_vertical_space import add_vertical_space 
import yaml
from yaml.loader import SafeLoader
from lib.texts import friendly_time
from lib.geo import reverse_lookup
import locale

from lib.texts import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from streamlit_extras.streaming_write import write as streamwrite 
import time
import string
import streamlit_survey as ss
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
import random
from lib.presentation import PagedContainer
from lib.authentication import _Authenticate
import hashlib
# from pages.test_game import display_dictionary_by_indices
# from pages.test_pleasure import display_dictionary
from streamlit_authenticator.exceptions import RegisterError

from lib.matrices import generate_random_matrix, encode_matrix, display_matrix
from lib.dictionary_manip import display_dictionary, display_dictionary_by_indices, display_details_description
from lib.survey import CustomStreamlitSurvey
update_frequency = 500  # in milliseconds
from lib.texts import match_input, _stream_once
from lib.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_yesno_row, create_next, create_globe, create_textinput, create_checkbox, create_equaliser, fetch_and_display_data, conn
# from pages.test_footer import footer
import pandas as pd
import numpy as np
from lib.geo import get_coordinates
locale.setlocale(locale.LC_TIME, 'fr_FR')

class Authenticate(_Authenticate):

    def register_user(self, form_name: str, location: str='Athens', preauthorization=True) -> bool:
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
        if not location:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        register_user_form = st.form('OpenConnection')

        col1, _, col2 = st.columns([2, .1, 2])
        
        register_user_form.subheader(form_name)

        new_email = ''
        new_username = ''
        new_name = ''
        new_password = ''
        new_password_repeat = ''
        
        if register_user_form.form_submit_button('`Here` • `Now`'):
            now = datetime.now()
            st.write(now) 
            if len(location) > 0:
                coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
                if coordinates:
                    st.write(f"Coordinates for {location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
                    st.session_state.location = location
                    st.session_state.coordinates = coordinates
                    # the access key is the hash of the current time (now) and the location
                    access_key_string = f"{now}_{location}"
                    access_key_hash = hashlib.md5(access_key_string.encode()).hexdigest()
                    
                    # access_key_hash = hashlib.sha256(access_key_string.encode()).hexdigest()
                    # st.write(access_key_hash)
                    if self.__register_credentials(access_key_hash, new_name, new_password, new_email, preauthorization):
                        self.credentials['access_key'] = access_key_hash
                # self._register_credentials(new_username, new_name, new_password, new_email, preauthorization)
                return True
            else:
                raise RegisterError('We forget the `where`, there...?')

if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Panel Discussion - Athens Conference 2024",
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

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

with open("pages/discourse.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write(f.read())
    
with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
class _PagedContainer(PagedContainer):

    def display_page(self, page):
        start_idx = page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_items = [start_idx, end_idx]

        display_dictionary_by_indices(self.items, indices=page_items)
    
        if self.show_pagination:
            st.write(f"Page {page + 1}/{self.get_total_pages()}")

class ConnectingContainer(PagedContainer):
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

    def check_no_exit(self, session_state, data):
        if session_state.no_clicked:
            st.warning("Perhaps we misuderstood.")
            st.info("We are always here, we can meet back later.")
            st.write(data)
            st.write(session_state)
            st.stop()

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
            
survey = CustomStreamlitSurvey()

if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

if "current_booklet_page" not in st.session_state:
    st.session_state["current_booklet_page"] = 0

if "total_discourse_page" not in st.session_state:
    st.session_state["total_discourse_page"] = 1

if 'no_clicked' not in st.session_state:
    st.session_state["no_clicked"] = False

def no_clicked():
    st.session_state.no_clicked = True

def yes_forward():
    st.session_state["current_discourse_page"] = min(st.session_state.current_discourse_page + 1, st.session_state.total_discourse_page - 1)

def create_map(key, kwargs = {}):

    _c = st.session_state.coordinates
    
    if _c:
        with st.spinner():
            _lookup = reverse_lookup(st.secrets.opencage["OPENCAGE_KEY"], _c)
    
        data = _lookup
        # # Access relevant information from the first entry
        first_entry = data[0][0]
        # political_union = first_entry["components"]["political_union"]
        print(first_entry)
        sun_rise = first_entry["annotations"]["sun"]["rise"]["astronomical"]
        sun_set = first_entry["annotations"]["sun"]["set"]["astronomical"]
        print(list(first_entry["annotations"]["UN_M49"]["regions"])[-3])
        geographical_region = str(list(first_entry["annotations"]["UN_M49"]["regions"])[-3]).title()
        confidence = first_entry["confidence"]
        st.markdown(f"### The Sun rises from the east and sets in the west.")
    #     st.markdown(f"## The geographical region is {geographical_region} and the political union is {political_union}.")
        st.markdown(f"## Our confidence in  level is {confidence}.")
        sun_rise_readable = datetime.utcfromtimestamp(sun_rise).strftime('%H:%M:%S UTC')
        sun_set_readable = datetime.utcfromtimestamp(sun_set).strftime('%H:%M:%S UTC')

        st.markdown(f"At {_c} the sun rises at {friendly_time(sun_rise)} and sets at {friendly_time(sun_set)}.")
        # st.markdown(f"The sun rises at {sun_rise_readable} and sets at {sun_set_readable} in {text}.")


        st.markdown(f"## Forward, confirming that you connect from `{geographical_region}`")


    
    df = pd.DataFrame({
        "col1": np.random.randn(1000) / 10 + (-_c[0]),
        "col2": np.random.randn(1000) / 10 + ((_c[1] + 180) % 360),
        "col3": np.random.randn(1000) * 100,
        "col4": np.random.rand(1000, 4).tolist(),
    })

    st.map(df,
        latitude='col1',
        longitude='col2',
        size='col3',
        color='col4',
        zoom=6,
        use_container_width=True)
    st.markdown('### Do you see new patterns _known_?')
    st.markdown('## This is how we think: a _matrix is a map where patterns emerge_')

def create_connection(key, kwargs = {}):
    authenticator = kwargs.get('authenticator')
    survey = kwargs.get('survey')
    _location = survey.data['location?']['value']

    if st.session_state["authentication_status"] is None:
        try:
            if authenticator.register_user(' Check • Point ', location = _location,  preauthorization=False):
                st.success(f'Very good 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
                    💨 Here is one for your access ✨ <`{ authenticator.credentials["access_key"] }`> ✨.        \
                    Keep it in your pocket, add it to your wallet...keep it safe 💭. You will use it to re•open the connection 💫')
        except Exception as e:
            st.error(e)
            
    else:
        st.warning("We are already connected. Re•enter using your key, check the connection later.")

def create_access(key, kwargs = {}):
    
    MILESTONE_KEY_CHAPTER = 9
    
    if st.session_state.range >= MILESTONE_KEY_CHAPTER:
        authenticator.login('Do you already have a key?')

    pass

def enter_location(label):

    if survey.data.get(label):
        location = survey.data.get(label)["value"]
    else:
        return
    coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
    if coordinates:
        # st.info(f"Coordinates for {location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
        st.session_state.location = location
        st.session_state.coordinates = coordinates
    
intro_text = """

## On aimeirait ... 

## Que penses-tu de ces questionnements ?

### En tant ..., membre  $\partial'$Alembert ...
Tu as une invitation à prendre part à la conversation, à la réflexion, à la coordination, à l'action.

"""

panel_0 = """

## Mood rings dolly the sheep hey arnold discovery zone sup. Sublime personal computer playa turquoise I don’t want no scrubs, miss cleo I will be your father figure independence day space jam carlton dance.

"""

panel_1 = """

Home alone g-shocks troll dolls playstation independence day my heart will go on. Cut-off jean shorts stretch armstrong kool-aid man umbro shorts, discovery zone rocko's modern life quiet storm maze screensavers. Gak oasis slap bracelet mario lemieux airwalk. Home improvement pixie cut turtlenecks george michael sugar ray. Denzel washington aviators tying your sweater around your waist hoodies uncle phil west wing, mazda mpv meg ryan life is like a box of chocolates the truman show i'm king of the world alta vista.

# Question 1: (Fausse dichotomie)

""" 

panel_2 = """

Avez bonnes experiences en presenitel ? 

Puff daddy bye bye bye fresh windows 95. Life is like a box of chocolates polo shirts with popped collars renting movies at a store west wing, saved by the bell toy story cargo pants wearing your cap backwards. Koosh ball nickelodeon lisa frank crimped hair garth brooks pixie cut, personal computer neon colors rachel green david duchovny. Yo patti mayonnaise quiet storm blur, kool-aid man super nintendo hush puppies I will be your father figure chat rooms.

# Question 2: (Vraie dichotomie)

"""

## What do you think? 
## Are we on the right path?
## Is this a good idea?
## Shall .. more details?
## Can we .. more details?


panel_3 = """ 

## <center> ...  🧶 </center> 

"""
 
panel_4 = """

## Renting movies at a store west wing, saved by the bell toy story cargo pants wearing your cap backwards.


"""
 
panel_5 = """

## Puff daddy bye bye bye fresh windows 95. Life is like a box of chocolates polo shirts with popped collars 


"""


sandbox = """
## We'll tell you all about it in a moment...

## Are you happy to engage?
## Are you ready to participate? 
## Where are you located? 
## Does this sound like a _good idea_? 


## Our simple platform is multi-purpose and inclusive by design, 

## To use it, we start questioning the channels and the structures through which we relate and the interfaces through which we communicate. 

## As we invite your free and conscious participation, just a reminder:
 our platform is 'free software' in the sense that has a lot to do with freedom, and nothing with price.

"""

""" `Punchline, en français et avec point d'interrogation finale ?`
    `La mécanique à l'echelle humaine ?`
"""

if 'range' not in st.session_state:
    st.session_state.range = 0  # Set the initial value



def update_range(page_number):
    # Initialize session state

    # Update range if the current page_number is greater
    if page_number > st.session_state.range:
        st.session_state.range = page_number


panel = [panel_0, panel_1, panel_2, panel_3, panel_4, panel_5
        #  panel_9, 
        #  panel_10, 
        #  panel_11, panel_12
         ]

challenges = [
    ("Direction, Vision, Structure", ""),
    ("Liberté", ""),
    ("...", ""),
    ("Control variable for lower bound", ""),
]

widget_info = [
    {"type": None, "key": None},
    {"type": "yesno", "key": "button_0", "kwargs": 
        {"survey": survey, "callback": (yes_forward, no_clicked), "labels":["Oui !", "Non, merci."]}},
    {"type": "yesno", "key": "button_1", "kwargs": 
        {"survey": survey, "callback": (yes_forward, no_clicked), "labels":[":honey_pot: ", ":ticket: "]}},
    {"type": "equaliser", "key": "equaliser", "kwargs": {"data": challenges[0:3], "survey": survey}},
    # {"type": "checkbox", "key": "opinion_counts", "kwargs": {"survey": survey, "label": 'Yes, my opinion counts.'}},
    {"type": "dichotomy", "key": "dichotomy_1", "kwargs": {"label": "transition_rate", "survey": survey, "inverse_choice": lambda x: 'slow 🐌' if x == 1 else 'fast 💨' if x == 0 else 'a mix ✨', "name": 'there', 'question': 'La question posée : .','messages': ["Oui", "Non", "_il y a-t-il des options ?_"], 'forward_message': "" }},
    {"type": None, "key": None},
    {"type": "yesno", "key": "button_1", "kwargs": 
        {"survey": survey, "callback": (yes_forward, no_clicked), "labels":["Yes, indeed!", "Not really, I'm not sure."]}},
    # {"type": "button", "key": "Let's...", "kwargs": {"survey": survey}},
    {"type": "equaliser", "key": "equaliser", "kwargs": {"data": challenges[0:5], "survey": survey}},
    {"type": "textinput", 
        "key": "location?",
        "kwargs": {"survey": survey},
        "callback": enter_location("location?")
     },
    {"type": "projectionmap", "key": "map", "kwargs": {"survey": survey}},
    {"type": "openconnection", "key": "`Here` • `Now`", "kwargs": {"survey": survey, "authenticator": authenticator}},
    {"type": "globe", "key": "Singular Map", "kwargs": {"survey": survey, "database": "gathering"}},
    {"type": "button", "key": "`Here`  `Now`", "kwargs": {"survey": survey}},
    {"type": "yesno", "key": "extra_info", "kwargs": {"survey": survey}},
    {"type": "qualitative", "key": "quali", "kwargs": {"survey": survey}},
    {"type": None, "key": None}
]

placeholders = [{"type": None, "key": None} for _ in range(len(panel)-len(widget_info))]

widget_info = widget_info + placeholders

widget_dict = {}


# Dictionary mapping widget types to creation functions
widget_creators = {
    "button": create_button,
    "next": create_next,
    "dichotomy": create_dichotomy,
    "yesno": create_yesno_row,
    "projectionmap": create_map,
    "checkbox": create_checkbox,
    "qualitative": create_qualitative,
    "equaliser": create_equaliser,
    "openconnection": create_connection,
    "textinput": create_textinput,
    "globe": create_globe,
    None: lambda x, kwargs: st.write(x)
}

# Main function
def main():
    # Page title
    # st.title(":circus_tent: Europe in Discourse")
    # st.title(":fountain: Athens Conference, :satellite: 2024")

    # survey = ss.StreamlitSurvey("Home")
    col1, col2, col3 = st.columns(3)

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    if 'current_discourse_page' not in st.session_state:
        st.session_state.current_discourse_page = 0
    
    if 'damage_parameter' not in st.session_state:
        st.session_state.damage_parameter = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state['location'] = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state['coordinates'] = None  # Initial damage parameter
    # once usage:
    
    streamwrite(_stream_once(intro_text, 0))
    # st.markdown()
    
    # create_connection("connection", kwargs = {"survey": survey, "authenticator": authenticator})

    st.divider()
    now = datetime.now()
    st.markdown(f"# <center>Cher·ère·s Tou·te·s </center> ", unsafe_allow_html=True)
    st.markdown(f"# <center>{float(st.session_state.current_discourse_page/st.session_state.range) if hasattr(st.session_state, 'range') and st.session_state.range != 0 else '0'}</center> ", unsafe_allow_html=True)
    st.divider()
    st.markdown("### <center>.</center>", unsafe_allow_html=True)
    st.markdown('<center>``qu\'est-ce vous envisagez ?``</center>', unsafe_allow_html=True)
    st.markdown('', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        matrix_size = 5
        matrix_placeholder = st.empty()
        seconds = 1

        start_time = time.time()
        # st.write(st.session_state.current_discourse_page)
        if st.session_state.current_discourse_page == 0:
            while True:
                time.sleep(update_frequency / 1000.0)  # Convert to seconds
                matrix = generate_random_matrix(matrix_size)
                encoded_matrix = encode_matrix(matrix)

                # norm_value = frobenius_norm(encoded_matrix)/_scale
                # norm_values.append(norm_value)
                
                # with col1:
                #     st.write(norm_value)
                
                with col2:
                    matrix_placeholder.empty()
                    with matrix_placeholder:
                        display_matrix(matrix)
                        
                elapsed_time = time.time() - start_time
                if elapsed_time >= seconds:
                    matrix_placeholder.empty()
                    break

    create_access(key = '', kwargs = {})
    st.divider()
    
    if st.session_state["authentication_status"]:
        st.error('Error! 🐉 Some content is new')
        # st.session_state.current_discourse_page = 9
        
        authenticator.logout('Disconnect', 'main', key='disconnect')
    # st.write(f'Welcome')
    
    st.markdown(f"## _Aujourd'hui_ est {now.strftime('%A')}, {now.strftime('%d')} {now.strftime('%B')} {now.strftime('%Y')}")
    if st.session_state["authentication_status"]:
        st.write(f'Welcome, your key is `<{st.session_state["access_key"]}>` 💭 keep it safe.')

    
    # with tab1:
    connect()

    tab1, tab2 = st.tabs(["References", "Plus si affinités..."])
    
    with tab1:
        st.markdown("## Le botin")
        references()

    with tab2:
        st.markdown("## Affinités electives")
        affinites()
        
    return survey

def display_category_description(category, description):
    """
    Function to display category and its description.
    """
    col1, _, col2 = st.columns([2, .2, 4])
    with col1:
        # st.markdown(f"**{category}**")
        st.markdown(f"{category}")
    with col2:
        st.markdown(description)
    st.write("---")

def connect():
    if "current_discourse_page" not in st.session_state:
        st.session_state["current_discourse_page"] = 0
    paginator = ConnectingContainer(items = list(zip(panel, widget_info)), items_per_page=1)
    st.session_state.total_discourse_page = paginator.get_total_pages()
    # st.write(f'Current page is {st.session_state.current_discourse_page}/{st.session_state.total_discourse_page}')
    with st.container():
        col1, _, col2 = st.columns([2, 12, 2])
        with col2:
            if st.button("$ • > $", key="next_discourse_page"):
                st.session_state["current_discourse_page"] = min(st.session_state.current_discourse_page + 1, paginator.get_total_pages() - 1)
        with col1:
            if st.button("• $<$", key="prev_discourse_page"):
                st.session_state["current_discourse_page"] = max(st.session_state.current_discourse_page - 1, 0)
        with _:
            st.progress((st.session_state.current_discourse_page+1) / paginator.get_total_pages(), text=None)
        
        paginator.check_no_exit(st.session_state, survey.data)
        paginator.display_page(st.session_state.current_discourse_page)
        update_range(st.session_state.current_discourse_page)

    st.divider()


def glossary():
    categories = [
        ("Environmental Sustainability", "Priorities related to ecological balance, climate action, and sustainable development."),
        ("Social Equity", "Addressing issues of justice, equality, and inclusivity within society."),
        ("Technological Innovation", "Exploring the role of technology in societal progress and ethical considerations."),
        ("Economic Resilience", "Focusing on economic systems, financial stability, and resilience in the face of global challenges."),
        ("Cultural Identity", "Discussing the dynamics and evolution of cultural identities in a changing world."),
        ("Health and Well-being", "Prioritising healthcare, mental health, and overall well-being of communities and individuals."),
        ("Education and Knowledge", "Examining strategies for knowledge dissemination, access to education, and lifelong learning."),
        ("Governance and Policy", "Addressing the role of governance, policy frameworks, and political systems in societal change."),
        ("Community Engagement", "Emphasising the importance of community participation and grassroots initiatives."),
        ("International Collaboration", "Discussing the role of global cooperation and diplomacy in addressing shared challenges.")
    ]

    for category, description in categories:
        display_category_description(category, description)
    

    return

def more():
    links_row = row(2, vertical_align="center")
    links_row.button(
        ":honey_pot: Explore our panel contributions",
        use_container_width=True,
    )
    links_row.link_button(
        ":ticket: Visit the conference's website",
        "https://www.europeindiscourse.eu/",
        use_container_width=True,
    )

    return
    
def references():
    with st.expander("Toutes les données", expanded=False):
        st.write("Données de Profil:")
        st.json(survey.data, expanded=True)
        st.json(st.session_state, expanded=True)

    # st.markdown("## Suggest reference..")

    return

def affinites():

    references_dict = {
        "## Livre #1 \n ## David Graeber": {"### `Zzz zzz zzz`"},
        "## Anecdote #1": {"### ..."},
    }

    display_dictionary(references_dict)


if __name__ == "__main__":
    
    survey = main()
    add_vertical_space(7)
    
    st.markdown("""##
                
                """)

