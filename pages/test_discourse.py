import streamlit as st
import datetime
import time
from streamlit_extras.add_vertical_space import add_vertical_space 

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
    </style>
    """,
        unsafe_allow_html=True,
    )

st.write(st.secrets["runtime"]["STATUS"])

from lib.texts import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from lib.survey import CustomStreamlitSurvey
from streamlit_extras.streaming_write import write as streamwrite 
import time
import string
import streamlit_survey as ss
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
import random
from lib.presentation import PagedContainer
# from pages.test_game import display_dictionary_by_indices
# from pages.test_pleasure import display_dictionary

from lib.matrices import generate_random_matrix, encode_matrix, display_matrix
from lib.dictionary_manip import display_dictionary, display_dictionary_by_indices, display_details_description
from lib.survey import CustomStreamlitSurvey
update_frequency = 500  # in milliseconds
from lib.texts import match_input
from lib.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_next, create_globe, create_textinput, create_checkbox, create_equaliser, fetch_and_display_data, conn
from pages.test_footer import footer
with open("pages/discourse.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write(f.read())
    
class _PagedContainer(PagedContainer):

    def display_page(self, page):
        start_idx = page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_items = [start_idx, end_idx]

        display_dictionary_by_indices(self.items, indices=page_items)
    
        if self.show_pagination:
            st.write(f"Page {page + 1}/{self.get_total_pages()}")


class ConnectingContainer(PagedContainer):
    def display_page(self, page):
        page_item = list(self.items)[page]
        (panel, widget_info) = page_item
        st.markdown(panel)
        widget_key = widget_info["key"]
        widget_type = widget_info["type"]
        widget_kwargs = widget_info["kwargs"] if "kwargs" in widget_info else {}
        if widget_type in widget_creators:
            widget_dict[widget_key] = widget_creators[widget_type](widget_key, kwargs = widget_kwargs)

        # for item in self.items:
        #     (panel, widget_info) = item
        #     st.markdown(panel)

        #     st.divider()
            

        pass
        # return super().display_page(page)

survey = CustomStreamlitSurvey()

print(dir(survey))
if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

if "current_booklet_page" not in st.session_state:
    st.session_state["current_booklet_page"] = 0

if "current_discourse_page" not in st.session_state:
    st.session_state["current_discourse_page"] = 0

intro_text = """
## Our questions are simple: _we don't want a bored audience._ This is why we engage.
## We elicit participation constructing new narratives and implement ideas based on collective understanding.
## To broaden and articulate a vision of imminent social transitions...have you been invited yet?


#### Details follow, _just_ use the top arrow [>] 
"""

panel_1 = """ ## We face an international landscape characterised by simultaneous and juxtaposed crises often described as '_polycrises'_.

## These crises are not only juxtaposed but often interconnected as much in their effects as in their causes.

 ## They emerge as facets of a deeper `organic` crisis.
 
## How do you feel? Does this make any sense to you?

""" 
panel_2 = """

## We are organising a panel discusion at _Europe in Discourse_ conference in Athens, 2024.

## Our panel springs at the intersection of Social Sciences, Natural Sciences, Philosophy, and Arts, offering an opportunity to build a concrete perspective in addressing uncertainty, confusion, and risk.

## ..._to bring forward_ an emancipatory vision of change.

## What do you think? Are we on the right path?

"""

panel_3 = """ 

## Everything seems to lie upon a notion of change and connection.

## _"these are not easy times for multilateral cooperation_ and _there is more than a list of policies to be considered."*_

\* `Development Cooperation Review  Vol. 6 - Special Issue` - opening to _new hopes_...in the context of international cooperation.
## ... Pez ...

## _That issue_ was published at a crucial time. We decide to engage in a conversation in which you participate.

### Your opinion counts, `right`?"""
 
panel_4 = """

## To integrate a bigger picture, help us make sense of time scales and policy priorities.

## Think (or picture) a _global social transition_: should this be fast or slow, or a mix of both?

"""

panel_4_bis = """

## Thank...

## Think (or picture) a _global social transition_: should this be fast or slow, or a mix of both?

"""

panel_5 = """

## We are constructing a versatile direct coordination tool, an interactive digital platform as a framework to discuss and connect. 

## _To be clear_, the task is difficult: we need your input.

## You can take _this_ as an opportunity to express, we have taken this as a challenge to address.

## Let's play: what is your perception of priority levels?

"""

panel_6 = """
## The following is a list of `social dimensions` or policy concerns. Match the sliders with your perception of priority levels.

##### This is a great exercise in making communication effective, actionable, and visual.

### These aspects are core for us: 


"""

