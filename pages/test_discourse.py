import streamlit as st
import streamlit.components.v1 as components
import hashlib

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


class CustomStreamlitSurvey(ss.StreamlitSurvey):
    shape_types = ["circle", "square", "pill"]

    def dichotomy(self, label: str = "", id: str = None, **kwargs) -> str:
        return Dichotomy(self, label, id, **kwargs).display()
    
    def equaliser(self, label: str = "", id: str = None, **kwargs) -> str:
        return VerticalSlider(self, label, id, **kwargs).display()

    def qualitative_parametric(self, label: str = "", id: str = None, key=None, **kwargs):
        return ParametricQualitative(self, label, id, **kwargs).display()


survey = CustomStreamlitSurvey()

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
    
def _qualitative(name, question, label, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    label = label,
    key=key,
    areas = areas,
    data_values  = [1, 2, 10],
    question = question)

Dichotomy = ss.SurveyComponent.from_st_input(_dichotomy)
VerticalSlider = ss.SurveyComponent.from_st_input(vertical_slider)
ParametricQualitative = ss.SurveyComponent.from_st_input(_qualitative)

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

## Our panel springs at the intersection of Human Sciences, Natural Sciences, Philosophy, and Arts, offering an opportunity to build a concrete perspective in addressing uncertainty, confusion, and risk.

## ..._to bring forward_ an emancipatory vision of change.

## What do you think? Are we on the right path?

"""
panel_3 = """ 

## Everything seems to lie upon a notion of change and connection.

## _"these are not easy times for multilateral cooperation_ and _there is more than a list of policies to be considered."*_

*) From: `Development Cooperation Review  Vol. 6 - Special Issue` - opening to _new hopes_...in the context of international cooperation.
## ... Pez ...

## _That issue_ was published at a crucial time. We decide to engage in a conversation in which you participate.

### Your opinion counts, `right`?"""
 
panel_4 = """

## To integrate a bigger picture, help us make sense of time scales and policy priorities.

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

[mixer]

##### This is a great exercise in making communication effective, actionable, and visual.


"""

panel_7 = """

[sanity check: u_0 neq u_rnd]

## Your conscious input is precious, and energy naturally flows where is most needed. Thank you for your participation. What's your name?

## We are trying to understand why the world is in a state of fracture on several levels: individual, social and universal.

## Human beings no longer meet in ideas. How do patterns behave?

## This is how we think: _matrix is a map where patterns emerge_

##  Buut maybe you are used to different types of map

this is Paris

what's your city?

"""

