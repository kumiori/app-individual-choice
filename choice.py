import streamlit as st
import streamlit_survey as ss
from streamlit_extras.streaming_write import write as streamwrite 
from pages.test_1d import _stream_example, corrupt_string
from lib.texts import _stream_once
import time

st.set_page_config(
    page_title="Choice choosen",
    page_icon="👋",
    initial_sidebar_state="collapsed"
)
if 'read_texts' not in st.session_state:
    st.session_state["read_texts"] = set()


st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.header('Freedom of Choice is choice by Choosing')
# st.header("This is abstract 👋 Hello?")

abstract = [""" ## The user's digital journey, for us, is as important as the experience.
            As the context from which - he or she - approaches this...

## Scattered through Liquid Crystal flat displays within a Digital Society, the following comes with a few lines of advice to prepare... 

# This Time, this journey...\n

## is of a different kind. 
""",

""" 
## We wish you at ease. 

# Prepare your ritual, allow yourself to indulge. If you like scotch, share one with us, if you enjoy whiskey (or whisky), prepare a glass. 

### Burn an Earthy wood and pour, light a cigar, _flow slow_. Pick your favourite flower, breathe in - let a candle illuminate further - exhale - and give.. 

# Time: your-Self, them-Self, One-Self need some to meet. 
""",
"""
# Sit comfortably, and if pleases you - rocking slowly, we roll. Take your Time and get ready for this: enjoy ~suspension~ in Thought. 
 
# Consider some water.
 
## fork and knife are _of the mind_, we cut with a click - a deep soundtrack is integral part of the trip. 

# Do you like smooth jazz? Our soundrack, is for you: to share.

This is: FREEDOM OF CHOICE + https://open.spotify.com/playlist/2ryrm6BlsY6CRuXL5jPZur
"""]

soundrack_html = """
<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/2ryrm6BlsY6CRuXL5jPZur?utm_source=generator" width="100%" height="152" frameBorder="10" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    """

frame = st.empty()

with frame.container(height=666):
    # st.markdown(abstract[0])
    streamwrite(_stream_once(abstract[0], damage=0.), unsafe_allow_html=True)
    with st.spinner('Welcome...'):
        time.sleep(3)

frame.empty()

with frame.container(height=600):
    # st.markdown(abstract[1])
    streamwrite(_stream_once(abstract[1], damage=0.), unsafe_allow_html=True)
    with st.spinner('Welcome...'):
        time.sleep(3)

frame.empty()

with frame.container(height=600):
    streamwrite(_stream_once(abstract[2], damage=0.), unsafe_allow_html=True)
    st.markdown(soundrack_html, unsafe_allow_html=True)
# st.markdown(abstract)

st.sidebar.header('About')
st.sidebar.write('This may seem simple.')
