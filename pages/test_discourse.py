import streamlit as st
import streamlit.components.v1 as components
from  streamlit_vertical_slider import vertical_slider 
import hashlib
from pages.test_1d import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from pages.test_injection import CustomStreamlitSurvey
from streamlit_extras.streaming_write import write as streamwrite 
import time
import string
import streamlit_survey as ss
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
import random
import numpy as np

if st.secrets["runtime"]["STATUS"] == "Production":
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

st.write(st.secrets["runtime"]["STATUS"])


_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)

def _dichotomy(name, question, label, rotationAngle = 0, gradientWidth = 40, invert = False, shift = 0, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    label = label,
    key=key,
    question = question,
    rotationAngle = rotationAngle,
    gradientWidth = gradientWidth,
    invert = invert,
    shift = shift
    )

Dichotomy = ss.SurveyComponent.from_st_input(_dichotomy)
VerticalSlider = ss.SurveyComponent.from_st_input(vertical_slider)

class CustomStreamlitSurvey(ss.StreamlitSurvey):
    shape_types = ["circle", "square", "pill"]

    def dichotomy(self, label: str = "", id: str = None, **kwargs) -> str:
        return Dichotomy(self, label, id, **kwargs).display()
    
    def equaliser(self, label: str = "", id: str = None, **kwargs) -> str:
        return VerticalSlider(self, label, id, **kwargs).display()

# Usage example


# Initialize read_texts set in session state if not present
if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def _stream_once(text, damage):
    text_hash = hash_text(text)

    # Define sleep lengths for different punctuation symbols
    sleep_lengths = {'.': 1., ',': 0.3, '!': 1.7, '?': 1.5, ';': 0.4, ':': 0.4}
    sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}
    # st.json(sleep_lengths)

    # st.write(sleep_lengths.values() * (1+damage))

    # Check if the text has already been read
    if text_hash not in st.session_state.read_texts:
        # st.write(text)
    
        for i, word in enumerate(text.split()):
            # Check if the last character is a punctuation symbol
            last_char = word[-1] if word[-1] in string.punctuation else None

            # Yield the word with appropriate sleep length
            if last_char == '.' or last_char == '?' or last_char == '^':
                yield word + " \n "
            else:
                yield word + " "
            
            if last_char and last_char in sleep_lengths:
                time.sleep(sleep_lengths[last_char])
            else:
                time.sleep(0.3)
            
        st.session_state.read_texts.add(text_hash)  # Marking text as read

def create_streamed_columns(panel):
    num_panels = len(panel)
    
    for i in range(num_panels):
        width_pattern = [2, 1] if i % 2 == 0 else [1, 2]
        cols = st.columns(width_pattern)

        col_idx = 0  if i % 2 == 0 else 1
        with cols[col_idx]:
            streamwrite(_stream_once(panel[i], 0))

def match_input(input_text, translation_dict):
    if not input_text:
        return None
    
    matching_keys = [key for key, value in translation_dict.items() if value.lower() == input_text.lower()]

    if matching_keys:
        return matching_keys
    else:
        return False

intro_text = """
## Our questions are simple.

## Have you been invited yet?
"""

panel_1 = """ ## We face an international landscape characterised by simultaneous and juxtaposed crises often described as '_polycrises'_...

""" 
panel_2 = """
## These crises are not only juxtaposed but often interconnected as much in their effects as in their causes. 
"""
panel_3 = """ ## They emerge as facets of a deeper “organic crisis”."""

panel_4 = """## Development Cooperation Review  Vol. 6 - Special Issue - opens to New Hopes...

## _That issue_ was published at a crucial, _timely_ time...

## As a response, we are organising a panel discusion at the next Europe in Discourse conference in Athens, 2024.

"""

panel_5 = """## Our panel springs at the intersection of Human Sciences, Natural Sciences, Philosophy, Performance, and Arts, offering an opportunity to build a concrete perspective in addressing uncertainty, confusion, and risk.

## To bring forward an emancipatory vision of change...

"""

panel_6 = """
## we deploy an interactive digital platform as a framework to discuss and connect.

## _To be clear, the task is difficult:_  
## _..."these are not easy times for multilateral cooperation_ and _there is more than a list of policies to be considered."_
"""

panel_7 = """
## You can take _this_ as an opportunity,
## we have taken this as a challenge...

"""

panel_8 = """
## We are constructing a versatile coordination tool, and we need your help.

## Are you happy to engage?
## Are you ready to participate? 

## We'll tell you more about all in a moment...

## Our simple platform is multi-purpose and inclusive by design, 

## To use it, we start questioning the channels and the structures through which we relate and the interfaces through which we communicate. 

## As we invite your free and conscious participation, just a reminder:
 our platform is 'free software' in the sense that has a lot to do with freedom, and nothing with price.
 

"""

yesses = {
    "Albanian": "po",
    "Basque": "bai",
    "Belarusian": "ды",
    "Bosnian": "da",
    "Bulgarian": "да",
    "Catalan": "si",
    "Corsican": "Iè",
    "Croatian": "Da",
    "Czech": "Ano",
    "Danish": "Ja",
    "Dutch": "Ja",
    "Estonian": "jah",
    "Finnish": "Joo",
    "French": "Oui",
    "Frisian": "ja",
    "Galician": "Si",
    "German": "Ja",
    "Greek": "Ναί",
    "Hungarian": "Igen",
    "Icelandic": "Já",
    "Irish": "yes",
    "English": "yes",
    "Italian": "sì",
    "Italian": "si",
    "Latvian": "jā",
    "Lithuanian": "taip",
    "Luxembourgish": "Jo",
    "Macedonian": "Да",
    "Maltese": "iva",
    "Norwegian": "ja",
    "Polish": "tak",
    "Portuguese": "sim",
    "Romanian": "da",
    "Russian": "да",
    "Scots Gaelic": "Tha",
    "Serbian": "да",
    "Slovak": "Áno",
    "Slovenian": "ja",
    "Spanish": "sí",
    "Swedish": "ja",
    "Tatar": "әйе",
    "Ukrainian": "так",
    "Welsh": "ie",
    "Yiddish": "יאָ",
}