panel_8 = """


## Here and Now, our commitment is towards action.

## As we invite your free and conscious participation, let's treasure this moment of exchange.

## How to visualise a bigger picture? 

## Verify your location and local time. You will receive an access key to join the conversation.

# access key: `[here] x [now]` 
# [ I {NAME} CONNECT here and now ]

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

## In the meantime, we aare reconstructing our links to backend.

## In {city} it's {weather} and {temperature} degrees. Happy to leave us a message or share a feedback?

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

widget_info = [
    {"type": "next", "key": "next"},
    {"type": "yesno", "key": "button_0"},
    {"type": "yesno", "key": "button_1"},
    {"type": "yesno", "key": "opinion_counts"},
    {"type": "dichotomy", "key": "dichotomy_1"},
    {"type": "button", "key": "Let's..."},
    {"type": "equaliser", "key": "equaliser", "kwargs": {"data": challenges[0:3]}},
    {"type": "textinput", "key": "location"},
    {"type": "button", "key": "`Here` • `Now`"},
    {"type": "globe", "key": "Singular Map"},
    {"type": "button", "key": "`Here`  `Now`"},
    {"type": "yesno", "key": "extra_info"},
    {"type": "qualitative", "key": "quali"},
    {"type": None, "key": None}
]

placeholders = [{"type": None, "key": None} for _ in range(len(panel)-len(widget_info))]

widget_info = widget_info + placeholders

widget_dict = {}

def create_button(key, kwargs = {}):
    return st.button(label=key)

def create_dichotomy(key, kwargs = {}):
    return survey.dichotomy(name="Spirit", 
                            label="Confidence",
                            question="Dychotomies, including time...", 
                            key=key)

def create_qualitative(key, kwargs = {}):
    print(kwargs)
    return survey.qualitative_parametric(name="Spirit",
            question = "Support, Donate, or Invest?",
            label="Qualitative",
            areas = 3,
            key = "parametric")
    
def create_yesno(key, kwargs = {}):
    col1, col2 = st.columns(2)
    with col1:
        yes_clicked = st.button("Yes", key=f"{key}_yes")
    with col2:
        no_clicked = st.button("No", key=f"{key}_no")
    
    return

def create_next(key, kwargs = {}):
    return st.button("Next", key=f"{key}")

def create_globe(key, kwargs = {}):
    data = fetch_and_display_data(conn, table_name="gathering")
    
    # with stream:
        # st.write('.........')
    
    # Generate JavaScript code with city data
    javascript_code = f"""
    // Gen city data
    const VELOCITY = 9; // minutes per frame

    const sunPosAt = dt => {{
        const day = new Date(+dt).setUTCHours(0, 0, 0, 0);
        const t = solar.century(dt);
        const longitude = (day - dt) / 864e5 * 360 - 180;
        return [longitude - solar.equationOfTime(t) / 4, solar.declination(t)];
    }};

    let dt = +new Date();
    const solarTile = {{ pos: sunPosAt(dt) }};
    const timeEl = document.getElementById('time');

    const cityData = { data };
    const N = 10;

    const world = Globe()
        (document.getElementById('globeViz'))
        .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
        .backgroundColor('rgb(14, 17, 23)')
        .tilesData([solarTile])
        .tileLng(d => d.pos[0])
        .tileLat(d => d.pos[1])
        .tileAltitude(0.01)
        .tileWidth(180)
        .tileHeight(180)
        .tileUseGlobeProjection(false)
        .tileMaterial(() => new THREE.MeshLambertMaterial({{ color: '#ffff00', opacity: 0.3, transparent: true }}))
        .tilesTransitionDuration(0)
        .pointsData(cityData)
        .pointAltitude('luckynumber');

    // animate time of day
    requestAnimationFrame(() =>
        (function animate() {{
        dt += VELOCITY * 60 * 1000;
        solarTile.pos = sunPosAt(dt);
        world.tilesData([solarTile]);
        timeEl.textContent = new Date(dt).toLocaleString();
        requestAnimationFrame(animate);
        }})()
    );

    // Add auto-rotation
    world.controls().autoRotate = true;
    world.controls().autoRotateSpeed = 3.6;
    """

    # HTML code with embedded JavaScript
    html_code = f"""
    <head>
    <style> body {{ margin: 0em; }} </style>
    <script src="//unpkg.com/three"></script>
    <script src="//unpkg.com/globe.gl"></script>
    <script src="//unpkg.com/solar-calculator"></script>
    </head>

    <body>
    <div id="globeViz"></div>
    <div id="time"></div>
    <script>
        { javascript_code }
    </script>
    </body>
    """

    # Display the HTML code in Streamlit app
    col1, col2 = st.columns(2)
    with col1:
        st.components.v1.html(html_code, height=700, width=700)
    
    st.write("Globe")
    return 

def create_textinput(key, kwargs = {}):
    text = survey.text_input(key, help="")
    return 

def create_checkbox(key, kwargs = {}):
    return survey.checkbox("Choose one:", key=key)

def create_equaliser(key, kwargs):
    rows = 1
    dimensions = kwargs["data"]
    split_len = len(dimensions) // rows
    bottom_cols = st.columns(split_len)

    # for j in range(rows):
    j = 0
    with st.container():
        for i, column in enumerate(bottom_cols):
            with column:
                print(dimensions[i + j*split_len][0])
                survey.equaliser(
                    label=dimensions[i + j*split_len][0],
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
    st.markdown("# _Today_ {date}...")


    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Connecting...", "Contributions", "Contact", "Minimal Glossary", "Frequency Asked Questions", "References"])
    
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
        st.markdown("# Panel contributions so far")
        contributions()

    with tab4:
        st.markdown("## Minimal Glossary")
        glossary()

    with tab5:
        st.markdown("## Frequently Asked Questions")

    with tab6:
        st.markdown("## References")
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
        ("## (_AI: behind the scenes_)", "## Claire Aoi \n ### [einsteigenbitte](https://einsteigenbitte.eu/)"),
        ("## tba", "Andrés León Baldelli"),
    ]
    with st.container(height=666):
        for author, title in booklet:
            display_category_description(author, title)

        st.divider()
            
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

    st.markdown("## We are happy to share more and connect")

    
    st.markdown("""## A panel discussion bringing forward an emancipatory vision of           change... \n
                On est dans la merde
        On est revenus a un etat de chaos dans les 
    relations geopolitiques internationales...
                
                """)
    st.markdown("## Would you like to participate?")


    # return_value = survey.dichotomy(name="", 
    #                             label="Confidence",
    #                             question="...", 
    #                             key="boundaries")
