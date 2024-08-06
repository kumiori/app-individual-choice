import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="What the Fuck is going on?",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

import streamlit.components.v1 as components
import pandas as pd

import sys
sys.path.append('pages/')
from test_multicomponents import dichotomy


tabs = ["Celestial Portal", "Release Odyssey", "Cosmic Revelations"]

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)



def qualitative(name, question, data_values, key=None):
    return _qualitative_selector(component = "qualitative",
    name = name,
    key=key,
    data_values = data_values,
    question = question)

def qualitative_parametric(name, question, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    key=key,
    areas = areas,
    data_values  = [1, 3, 10],
    question = question)

def home():
    st.title("Welcome to the Home Page!")
    st.write("This is the home page content.")

def about():
    st.title("About Us")
    st.write("Learn more about our company on this page.")


def contact():
    st.title("Contact Us")
    st.write("Reach out to us through the contact page.")

# App
# def main():
#     st.sidebar.title("Navigation")
#     tabs = ["Home", "About", "Contact"]
#     selected_tab = st.sidebar.radio("Select Page", tabs)

#     if selected_tab == "Home":
#         home()
#     elif selected_tab == "About":
#         about()
#     elif selected_tab == "Contact":
#         contact()

# Initialize a DataFrame to store celestial responses
celestial_responses = pd.DataFrame(columns=['Star', 'Galaxy', 'Interest in Constellations', 'Stellar Feedback'])

# Celestial Portal
def celestial_portal():
    st.title('# What-the-Fuck-is-going-on?')
    st.subheader("Please, welcome my F-French...")
    st.write(
        "Committed in code, ... "
        "Embark on wonders of the universe."
    )
    # Add any additional cosmic content here
    
    
    inverse_choice = lambda x: 'OK 🥲' if x == 0 else 'NOK ⚠︎' if x == 1 else 'in-between ✨'
    
    
    col1, col2, col3 = st.columns([3, .1, 1])

    with col1:
        return_value = dichotomy(name = "Spirit", question = "Boundaries matter, see below...", key = "boundaries")

    with col3:
        st.markdown(f'## Your choice <code>chooses</code> {return_value}', unsafe_allow_html=True)
        if return_value:
            st.write('Which, for us, is something like...')
            st.markdown(f'## {inverse_choice(float(return_value))}')


def download_crac():
    pdf_url = "https://drive.google.com/file/d/133jCZb3VUNkrLnte2IB6zgzNWjkvEyYk/view?usp=drive_link" 

    pdf_description = """This my last yearly assesment of my scientific activity, it is evaluated yearly
    by the National Commission of Scientific Research (CoNRS) in France. All fine? Here's the catch: I 
    publish very little, and for a reason. For this reason, I am not a good fit for a system that blindly pressures for scientific production, regardless of its interest, especially if not economically relevant. Psychological harassment is a real thing, it can go very deep: my examples are by experience on a daily..."""

    # Download button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        download_button = f'<a href="{pdf_url}" download="sample.pdf">' \
                      f'<button style="padding: 10px; background-color: #4CAF50; color: white; ' \
                      f'border: none; border-radius: 5px; cursor: pointer;">Download REPORT</button></a>'

        st.markdown(download_button, unsafe_allow_html=True)
    st.write(pdf_description)

# Cosmic Odyssey Section
def cosmic_odyssey():
    st.header('A Release Odyssey')
    st.write(
        "Embark on a celestial odyssey through the cosmos. "
        "Explore the mysteries of stars, galaxies, and the poetry written in the language of the universe."
    )
    
    return_value = qualitative(name = "Spirit", question = "How tricky is Quantity?", data_values = [1, 2, 10, 11, 25], key = "qualitative")
    st.write('You picked me:', return_value)

# Cosmic Revelations Section
def cosmic_revelations():
    st.header('Revelations: Who am I, from the outside?')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        st.write("## Under pressure and constraints")
        download_crac()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("## Motivation")
        st.write(
            "Commit(ment)s are fragments of a testament, turned into mental. They reveal the inner workings and hidden secrets of a coder layering invisible structure. It's always an Odyssey, of sorts."
            "My scientific profile appears to cover a broad spectrum of disciplines, showcasing a diverse range of interests and expertise. I am a theoretician, my thinking is abstract. My activity is flexible, smooth, a constant progression in difficulty."
            "This is my journey, through the layering of logic tasks, delving into their nature springing from the dark, to witness the dawn of new ecstatic revelations."
        )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:

        st.write(
            'I have decided to extend my involvement in areas such as political economy, power dynamics, knowledge in general, legitimacy, mathematical theory, number theory, astronomy, behavioural sciences, mythology, psychological analysis, beyond mathematical functional analysis. This, with the intention of an harmonious growth and learning process.'
        )
        st.write('In many ways when it comes to learning, I am `savage` like ~ a thrilled child.')

    col1, col2, col3 = st.columns([3, .1, 1])

    with col1:
        return_value = qualitative_parametric(name = "welcome the Spirit",
            question = "Boundaries matter, see below...",
            areas = 3,
            key = "parametric")
    with col3:
        st.write('You picked me:', return_value)

# Streamlit app with cosmic tabs
def main():
    st.title('Commits and commitments made transparent.')
    st.markdown("### Is <code>raw</code> expression welcome? If not, why not?", unsafe_allow_html=True)

    # Create tabs

    _tabs = st.tabs(tabs)

    # Display content based on selected tab
    # Traverse through cosmic tabs and unveil celestial wonders
    for i, selected_tab in enumerate(tabs):
        with _tabs[i]:
            if selected_tab == "Celestial Portal":
                celestial_portal()
            elif selected_tab == "Release Odyssey":
                cosmic_odyssey()
            elif selected_tab == "Cosmic Revelations":
                cosmic_revelations()

# Run the cosmic app
if __name__ == "__main__":
    main()
