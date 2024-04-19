import streamlit as st
from streamlit_extras.stateful_button import button as stateful_button 
from streamlit_extras.stylable_container import stylable_container


st.markdown("""
<style>
.custom-button {
   background-image: url("data/qrcode_1.png");
   color: white;
   padding: 14px 20px;
   margin: 8px 0;
   border: none;
   cursor: pointer;
   width: 100%;
   height: 200px;
   
}
.custom-button:hover {
   opacity: 0.8;
}
</style>
<button class="custom-button">Custom Button</button>
""", unsafe_allow_html=True)


st.image("data/qrcode_1.png", width=200)

if st.button("Click me"):
    st.write("Clicked")


# st.markdown(
#     """
#     <style>
#     button {
#         background: white!important;
#         border: none;
#         padding: 0!important;
#         color: black !important;
#         text-decoration: none;
#         cursor: pointer;
#         border: none !important;
#     }
#     button:hover {
#         text-decoration: none;
#         color: white !important;
#     }
#     button:focus {
#         outline: none !important;
#         box-shadow: none !important;
#         color: black !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

st.write("<a href='#' id='my-link'>Click me</a>", unsafe_allow_html=True)

if st.button("my-link"):
    st.write("Link clicked!")
    
    

if st.button("Click me", type="primary"):
    st.write("Clicked")

st.button("Another button!")

# st.markdown(
#     """
#     <style>
#     button[kind="primary"] {
#         background: none!important;
#         border: none;
#         padding: 0!important;
#         color: black !important;
#         text-decoration: none;
#         cursor: pointer;
#         border: none !important;
#     }
#     button[kind="primary"]:hover {
#         text-decoration: none;
#         color: black !important;
#     }
#     button[kind="primary"]:focus {
#         outline: none !important;
#         box-shadow: none !important;
#         color: black !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

def foo():
    st.toast("Button clicked", icon="🚀")
    
if stateful_button("Button 1", key="button1"):
    if stateful_button("Button 2", key="button2"):
        if stateful_button("Button 3", key="button3"):
            st.write("All 3 buttons are pressed")
            

with stylable_container(key="my_unique_button",css_styles="""
{
    [data-testid="baseButton-primary"] {
        box-shadow: 0px 10px 14px -7px #3e7327;
        background-color:#77b55a;
        border-radius:4px;
        border:1px solid #4b8f29;
        display:inline-block;
        cursor:pointer;
        color:#ffffff;
        font-family:Arial;
        font-size:13px;
        font-weight:bold;
        padding:14px 31px;
        text-decoration:none;
        text-shadow:0px 1px 0px #5b8a3c;
    }
    [data-testid="baseButton-primary"]:hover {
        # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
        background-color:#72b352;
        background-color: red;
        cursor: arrow;
    }
    [data-testid="baseButton-primary"]:active {
        position:relative;
        background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
        top:1px;
    }
}
""",):
    st.button("button", type='primary', on_click=foo)


with stylable_container(key="payment_button",css_styles="""
{
    [data-testid="baseButton-primary"] {
        box-shadow: 0px 10px 14px -7px #3e7327;
        background-image:url("data/qrcode_1.png") fixed center;
        border-radius:4px;
        border:1px solid #4b8f29;
        display:inline-block;
        cursor:pointer;
        color:#ffffff;
        font-family:Arial;
        font-size:13px;
        font-weight:bold;
        padding:14px 31px;
        text-decoration:none;
        text-shadow:0px 1px 0px #5b8a3c;
    }
    [data-testid="baseButton-primary"]:hover {
        # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
        background-color:#72b352;
        background-color: red;
        cursor: arrow;
    }
    [data-testid="baseButton-primary"]:active {
        position:relative;
        background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
        top:1px;
    }
}
""",):
    st.button("button", type='primary', on_click=foo, key="payment")

import streamlit.components.v1 as components

src_100K = 'https://pay.sumup.com/b2c/Q8F8EX3C'
src_max = "https://pay.sumup.com/b2c/QKLGKAHL"
src_101 = "https://pay.sumup.com/b2c/QDJLWO13"
src_free = "https://pay.sumup.com/b2c/Q2RYJEC8"

from streamlit_modal import Modal
from streamlit import rerun as rerun  # type: ignore

class _Modal(Modal):
    def open(self, **kwargs):
        print(kwargs)
        if 'src' in kwargs:
            self.src = kwargs['src']
            print(self.src)
        st.session_state[f'{self.key}-opened'] = True
        st.session_state[f'{self.key}-src'] = kwargs['src']
        rerun()


modal = _Modal(
    "There is no _______ without consent.", 
    key="demo-modal",
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)

open_modal = st.button("Consent: 100K")
open_modal2 = st.button("Consent: Max")
# open_modal = st.button("Consent: 101")
# open_modal = st.button("Consent: free")

if open_modal:
    modal.open(src=src_100K)

if open_modal2:
    modal.open(src=src_max)

if modal.is_open():
    with modal.container():
        # st.write(modal)
        # st.write(st.session_state[f'{modal.key}-src'])
        # if hasattr(modal, 'src'):
        #     st.toast(modal.src)
        #     st.balloons()
        #     components.iframe(modal.src, height=1500)
        components.iframe(st.session_state[f'{modal.key}-src'], height=1500)
