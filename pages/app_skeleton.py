import streamlit as st


st.set_page_config(
    page_title="Celestial Verse Portal",
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


tabs = ["Celestial Portal", "Cosmic Odyssey", "Cosmic Revelations"]

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
    data_values  = [1, 2, 10],
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
    st.title('Celestial Verse Portal')
    st.write(
        "Welcome to the Celestial Verse Portal. "
        "Embark on a cosmic journey through the tabs below and uncover the wonders of the universe."
    )
    # Add any additional cosmic content here
    return_value = dichotomy(name = "Spirit", question = "Boundaries matter, see below...", key = "boundaries")
    st.write('You picked me:', return_value)


# Cosmic Odyssey Section
def cosmic_odyssey():
    st.header('Cosmic Odyssey')
    st.write(
        "Embark on a celestial odyssey through the cosmos. "
        "Explore the mysteries of stars, galaxies, and the poetry written in the language of the universe."
    )
    
    return_value = qualitative(name = "Spirit", question = "How tricky is Quantity?", data_values = [1, 2, 10, 11, 25], key = "qualitative")
    st.write('You picked me:', return_value)

# Cosmic Revelations Section
def cosmic_revelations():
    st.header('Cosmic Revelations')
    st.write(
        "Reveal the celestial secrets unveiled during the Celestial Verse Odyssey. "
        "Journey through the profiles of cosmic poets, delve into their verses, and witness the dawn of new astronomical revelations."
    )

    return_value = qualitative_parametric(name = "Spirit",
        question = "Boundaries matter, see below...",
        areas = 3,
        key = "parametric")
    st.write('You picked me:', return_value)

# Streamlit app with cosmic tabs
def main():
    st.title('Celestial Verse Portal')

    # Create tabs

    _tabs = st.tabs(tabs)

    # Display content based on selected tab
    # Traverse through cosmic tabs and unveil celestial wonders
    for i, selected_tab in enumerate(tabs):
        with _tabs[i]:
            if selected_tab == "Celestial Portal":
                celestial_portal()
            elif selected_tab == "Cosmic Odyssey":
                cosmic_odyssey()
            elif selected_tab == "Cosmic Revelations":
                cosmic_revelations()

# Run the cosmic app
if __name__ == "__main__":
    main()
