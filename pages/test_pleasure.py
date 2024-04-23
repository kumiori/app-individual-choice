import streamlit as st
import streamlit.components.v1 as components
import hashlib
import datetime

from streamlit_vertical_slider import vertical_slider 
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
from pages.test_settimia import fetch_and_display_data
from pages.test_location import conn
from pages.test_paged import PagedContainer
# from pages.test_game import display_dictionary_by_indices

from pages.test_discourse import display_dictionary_by_indices, display_details_description, CustomStreamlitSurvey, _PagedContainer, _dichotomy, _qualitative, hash_text, _stream_example, _stream_once, match_input, create_button, create_dichotomy, create_qualitative, create_yesno, create_next, create_globe, create_textinput, create_checkbox, create_equaliser, display_category_description

with open("pages/discourse.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write(f.read())
  


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

survey = CustomStreamlitSurvey()

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
)


Dichotomy = ss.SurveyComponent.from_st_input(_dichotomy)
VerticalSlider = ss.SurveyComponent.from_st_input(vertical_slider)
ParametricQualitative = ss.SurveyComponent.from_st_input(_qualitative)

# Initialize read_texts set in session state if not present
if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

if "current_booklet_page" not in st.session_state:
    st.session_state["current_booklet_page"] = 0
    
intro_text = """
## Our questions are simple: _we don't want a ________ study._ This is why we engage.
## We _________ constructing new _________ and implement ideas based on collective understanding.
## To broaden and articulate a vision of imminent social transitions...have you enrolled yet?

#### Details follow, _just_ use the top arrow [>] 
"""

panel_1 = """ ## We face an ________ characterised by _________.

## These ________ are not only ________ but often _____________.

 ## Do they emerge as facets of a deeper `organic` crisis?
 
## Excited to continue? Does this make any sense to you?

""" 
panel_2 = """

## We are organising a panel discusion at _Europe in Discourse_ conference in Athens, 2024.

## Our panel springs at the intersection of Human Sciences, Natural Sciences, Philosophy, and Arts, offering an opportunity to build a concrete perspective in addressing uncertainty, confusion, and risk.

## ..._to bring forward_ an emancipatory vision of change.

## What do you think? Are we on the right path?

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

panel = [intro_text, panel_1]

challenges = [
    ("Productive Innovation", ""),
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

widget_info = [
    {"type": "next", "key": "next"},
    {"type": "yesno", "key": "opinion_counts"},
    {"type": "dichotomy", "key": "dichotomy_1"},
    {"type": "button", "key": "Let's..."},
    {"type": "equaliser", "key": "equaliser", "kwargs": {"data": challenges[0:3]}},
    {"type": "textinput", "key": "location"},
    {"type": "globe", "key": "Singular Map"},
    {"type": "qualitative", "key": "quali"},
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
    "yesno": create_yesno,
    "qualitative": create_qualitative,
    "equaliser": create_equaliser,
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
    
    if 'damage_parameter' not in st.session_state:
        st.session_state.damage_parameter = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter


    # once usage:
    # streamwrite(_stream_once(intro_text, 0))
    # st.markdown()
    now = datetime.datetime.now()
    st.markdown(f"# _Today_ is {now.strftime('%A')}, {now.strftime('%d')} {now.strftime('%B')} {now.strftime('%Y')}")
    st.markdown("_Now_ is time for `Pleasure & Growth >` be welcome: brought to you by ______")


    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Enrolling...", "Ideas", "Connect", "Minimal Glossary", "Frequency Asked Questions", "References"])
    
    with tab1:        

        for p, (i, info)  in zip(panel, enumerate(widget_info)):
            widget_key = info["key"]
            widget_type = info["type"]
            widget_kwargs = info["kwargs"] if "kwargs" in info else {}

            st.markdown(p)
            if widget_type in widget_creators:
                widget_dict[widget_key] = widget_creators[widget_type](widget_key, kwargs = widget_kwargs)

            st.divider()
            
    st.write(st.session_state.read_texts)

    with tab3:        
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

    with tab2:
        st.markdown("# Ideas, tutorials, sessions, so far")
        contributions()

    with tab4:
        st.markdown("## Minimal Glossary")
        glossary()

    with tab5:
        st.markdown("## Frequently Asked Questions")

    with tab6:
        st.markdown("## The bounty")
        references()

    return survey

def contributions():
    
    ideas_dict = {
        "# Idea": {"### `growth` \n ## Potentials, determined"},
        "## tba": {"### Andrés León Baldelli"},
    }

    paged_container = _PagedContainer(ideas_dict, items_per_page=2, show_pagination = False)

    with st.container():
        col1, _, col2 = st.columns([2, 10, 2])
        with col2:
            if st.button("Next"):
                st.session_state["current_booklet_page"] = min(st.session_state.current_booklet_page + 1, paged_container.get_total_pages() - 1)
        with col1:
            if st.button("Prev"):
                st.session_state["current_booklet_page"] = max(st.session_state.current_booklet_page - 1, 0)

        paged_container.display_page(st.session_state.current_booklet_page)
        
            
    return

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
        ":ticket:  Visit the conference's website",
        "https://www.europeindiscourse.eu/",
        use_container_width=True,
    )

    return
    
def faq():
    return

def references():
    with st.expander("Show all the data", expanded=False):
        st.write("Survey Data:")
        st.json(survey.data, expanded=True)

        
    references_dict = {
        "# Book #1": {"### `growth` \n ## Potentials, determined"},
        "# Book #2": {"### ..."},
        "# Docu #0": {"### ..."},
        "# Event #3": {"### ..."},
        "# Story #4": {"### ..."},
    }

    display_dictionary(references_dict)
    
    return

if __name__ == "__main__":
    
    survey = main()
    # add_vertical_space(1)
    # more()
    
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

    st.markdown("""## A _________ bringing forward an emancipatory vision of _pleasure_ and `growth`... \n
        On est dans la merde
        On est revenus a un état de chaos dans les 
    relations _________...
                
                """)
    st.markdown("## Would you like to join?")


    return_value = survey.dichotomy(name="", 
                                label="Confidence",
                                question="...", 
                                key="boundaries")
