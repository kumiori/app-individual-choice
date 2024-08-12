import streamlit as st
import streamlit_survey as ss
from streamlit_extras.streaming_write import write as streamwrite 
from pages.test_1d import _stream_example, corrupt_string
from lib.texts import _stream_once
import time
import pages

# st.set_page_config(
#     page_title="Choice choosen",
#     page_icon="👋",
#     initial_sidebar_state="collapsed"
# )

if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

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

st.header('Freedom of Choice is ')
st.markdown('# P•Hack the System')
st.markdown("## | fʌk ðə ˈsɪstɪm |" )
st.markdown("### `that sweet spot in between...`" )
# st.header("This is abstract 👋 Hello?")

abstract = ["""
## The journey, for us, is as important as the experience.
### This Time, this journey...\n
### is of a different kind.

### Not for the faint of heart, nor for the weak of mind.
## Fuck the system, you read it right.
""",
"""
# Sit comfortably, we roll. Take your Time and get ready for this: enjoy ~suspension~. 
# Consider some water.
## fork and knife are _of the mind_. A deep soundtrack is integral part of the trip. 
# Do you like smooth jazz? Our soundrack, is for you: to share.
This is: FREEDOM OF CHOICE + https://open.spotify.com/playlist/2ryrm6BlsY6CRuXL5jPZur
"""]

soundrack_html = """
<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/2ryrm6BlsY6CRuXL5jPZur?utm_source=generator" width="100%" height="152" frameBorder="10" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    """

with st.spinner('Welcome...'):
    time.sleep(3)

frame = st.empty()

streamwrite(_stream_once(abstract[0], damage=0.), unsafe_allow_html=True)
with st.spinner('Welcome...'):
    time.sleep(3)

# frame.empty()

# with frame.container(height=600):
#     # st.markdown(abstract[1])
#     streamwrite(_stream_once(abstract[1], damage=0.), unsafe_allow_html=True)

# frame.empty()
