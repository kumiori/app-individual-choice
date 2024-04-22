import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px
from matplotlib.patches import Polygon
from lib.survey import CustomStreamlitSurvey
from lib.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_yesno_row, create_next, create_globe, create_textinput, create_checkbox, create_equaliser, fetch_and_display_data, conn

from streamlit_extras.stateful_button import button as stateful_button 
from streamlit_extras.stylable_container import stylable_container
from streamlit_modal import Modal
from streamlit import rerun as rerun  # type: ignore
import streamlit.components.v1 as components
from lib.authentication import _Authenticate

from streamlit_elements import mui
from streamlit_elements import elements

import streamlit_shadcn_ui as ui

from streamlit_image_select import image_select


import pandas as pd
from PIL import Image
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase
from lib.sound import recorder
import yaml
from yaml.loader import SafeLoader
import datetime
with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

class Authenticate(_Authenticate):

    def register_user(self, form_name: str, match: bool=False, preauthorization=True) -> bool:
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
        
        access_key_hash = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
        if register_user_form.form_submit_button('`Here` • `Now`'):
            if match:
                if self.__register_credentials(access_key_hash, self.webapp, preauthorization):
                    self.credentials['access_key'] = access_key_hash
                return True
            else:
                st.success(f'Well 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
                    This is yours <`{ hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest() }`>.        \
                    Keep it in your pocket, add it to your wallet...keep it safe 💭. It will open only if the match holds 🕯️')
                raise RegisterError('Speaking of matches, have you watched the movie `The Match Factory Girl`, by Aki Kaurismäki? 🎥')

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
        # if not self.validator.validate_username(username):
        #     raise RegisterError('Username is not valid')
        # if not self.validator.validate_name(name):
        #     raise RegisterError('Name is not valid')
        # if not self.validator.validate_email(email):
        #     raise RegisterError('Email is not valid')
        
        existing_access_key = self.get_existing_access_key(access_key)
        
        if existing_access_key:
            st.write("Access key already exists. Choose a different location or try again later.")
            return False
        
        data = {'key': access_key, 'webapp': webapp}
        response = self.supabase.table('access_keys').insert(data).execute()
        # st.write(data, response)
        if response:
            return True
    
modal = Modal(
    "Disclaimer", 
    key="manifesto",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)

survey = CustomStreamlitSurvey()
personal_data = CustomStreamlitSurvey(label="personal")


if "checked" not in st.session_state:
    st.session_state['checked'] = ''

open_modal = st.button("Open Question")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        """This is `explicit thinking` as visual language."""
                 
        st.markdown("## Some say this, some say that.")
        st.markdown("""
In contrast to a dominating and dominant view of eros, which often oversimplifies and underestimates its richness and complexity, this collaborative project seeks to amplify diverse voices and perspectives on the subject. In patriarchal societies, eros is frequently confined to narrow and predefined roles, reinforcing rigid gender norms and power dynamics.

By inviting to participate in this exploration, we challenge the patriarchal constraints placed on eros and celebrate its multifaceted nature. Through this inclusive dialogue, we aim to dismantle outdated paradigms and foster a deeper understanding of eros as a universal force that transcends societal constructs and embraces the full spectrum of human experience.


Patriarchal constraints on eros reinforce hierarchical power structures, restrict individual agency and autonomy, and perpetuate harmful stereotypes and inequalities based on gender and sexuality. Overcoming these constraints requires challenging and dismantling patriarchal norms and advocating for inclusive, equitable, and empowering expressions of eros for all individuals.

On a societal level, the connection between eros and sex shapes cultural norms, attitudes, and behaviors surrounding sexuality and relationships. Eros often intersects with social constructs such as gender, power, and morality, influencing societal perceptions of sexuality and acceptable forms of expression. The commodification and commercialization of sex in media, advertising, and entertainment reflect societal attitudes toward eros, often reinforcing narrow and objectifying representations of desire and intimacy.

### The Project
We commit to making this project self-funded. We establish a connection with participants in such a way that contributions are innovative and engaging. By incorporating audio recordings from participants, we create a dynamic and interactive platform that invites viewers to not only listen but also actively engage with the content.

Eros plays a role in every process of emancipation.
Eros plays a role in every process of liberation.
Eros plays a role in every process of awakening, 
    Eros plays, 
            inviting to play. 
            
            
            Would you like to play?

            .-;_;;-;;:+p0-"llLl
            
            ☎️📞🤳🏾💫🫧🛁🌺🎶⛈️💦
"""
        )
        value = st.checkbox("Checked for understanding", value=st.session_state['checked'],
                            on_change=lambda x: st.session_state.update({'checked': x}),
                            args=(not st.session_state.checked,))
        st.write(f"Understanding: {value}")


        
st.write('Understanding', st.session_state['checked'])
if st.session_state['checked']:
    st.write("Consent is granted.")
    
def stepper_component(active = 0):
    steps = ["Intro", "Would you like to play?", "Save preferences", "View the shots", "Play"]

    # Display the stepper
    with elements(f"example_stepper{active}"):
        with mui.Stepper(activeStep=active, alternativeLabel=True):
            for label in steps:
                with mui.Step:
                    mui.StepLabel(label, completed = False)


def energy_mix():
    """We revisit eros with a philosophical twist. Would you like to explore specific themes?
    """
    st.write("Eros as an Energy Mix.")

    
    equaliser_data = [
        ("Sensual Exploration", ""),
        ("Emotional Connection", ""),
        ("Intellectual Stimulation", ""),
        ("Spiritual Connection", ""),
        ("Power Dynamics", ""),
        ("Personal Growth", ""),
    ]

    # st.write(survey)
    st.markdown("Let's think _energetically..._")
    st.markdown("### Using an _energy_ mixer, where energy _comes from_?")
    create_equaliser(key = "equaliser", kwargs={"survey": survey, "data": equaliser_data})
    
    
def intro_eros():
    st.write("Eros as an Energy.")
    




    st.markdown("""
Eros is a powerful force with us, isn’t it clearest crystallisation that which speaks through the mind?


Enjoy your selection of my catalogues pictures tagged erotica.

Everyday objects, views, details, street walls, abstract scenes, which in some way inspire me the eros.

If eros is a potent force that permeates our lives, does it come from within or it comes from the outside? It is manifesting in myriad ways, both subtle and profound.


My selection of photographs, tagged erotica, starts building up as a glance to eros' multifaceted nature. Through my lens, everyday objects, views, and details are transformed into vessels of desire, inviting to explore the sensual within the transcending mundane.


I want to invite you to participate in this collaborative project, lending their voice to speak of the inspiration or the sparks or the ideas or the viewpoints or the perspective they have on eros and the erotic energy.

Why you? See below.

                """)    
    
def platform():
    st.markdown("""
## This is an invitation

This invitation can be more beautifully crafted and be more deeply evocative. I invite you to join in a collaborative exploration of eros and erotic energy, inviting you to lend your voices to speak an image of your choice.

We set silence aside, you create space to speak what is without words. The rustle of spirits awakening to life beyond form.

Through the folds of our thoughts, eros, there is a new story waiting to be told—an intimate and profound journey into the depths of eros.

By participating in this collaborative endeavor, you to contribute to a collective exploration of eros, enriching the dialogue and expanding our understanding of this timeless force that shapes our perceptions and experiences.

    """)
    
def preferences():

    st.markdown("## Your Preferences • Checkpoint")
    st.write("Eros Energy mix.")
    
    
    switch_value = ui.switch(default_checked=True, label="Happy to share some extra details?", key="switch1")
    
    if switch_value:
        with st.expander("Personal Details", expanded=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                name = st.text_input("Name", "")
            with col2:
                desired_bedrooms = st.number_input("Superpower", min_value=1, max_value=2, step=1)
            additional_comments = st.text_area("Any additional comments or preferences?", "")

    
def shots():
    
    st.markdown("## Shots")
    if st.button("View Shots"):
        st.toast("Your preferences have been saved!", icon="🚀")

def play():
    
    st.markdown("## Play")
    st.write(
"""
I want to invite you to embody Eros and speak, lending your voice to speak of
the inspiration or unravel one spark in the ideas, pointing the view or the 
perspective from Eros on the erotic energy. 

""")
    img = image_select(
        label="Select a cat",
        return_value="index",
        images=get_images(),
        # captions=["A cat"],
    )
    
    st.write("Speak through...", img)
    
    duration = st.slider("Duration", min_value=1, max_value=3, value=1, step=1)
    _suff = "s" if duration > 1 else ""
    if st.button(f"Start Recording {duration} Eros minute{_suff}", key="start_recording"):
        st.session_state.recording = True
        with st.spinner("Recording..."):
            recorder.record(duration=duration)
    if st.button("Save", key="save_recording"):
        st.toast("Recording saved! / preferences updated", icon="🚀")

@st.cache_data    
def get_images():
    return [
            "https://bagongkia.github.io/react-image-picker/0759b6e526e3c6d72569894e58329d89.jpg",
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
            np.array(Image.open("images/APC_3171.jpg")),
        ]

def invitation():
    st.markdown("## What is the game?")
    st.markdown("""

In each shot, whether in the intimacy of distant shot or the raw beauty of an abstract scene, eros asserts its presence, reminding us of its ever-present influence on our perceptions and experiences. Truly, is eros just energy that resonates within us all? Shaping our thoughts, inspiring our creativity, and infusing our lives with passion and meaning?

But who speaks the voice of eros?
Who embodies this spirit?

We set silence aside, to honor a speech without words, the rustle of spirits awakening to life beyond form, through the folds of our bodies there is a new story to be told.
""")
    
def main():
    st.markdown("# <center>• Welcome •</center>", unsafe_allow_html=True)
    st.title("Eros speaks: images in expression")
    st.write("## Eros as an Energy.")




    # Define the content for the card
    def render_card():
        with mui.Card(sx={"width": 300}):
            with mui.CardContent:
                mui.Typography("Forgotten Idea", sx={"fontSize": 14}, color="text.secondary", gutterBottom=True)
                mui.Typography("erotica, n.", variant="h5", component="div")
                mui.Typography("/ ɪˈrɒtɪkə/")
                mui.Typography("n.", sx={"mb": 1.5}, color="text.secondary")
                mui.Typography(
                    "Matters of love; erotic literature or art (frequently as a heading in catalogues).")
                mui.Typography(
                    'Oxford English Dictionary',
                    variant="body2",
                    dangerously_set_inner_html=True
                )
            with mui.CardActions:
                mui.Button("Unlearn More", size="small")
                mui.Link("Go to Oxford English Dictionary", href="https://www.oed.com/search/dictionary/?scope=Entries&q=erotica", target="_blank")

    # Display the card
    
    col1, col2 = st.columns([1, 1])
    with col1:
        with elements("basic_card"):
            render_card()

    with col2:
        st.markdown("## Erotica • (Eροσ)")
        st.markdown("/ ɪˈrɒtɪkə/")
        st.markdown("### E • as in Energy")
        st.markdown("### R • as in ______")
        st.markdown("### O • as in ______")
        st.markdown("### S • as in ______")

    """
In philosophy, eros often represents a primal and powerful force, driving individuals towards fulfillment and connection. It encompasses desires for love, beauty, and transcendence, influencing human thoughts and actions.

Eros inspires every day experience from within ordinary details.
But who speaks the voice of eros?
Who embodies this spirit?

I want to invite you to embody Eros and speak, lending your voice to whisper an inspiration
or unravel a spark of idea, pointing the view or the 
perspective from Eros on the erotic energy. 

Eros plays a role in every process of emancipation. Eros plays a role in every process of liberation. Eros plays a role in every process of awakening, Eros plays, inviting to play.

Thinking as an exploration, expression, and manifestation.

    """

    st.divider()
    st.header("Disclaimer:")
    st.write("""
             `When we integrate eros, thinking, and expression, we delve into the depths of human experience. 
             Philosophical reflection also explores the complexities of desire, the nature of intimacy, and the pursuit of any meaning. Expression becomes a means to articulate insights, capturing the nuances of eros in all its manifestations.
             `
    """)
    st.write('`.|.|..........|.....................................|............*..............|.....||.`')

    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['cookie']['expiry_minutes'],
        config['preauthorized'],
        webapp = 'erotica-players'
    )
    
    authenticator.login('🎶 • Do you have an access key?', key='author_access')
    if st.session_state["authentication_status"]:
        now = datetime.datetime.now()
        st.markdown(f"# _Today_ is {now.strftime('%A')}, {now.strftime('%d')} {now.strftime('%B')} {now.strftime('%Y')}")

    db = IODatabase(conn, "access_keys")

    data = db.fetch_data()
    df = pd.DataFrame(data)
    item_count = len(df)
    
    # st.write(df)
    cols = st.columns(4)
    
    with cols[0]:
        ui.metric_card(title="Total count", content=item_count, description="Keys forged", key="card1")
    with cols[1]:
        ui.metric_card(title="Total funding", content="0.01 €", description="Since the start", key="card2")
    with cols[2]:
        ui.metric_card(title="Pending invites", content="13", description="This is an art", key="card3")
    with cols[3]:
        st.markdown("### Εροσ • Erotic")
        ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")
        ui.badges(badge_list=[("explicit", "primary")], class_name="flex gap-2", key="viz_badges3")
        
    # st.error('🐉 Some content is new')
    key = st.session_state["access_key"] if st.session_state["access_key"] else authenticator.credentials["access_key"]
    no_key = 'unknown'
    st.write(f'Welcome, your key is `<{ key }>` 💭 keep it safe.')
        
    stepper_component()
    st.divider()
    intro_eros()
    platform()

    st.divider()
    stepper_component(active = 1)

    energy_mix()
    
    invitation()
    
    
    st.divider()

    stepper_component(active = 2)
    
    preferences()
    
    st.divider()
    stepper_component(active = 3)
    shots()
    st.divider()

    stepper_component(active = 4)
    play()



if __name__ == "__main__":
    main()