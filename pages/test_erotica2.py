import streamlit as st


# if st.secrets["runtime"]["STATUS"] == "Production":
st.set_page_config(
    page_title="Celestial Verse Portal",
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
import hashlib

import pandas as pd
from PIL import Image
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase
from lib.sound import recorder
import yaml
from yaml.loader import SafeLoader
import datetime
import random

img = None
def intro_eros2():
    name = "Name"
    st.markdown("""
Hello{name}? 

Is this Eros reading?

Eros may...be energy that permeates
Eros may...be energy that Springs
Eros may...be expression and voice,

Who embodies Eros and the erotic light?


We are exploring the concept of Eros 
and its embodiment in various forms.


                
                """)

def play():
    
    st.markdown("## Play")
    st.write(
"""
I want to invite you to embody Eros and speak, lending your voice to speak of
the inspiration or unravel one spark in the ideas, pointing the view or the 
perspective from Eros on the erotic energy. 

""")
    _images = get_images()
    random_cards = set([random.randint(0, len(_images)-1) for _ in range(len(_images))])
    picked_elements = [_images[i] for i in random_cards]
    picked_elements = [_images[i] for i in range(5)]
    
    st.write("Pick a card, any card")
    st.write("Speak through the image, embodying Eros")
    st.markdown("""
    
#    What does Eros say?
    
#    What does Eros see?

#    .... does Eros feel?

#    .... does Eros hear?

#    Does Eros heal?

#    Eros, taste does

#    Eros, touch does

#    Eros, know us

#    Eros, change the game

    """)
    
    
    
    # img = image_select(
    #     label="Eros, draw a cat",
    #     # return_value="index",
    #     images = picked_elements,
    #     # captions=["A cat"],
    # )

    cols = st.columns([1, 3, 1])
    
    img = picked_elements[0]

    with cols[1]:
        st.button("Reshuffle", use_container_width=True)
        if img is not None:
            st.image(img, use_column_width=True)
        st.button("This is an erotic key", use_container_width=True)
    
    
    
    st.divider()
    
    st.markdown("""
If you're feeling brave, you can record your voice,
it will be a trace.


If Eros is a powerful force , 
does it live within or it comes from outside?

If Eros is a deep energy,
isn't it clearest manifestation
the light that speaks through the mind?

                """)
    
    st.divider()
    from streamlit_selectable_image_gallery import image_gallery
    # A list of image URLs for testing
    images = [
        "https://images.unsplash.com/photo-1575936123452-b67c3203c357?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1488372759477-a7f4aa078cb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1488372759477-a7f4aa078cb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1488372759477-a7f4aa078cb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1488372759477-a7f4aa078cb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1574169208507-84376144848b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
    ]

    # The height of an image
    height = 200

    selected_index = image_gallery(images, height)
    if selected_index >= 0:
        st.markdown(f"You've selected image {selected_index}!")
    
    duration = st.slider("Duration", min_value=1, max_value=3, value=1, step=1)
    _suff = "s" if duration > 1 else ""
    if st.button(f"Start Recording {duration} Eros minute{_suff}", key="start_recording"):
        st.session_state.recording = True
        with st.spinner("Recording..."):
            recorder.record(duration=duration)
    if st.button("Save", key="save_recording"):
        st.toast("Recording saved! / preferences updated", icon="🚀")

import glob
# @st.cache_data    
def get_images():
    _image_files = glob.glob("images/cards/crop/*.jpg")

    images = [np.array(Image.open(img)) for img in _image_files]

    random.shuffle(images)
    
    return images


def main():
    play()


if __name__ == "__main__":
    main()
