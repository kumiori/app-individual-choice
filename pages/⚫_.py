import streamlit.components.v1 as components
import streamlit as st
import pandas as pd

import sys
sys.path.append('pages/')

from test_multicomponents import dichotomy
# qualitative, qualitative_parametric

st.set_page_config(
    page_title="Celestial Verse Portal",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

tabs = ["Celestial Portal", "Cosmic Odyssey", "Cosmic Revelations"]

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)

# def dichotomy(name, question, key=None):
#     return _qualitative_selector(component = "dichotomy",
#     name = name,
#     key=key,
#     question = question)


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
    st.markdown("## Motivation")
    st.write(
        "The **Celestial Verse Portal** aims to provide users with a unique and immersive experience, guiding them through a cosmic journey of self-realization. The motivation behind this app is to blend the fascination of exploring the mysteries of the universe with the introspection of one's thoughts and feelings. By intertwining the celestial wonders with personal reflections, the app offers a novel approach to self-discovery."
    )



# Cosmic Odyssey Section
def cosmic_odyssey():
    st.header('Cosmic Odyssey')
    st.write(
        "Embark on a celestial odyssey through the cosmos. "
        "Explore the mysteries of stars, galaxies, and the poetry written in the language of the universe."
    )
    
    return_value = qualitative(name = "Spirit", question = "How tricky is Quantity?", data_values = [1, 2, 10, 11, 25], key = "qualitative")
    st.write('You picked me:', return_value)

    st.markdown("## Unique Advantages")
    st.write(
        "- **Immersive Cosmic Experience:** Unlike traditional self-realization apps, the Celestial Verse Portal provides a unique blend of cosmic exploration and personal reflection. Users are not only guided through celestial wonders but also encouraged to introspect based on cosmic themes."
        "\n\n"
        "- **Diverse Interaction:** The app offers various interaction components, including dichotomies, qualitative responses, and parametric inputs. This diversity ensures that users can express their thoughts in nuanced ways, capturing the intricacies of their cosmic journey."
        "\n\n"
        "- **Personalized Celestial Profiles:** As users engage with the app, their responses contribute to the creation of personalized celestial profiles. These profiles reflect the user's unique cosmic perspective and serve as a testament to their celestial voyage."
        "\n\n"
        "- **Seamless Navigation:** The use of Streamlit and tabs ensures a seamless and intuitive navigation experience. Users can effortlessly transition between different cosmic sections, enhancing overall usability."
    )
    
    st.markdown("## Scope")
    st.write(
        "The Celestial Verse Portal consists of three main sections:"
        "\n\n"
        "1. **Celestial Portal:** Embark on a cosmic journey, exploring the wonders of the universe. Users can engage in a dichotomy to understand their spiritual boundaries, offering a glimpse into their cosmic inclinations."
        "\n\n"
        "2. **Cosmic Odyssey:** Delve deeper into the mysteries of stars and galaxies. Users are prompted to provide qualitative responses, reflecting their understanding of cosmic quantities and the intricacies of the celestial realm."
        "\n\n"
        "3. **Cosmic Revelations:** Unveil the secrets discovered during the celestial odyssey. This section prompts users to share their insights through qualitative parametric responses, allowing for a nuanced exploration of their perceptions."
    )

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

    st.markdown("## Explore the Cosmos Within")
    st.write(
        "The Celestial Verse Portal invites users to embark on a journey of cosmic self-realization. By fusing the marvels of the universe with personal reflections, this app promises an unparalleled experience of discovering the cosmos within. Whether you're pondering spiritual boundaries, contemplating cosmic quantities, or unveiling profound revelations, the Celestial Verse Portal is your guide to a celestial odyssey of self-discovery. ✨"
    )

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