panel_7_bis = """Matrix viz.."""

panel_7 = """

## Your conscious input is precious, and energy naturally flows where is most needed. Thank you for your participation. What's your name?

## We are trying to understand why the world is in a state of fracture on several levels: individual, social and universal.

## Human beings no longer meet in ideas. How do patterns behave?

## This is how we think: _matrix is a map where patterns emerge_

[MATRIX]

##  But maybe you are used to different types of map...

![Two dimensional bounded projection](https://i.imgur.com/XlMGG76.png)

this is Paris

## Where are you, at the moment? Where do you live now? mainly host you in the next two years? X Where are you now?

"""

panel_8 = """


## Here and Now, our commitment is towards action.

## As we invite your free and conscious participation, let's treasure this moment of exchange.

## How to visualise a bigger picture? 

## Verify your location and local time. You will receive an access key to join the conversation.

# access key: `[here] x [now]` 
# [ I {NAME} CONNECT here and now ]

`st.success(f"This is your signature \n`` {signature} ``. Keep it in your files, it will allow swift access to the past.")`


"""

panel_9 = """

## Welcome, _________. 
## We are happy to have you here. You may have a lot of questions, we have a few too.
## How to connect, - _where_ do we connect from?

"""

panel_10 = """

We are oraganising...
Our panel
free software

Would you like to have agency on decisions that (indirectly) concern you?

Would you like to increase your agency in decisions that concern others?

"""

panel_11 = """

## Your preferences have been checkpointed.
## Feel free to come again in a few days to test your access key

## In the meantime, we are reconstructing our links to backend.

## In {city} it's {weather} and {temperature} degrees. Happy to leave us a message or share a feedback? //`prematuro?`

"""

panel_12 = """

qualitative
    - feedback/support/contribute

quantitative (how much: 0-100)
    - sliders

## Wishing you well, we are happy to share and develop with you,
## this is our email: [email]. Looking forward.

"""

sandbox = """
## We'll tell you all about it in a moment...

## Are you happy to engage?
## Are you ready to participate? 
## Where are you located? 
## Does this sound like a _good idea_? 


## Our simple platform is multi-purpose and inclusive by design, 

## To use it, we start questioning the channels and the structures through which we relate and the interfaces through which we communicate. 

## As we invite your free and conscious participation, just a reminder:
 our platform is 'free software' in the sense that has a lot to do with freedom, and nothing with price.

"""