panel = [panel_1, panel_2, panel_3, panel_4, panel_5, panel_6, panel_7, panel_8]

# Main function
def main():
    # Page title
    # st.title(":circus_tent: Europe in Discourse")
    # st.title(":fountain: Athens Conference, :satellite: 2024")
    st.markdown("## A panel discussion bringing forward an emancipatory vision of change...")
    st.markdown("## Would you like to participate?")
    # Session State also supports attribute based syntax

    # survey = ss.StreamlitSurvey("Home")
    col1, col2, col3 = st.columns(3)
    survey = CustomStreamlitSurvey()

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    if 'damage_parameter' not in st.session_state:
        st.session_state.damage_parameter = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter


    # once usage:
    # streamwrite(_stream_once(intro_text, 0))
    st.markdown(intro_text)
    return_value = survey.dichotomy(name="Spirit", 
                                label="Confidence",
                                question="Dychotomies, including time...", 
                                key="boundaries")

    [st.markdown(p) for p in panel]
    st.write(st.session_state.read_texts)
    
    col1, _, col2 = st.columns([3, 0.1, 1.5])

    with col1:
        st.markdown("## Are you happy...to interact?")
    with col2:
        response = survey.text_input("Try to respond in your natural language...", help="Our location will appear shortly...", value="")
        result = match_input(response, yesses)
    st.write(result)
    if result:
        st.write(f"Wonderful! We are happy to chime ✨")
        st.write(f"Your response is: {print_languages(result)}")
        st.success(f"Your response is: {result[0]}")
    elif result is False:
        st.error("We are always here...")
    elif result is None:
        st.info('All other non-intelligible input is considered as a \'no\'.')

    return survey

def display_category_description(category, description):
    """
    Function to display category and its description.
    """
    col1, col2 = st.columns([2, 4])
    with col1:
        # st.markdown(f"**{category}**")
        st.markdown(f"{category}")
    with col2:
        st.write(description)
    st.write("---")

def print_languages(languages):
    if "English" in languages:
        st.write("x")
    else:
        st.write(", ".join(f"{language}" for language in languages[0::-1]), f"and {languages[-1]}")

if __name__ == "__main__":
    survey = main()
    # add_vertical_space(1)

    st.markdown("## Panel contributions so far...")
    
    booklet = [
        ("## (Pop’Ecologie)", "Ariane Ahmadi"),
        ("## Aftermath Of Political Violence", "Sophie Wahnich"),
        ("## Engagement with the Sea", "Antonia Taddei"),
        ("## tba", "Gabrielle Dyson"),
        ("## Pulse", "Giorgio Funaro"),
        ("## We Are Enough", "Roger Niyigena Karera"),
        ("## Rethinking Solutions", "Graziano Mazza"),
        ("## tba", "Andrés León Baldelli"),
    ]
    
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

    challenges = [
        ("Productive transformation and Innovation", ""),
        ("Global Value Chains", ""),
        ("Artificial intelligence", ""),
        ("Farmers and Development", ""),
        ("Climate Change", ""),
        ("Adaptation and Finance", ""),
        ("Social Migration", ""),
        ("The Social Contract", ""),
        ("Cooperation Reinvented", ""),
        ("Values, Inequalities, and Sustainability", ""),
        ("Food system concerns", ""),
        ("Endogenous Solutions", "")
    ]
    
    for author, title in booklet:
        display_category_description(author, title)

    st.divider()
    
    st.markdown("#### We are happy to share more and connect")
    links_row = row(2, vertical_align="center")
    links_row.button(
        ":honey_pot: Explore our panel contributions",
        use_container_width=True,
    )
    links_row.link_button(
        ":ticket:  Visit the conference's website",
        "https://www.europeindiscourse.eu/",
        use_container_width=True,
    )

    st.markdown("## What are the priorities? Helping timescales appear.")
    st.markdown("""## Help us gauge the priorities of the community

    ## We start a joint conversation to harmonise time scales, asking your view of priorities from 0 to 100
    
    ## This is not a random test.

    ## Remark: the initial state is random, but the final state will not be""")

    rows = 3
    split_len = len(challenges) // rows
    bottom_cols = st.columns(split_len)

    for j in range(rows):
        with st.container():
            for i, column in enumerate(bottom_cols):
                with column:
                    survey.equaliser(
                        label=challenges[i + j*split_len][0],
                        height=200,
                        key=f"cat_{i}_{j}",
                        default_value = int(random.random() * 100),
                        step=1,
                        min_value=0,
                        slider_color=('red','white'),
                        thumb_shape="circle",
                        max_value=100,
                        value_always_visible=True,
                    )
    
    st.markdown("## Minimal Dictionary")

    for category, description in categories:
        display_category_description(category, description)
    

    st.markdown("## References")
    st.write("Survey Data:", survey.data)