""" `We have accepted explosion of information, are you willing to accept explosion of undertsanding?`

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

panel = [intro_text, panel_1, panel_2, panel_3, panel_4,  panel_5, panel_6,  panel_7,  panel_8,
         panel_9, panel_10, panel_11, panel_12]

challenges = [
    ("The Social Contract", ""),
    ("Cooperation Reinvented", ""),
    ("Inequalities and Sustainability", ""),
    ("The next Olympic games", ""),
    ("Climate Change", ""),
    ("Global Value Chains", ""),
    ("Productive Innovation", ""),
    ("Artificial intelligence", ""),
    ("Farmers and Development", ""),
    ("Adaptation and Finance", ""),
    ("Social Migration", ""),
    ("Food system concerns", ""),
    ("Endogenous Solutions", "")
]

widget_info = [
    {"type": "next", "key": "next", "kwargs": {"survey": survey}},
    {"type": "yesno", "key": "button_0", "kwargs": {"survey": survey}},
    {"type": "yesno", "key": "button_1", "kwargs": {"survey": survey}},
    {"type": "yesno", "key": "opinion_counts", "kwargs": {"survey": survey}},
    {"type": "dichotomy", "key": "dichotomy_1", "kwargs": {"survey": survey, "inverse_choice": lambda x: 'slow 🐌' if x == 1 else 'fast 💨' if x == 0 else 'a mix ✨', "name": '', 'question': 'Visualise social transitions and transformation rates','messages': ["A Quantum leap", "A smooth evolution", "This and *that*"] }},
    {"type": "button", "key": "Let's...", "kwargs": {"survey": survey}},
    {"type": "equaliser", "key": "equaliser", "kwargs": {"data": challenges[0:5], "survey": survey}},
    {"type": "textinput", "key": "location", "kwargs": {"survey": survey}},
    {"type": "button", "key": "`Here` • `Now`", "kwargs": {"survey": survey}},
    {"type": "globe", "key": "Singular Map", "kwargs": {"survey": survey, "database": "gathering"}},
    {"type": "button", "key": "`Here`  `Now`", "kwargs": {"survey": survey}},
    {"type": "yesno", "key": "extra_info", "kwargs": {"survey": survey}},
    {"type": "qualitative", "key": "quali", "kwargs": {"survey": survey}},
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
    st.divider()
    now = datetime.datetime.now()
    st.markdown("# <center>The Social Contract from Scratch</center>", unsafe_allow_html=True)
    st.markdown("### <center>The intersection of Human and Natural Sciences, Philosophy, and Arts.</center>", unsafe_allow_html=True)
    st.markdown('<center>``wait a minute``</center>', unsafe_allow_html=True)
    st.markdown('', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        matrix_size = 5
        matrix_placeholder = st.empty()
        seconds = 1

        start_time = time.time()
        while True:
            time.sleep(update_frequency / 1000.0)  # Convert to seconds
            matrix = generate_random_matrix(matrix_size)
            encoded_matrix = encode_matrix(matrix)
            # norm_value = frobenius_norm(encoded_matrix)/_scale
            # norm_values.append(norm_value)
            
            # with col1:
            #     st.write(norm_value)
            
            with col2:
                matrix_placeholder.empty()
                with matrix_placeholder:
                    
                    display_matrix(matrix)
                    
            elapsed_time = time.time() - start_time
            if elapsed_time >= seconds:
                break
    st.divider()

    
    st.markdown(f"## _Today_ is {now.strftime('%A')}, {now.strftime('%d')} {now.strftime('%B')} {now.strftime('%Y')}")


    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Connecting...", "Contributions", "Contact", "Minimal Glossary", "Frequency Asked Questions", "References"])
    
    with tab1:
        connect()

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
        st.markdown("# Panel contributions so far")
        contributions()

    with tab4:
        st.markdown("## Minimal Glossary")
        glossary()

    with tab5:
        st.markdown("## Frequently Asked Questions")
        faq()
        
    with tab6:
        st.markdown("## The bounty")
        references()

    return survey

def display_category_description(category, description):
    """
    Function to display category and its description.
    """
    col1, _, col2 = st.columns([2, .2, 4])
    with col1:
        # st.markdown(f"**{category}**")
        st.markdown(f"{category}")
    with col2:
        st.markdown(description)
    st.write("---")

def print_languages(languages):
    if "English" in languages:
        st.write("x")
    else:
        st.write(", ".join(f"{language}" for language in languages[0::-1]), f"and {languages[-1]}")

def connect():
    paginator = ConnectingContainer(items = list(zip(panel, widget_info)), items_per_page=1)
    
    with st.container():
        col1, _, col2 = st.columns([2, 10, 2])
        with col2:
            if st.button("Next", key="next_discourse_page"):
                st.session_state["current_discourse_page"] = min(st.session_state.current_discourse_page + 1, paginator.get_total_pages() - 1)
        with col1:
            if st.button("Prev", key="prev_discourse_page"):
                st.session_state["current_discourse_page"] = max(st.session_state.current_discourse_page - 1, 0)
        with _:
            st.progress(st.session_state.current_discourse_page / paginator.get_total_pages(), text=None)
        paginator.display_page(st.session_state.current_discourse_page)
        
    st.write(f'Current page is {st.session_state.current_discourse_page}')
    st.divider()


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

    # for p, (i, info)  in zip(panel, enumerate(widget_info)):
    #     widget_key = info["key"]
    #     widget_type = info["type"]
    #     widget_kwargs = info["kwargs"] if "kwargs" in info else {}

    #     st.markdown(p)
    #     if widget_type in widget_creators:
    #         widget_dict[widget_key] = widget_creators[widget_type](widget_key, kwargs = widget_kwargs)

    #     st.divider()
        
    st.write(survey.data)
    st.write(st.session_state.read_texts)

def contributions():
    
    booklet = [
        ("# Le Gai Savoir", "### _Ariane Ahmadi_ \n ## Crises as vectors for emancipation"),
        ("# The Aftermath Of Political Violence", "### Sophie Wahnich \n ## Fragilité et manque de confiance, en mars 1794..."),
        ("# Engagement with the Sea", "### Antonia Taddei \n ## Proposals for personhood as a defense strategy"),
        ("## tba", "Gabrielle Dyson"),
        ("# Pulse", "### Giorgio Funaro \n ## An electronic impulse through an immersive voyage"),
        ("# We Are Enough", "### Roger Niyigena Karera \n ## Arts and introspection of contemporary society"),
        ("# Rethinking Solutions", "### Graziano Mazza \n ## Polysemic nature of religion as the ancestor of economics"),
        ("# Je Suis l'Eau", "### Alessandra Carosi \n ## Emotional landscapes that lie beneath the surface of our world"),
        ("## Aligning Automated Decision Making with European Values", "## Claire Aoi \n ### •⁠ a fantasy of Stochastic Moral Guardians'"),
        ("## tba", "Andrés León Baldelli"),
    ]

    booklet_dict = {
        "# Le Gai Savoir": {"### Ariane Ahmadi \n ## Crises as vectors for emancipation"},
        "# The Aftermath Of Political Violence": {"### Sophie Wahnich \n ## Fragilité et manque de confiance, en mars 1794..."},
        "# Engagement with the Sea": {"### Antonia Taddei \n ## Proposals for personhood as a defense strategy"},
        "## tba": {"Gabrielle Dyson"},
        "# Pulse": {"### Giorgio Funaro \n ## An electronic impulse through an immersive voyage"},
        "# We Are Enough": {"### Roger Niyigena Karera \n ## Arts and introspection of contemporary society"},
        "# Rethinking Solutions": {"### Graziano Mazza \n ## Polysemic nature of religion as the ancestor of economics"},
        "# Je Suis l'Eau": {"### Alessandra Carosi \n ## Emotional landscapes that lie beneath the surface of our world"},
        "## Aligning Automated Decision Making with European Values": {"## Claire Aoi \n ### •⁠ a fantasy of Stochastic Moral Guardians"},
        "## tba": {"### Andrés León Baldelli"},
    }

    paged_container = _PagedContainer(booklet_dict, items_per_page=2, show_pagination = False)

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
    faq_dictionary = {
    "### What is the main theme of the conference panel discussion?": {"The panel discussion revolves around the theme of 'Change and Societal Transformation' within the context of Europe."},
    "### Who are the key participants in the panel discussion?": {"The panel will feature policymakers, scholars, experts, thinkers, artists, and institutional leaders, creating a diverse and dynamic conversation."},
    "### How can I actively participate in the discussion?": {"We encourage active engagement from the audience through live questions, comments, and feedback during the panel session."},
    "### What innovative interfaces will be presented during the discussion?": {"We plan to showcase new interfaces that harness data and preferences, offering a unique platform for global discussions on societal transitions."},
    "### How will the interactive equaliser metaphor be applied in the discussion?": {"Participants will have virtual sliders representing different categories, allowing them to express preferences, sensitivities, and perceptions related to societal changes."},
    "### What are the initial topics of focus for the discussion categories?": {"Initial topics include but are not limited to environmental sustainability, technological advancements, cultural shifts, economic models, and educational reforms."},
    "### Will the panel address global challenges or focus specifically on Europe?": {"While the primary focus is on Europe, the discussions will touch on global challenges, recognizing the interconnected nature of societal transformations."},
    "### How can I stay updated on the preparation and organization of the panel?": {"Regular updates, including framework details and participant information, will be available on our dedicated conference panel webpage."},
    "### Is there an opportunity for networking and collaboration after the panel discussion?": {"Yes, we encourage participants to connect, share contact information, and explore potential collaborations during and after the conference."},
    "### Can I access recordings of the panel discussion after the conference?": {"Who knows! Recordings may be made available for those who may have missed the live sessions, allowing for continued engagement and knowledge sharing."}
    }
    
    display_dictionary(faq_dictionary)
    
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

    st.markdown("## Suggest reference..")

    return

if __name__ == "__main__":
    
    survey = main()
    add_vertical_space(7)
    # more()
    # footer()
    
    challenges = [
        ("Productive transformation and Innovation", ""),
        ("Global Value Chains", ""),
        ("Artificial intelligence", ""),
        # ("Farmers and Development", ""),
        # ("Climate Change", ""),
        # ("Adaptation and Finance", ""),
        # ("Social Migration", ""),
        # ("The Social Contract", ""),
        # ("Cooperation Reinvented", ""),
        # ("Values, Inequalities, and Sustainability", ""),
        # ("Food system concerns", ""),
        # ("Endogenous Solutions", "")
    ]

    st.divider()
    
    st.markdown("## Would you like to participate?")
    st.markdown("## We are happy to share more and connect")

    st.markdown("""##
                On est dans la merde
        On est revenus a un etat de chaos dans les 
    relations geopolitiques internationales...
                
                """)


    # return_value = survey.dichotomy(name="", 
    #                             label="Confidence",
    #                             question="...", 
    #                             key="boundaries")
