import streamlit as st
import streamlit.components.v1 as components
import hashlib
import datetime
import time
import streamlit_tags as st_tags
import pandas as pd
import streamlit_player as st_player
import bibtexparser
import codecs
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from lib.dictionary_manip import display_dictionary


if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Workshop Cryosphère et stabilité",
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


def parse_bib_file(bib_file):
    with codecs.open(bib_file, 'r', encoding='utf-8') as file:
        # bib_database = bibtexparser.load(file)
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(file, parser=parser)
        
    return bib_database.entries


    return bib_database.entries


def display_bibliography(entries):
    for entry in entries:
        st.markdown(f"**{entry['title']}**")
        st.write(f"Authors: {entry['author']}")
        st.write(f"Journal/Book: {entry.get('journal', entry.get('booktitle', 'N/A'))}")
        st.write(f"Year: {entry['year']}")
        st.write(f"DOI: {entry.get('doi', 'N/A')}")
        st.write('---')


# Combien avons nous besoin de:
# (equaliser)
# pargager des connaissances
# pargager des ressources
# pargager des approches
# pargager des données
# pargager des perspectives
# pargager des problèmes

from streamlit_vertical_slider import vertical_slider 
from lib.texts import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from pages.test_injection import CustomStreamlitSurvey
from streamlit_extras.streaming_write import write as streamwrite 
import time
import streamlit_survey as ss
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
import random

from lib.io import fetch_and_display_data, conn

# from pages.test_paged import PagedContainer

from lib.matrices import generate_random_matrix, encode_matrix, display_matrix
from lib.dictionary_manip import display_dictionary, display_dictionary_by_indices, display_details_description
from lib.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_next, create_globe, create_textinput, create_checkbox, create_equaliser

update_frequency = 500  # in milliseconds

with open("pages/settimia.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write(f.read())
    
    
keywords = [
    "Cryosphere",
    "Ice Shelf",
    "Climate Science",
    "Scientific Workshop",
    "Environmental Research",
    "Glaciology",
    "Fracture",
    "Damage",
    "Irreversible Evolutions",
    "Energy",
    "Scientific Collaboration",
    "*...*"
]

# Main function
def main():
    # Page title
    # st.title(":circus_tent: Europe in Discourse")
    # st.title(":fountain: Athens Conference, :satellite: 2024")

    # survey = ss.StreamlitSurvey("Home")
    col1, col2, col3 = st.columns(3)
    
    if 'page_number' not in st.session_state:
        st.session_state["page_number"] = 0
    
    if 'damage_parameter' not in st.session_state:
        st.session_state["damage_parameter"] = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state["location"] = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state["location"] = None  # Initial damage parameter

    # once usage:
    # streamwrite(_stream_once(intro_text, 0))
    # st.markdown()
    now = datetime.datetime.now()
    st.markdown("# <center>Que dire sur la stabilité des grandes structures de glace ?</center>", unsafe_allow_html=True)
    st.markdown('#### `Que nous dit la rupture des grandes structures de glace sur les dynamiques et les échanges énérgetiques ? Sur ce sujet nous organisons :`', unsafe_allow_html=True)
    # st.markdown("### <center>nous organisons : </center>", unsafe_allow_html=True)
    st.markdown("# <center>Atelier, Cryosphère et Stabilité</center>", unsafe_allow_html=True)
    st.markdown("### <center>Grenoble, 2024</center>", unsafe_allow_html=True)
    st.divider()
    
    concatenated_keywords = " • ".join([f"**{keyword}**" for keyword in keywords])
    # st.write(concatenated_keywords)
    st.markdown(f"### <center> Keywords: {concatenated_keywords}  </center>", unsafe_allow_html=True)
    # st.markdown('`Do we have any data?`', unsafe_allow_html=True)

    # def st_tags(label: str,
    #         text: str,
    #         value: list,
    #         suggestions: list,
    #         key=None) -> list:
    tags = st_tags.st_tags(label = "## Mots clé à ajouter ? Collaborons !",
        text="Quels mots clé à ajouter ?",
                    suggestions=keywords,)
    # give your partner a sexy dance
    # 
    if tags:
        st.write(f"`Juste le temps de connecter une base de données...`")
        st.write(f"`{tags}`")
        st.button("Ajouter les mots clés dans la queue")

def naq():
    naq_dictionary = {
        "### Antarctic Ice and Sea Level Rise": {
            "How can we improve our understanding of the dynamics driving the cryosphere, and what are the potential implications for future sea level rise?"
        },
        "### Feedback Mechanisms in the Cryosphere": {
            "What are the feedback mechanisms between ice cracks, ice loss, ocean currents, and global climate patterns, and how might they influence regional and global climate stability?"
        },
        "### Impact of Iceberg Calving": {
            "What are the environmental and socio-economic impacts of large-scale iceberg calving events, and how can we understand their consequences?"
        },
        "### Social Adaptation to Antarctic Climate Change": {
            "How can communities and infrastructure in regions adjacent to ice masses adapt to changing climate conditions, including shifts in precipitation patterns and sea ice extent?"
        },
        "### Policy Responses to Antarctic Environmental Change": {
            "What policy frameworks and international collaborations are needed to effectively address the environmental challenges posed by Antarctic ice loss and climate change?"
        },
        "### Antarctic Ecosystem Resilience": {
            "How resilient are Antarctic ecosystems to the combined effects of climate change, ocean acidification, and human activities, and what conservation strategies are most effective in preserving biodiversity?"
        },
        "### Societal Perceptions of Antarctic Change": {
            "How do different societal groups perceive and interpret changes in the Antarctic environment, and what role does public awareness play in driving policy action?"
        },
        "### Equity and Access in Antarctic Research": {
            "How can we ensure equitable access to Antarctic research opportunities and data sharing, particularly for scientists from developing countries and underrepresented communities?"
        },
        "### Technological Innovations for Antarctic Monitoring": {
            "What emerging technologies, such as remote sensing, autonomous vehicles, and advanced modeling techniques, hold the greatest promise for improving our monitoring and understanding of Antarctic ice dynamics?"
        },
        "### Antarctic Governance and Stakeholder Engagement": {
            "How can we enhance stakeholder engagement and public participation in Antarctic governance processes, ensuring that diverse perspectives are incorporated into decision-making?"
        }
    }

    scientific_questions = {
    "### Exploring the integration of high-resolution satellite data with ground-based observations to improve spatial and temporal resolution in monitoring ice dynamics and surface changes.": {"How can advances in satellite imagery enhance our understanding of cryospheric processes?"},

    "### Investigating methods for refining theoretical models to better align with observational data, addressing discrepancies and uncertainties to enhance predictive capabilities.": {"What are the key challenges in reconciling theoretical models with empirical data in cryospheric research?"},

    "### Examining the potential of LiDAR (Light Detection and Ranging) and SAR (Synthetic Aperture Radar) technologies in providing detailed insights into ice thickness, topography, and glacier dynamics at unprecedented scales.": {"How can emerging sensing technologies, such as LiDAR and SAR, revolutionise cryospheric studies?"},

    "### Exploring interdisciplinary approaches to fuse data from various sources, leveraging machine learning algorithms, and statistical techniques to improve the accuracy and reliability of cryospheric assessments.": {"What strategies can be employed to integrate data from diverse sources, including field measurements, remote sensing, and numerical modeling, for comprehensive cryospheric analysis?"},

    "### Investigating strategies to enhance the fidelity of numerical models by integrating feedback loops and biophysical processes, enabling more accurate projections of cryospheric response to climate change.": {"How can numerical models be refined to incorporate feedback mechanisms between the cryosphere, atmosphere, and oceans, enhancing our ability to simulate future ice dynamics and sea level rise?"}
    }

    naq_dictionary.update(scientific_questions)
    
    return naq_dictionary

def faq():
    faq_dictionary = {
        "### What is the primary focus of the workshop discussion?": {"The workshop discussion centers around the stability of the cryosphere and its implications for global climate systems and human societies."},
        "### Who are the main participants in the workshop discussion?": {"The workshop will feature scientists, policymakers, community leaders, indigenous knowledge holders, and experts from various disciplines, fostering a multidimensional dialogue."},
        "### How can I actively engage in the workshop discussion?": {"We welcome active participation from attendees through questions, insights, and observations during the workshop sessions."},
        "### What innovative tools will be utilised during the workshop?": {"We intend to showcase novel tools and methodologies for studying the cryosphere, integrating traditional knowledge with scientific approaches to address complex challenges."},
        "### How will the concept of feedback loops be explored in the workshop?": {"Participants will engage in discussions on feedback loops within the cryosphere-climate system, exploring how changes in ice dynamics influence and are influenced by broader environmental processes."},
        "### What are the primary discussion themes for the workshop sessions?": {"Discussion themes encompass topics such as ice dynamics, sea level rise, permafrost degradation, impacts on ecosystems, and societal resilience strategies."},
        "### Will the workshop address global challenges or focus on specific regions?": {"While the workshop emphasises the cryosphere's role in global climate dynamics, it will also examine region-specific impacts and adaptation measures, recognising the interconnectedness of local and global systems."},
        "### How can I stay informed about workshop updates and logistics?": {"Regular updates on workshop logistics, session agendas, and participant information will be accessible through our workshop webpage and email communications."},
        "### Is there an opportunity for networking and collaboration during the workshop?": {"Absolutely! Attendees are encouraged to network, exchange contacts, and explore collaborative opportunities during breaks and dedicated networking sessions."},
        "### Will recordings of the workshop sessions be available post-event?": {"We aim to provide recordings of the workshop sessions for participants to review and for those unable to attend, facilitating continued learning and knowledge dissemination."}
    }
    return faq_dictionary

def download_pdf():
    pdf_file_path = "data/presentation_en.pdf"

    with open(pdf_file_path, "rb") as f:
        pdf_bytes = f.read()
        
    st.download_button(label="Presentation (PDF 🇬🇧)", data=pdf_bytes, 
                       file_name=f"presentation_workshop_cryosphere_stability_en.pdf", mime="application/pdf",
                       use_container_width=True)

    pdf_file_path = "data/presentation_fr.pdf"

    with open(pdf_file_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(label="Présentation (PDF 🇫🇷)", data=pdf_bytes, 
                       file_name=f"presentation_atelier_cryosphere_stabilité_fr.pdf", mime="application/pdf",
                       use_container_width=True)

if __name__ == "__main__":
    
    survey = main()
    # add_vertical_space(1)
    # more()
    # create_globe("Settimia", kwargs={'database': 'gathering'})
    st.divider()
    st.markdown("## Welcome to Grenoble")    
    st.markdown("""
The cryosphere, comprising ice sheets, glaciers, sea ice, and permafrost, plays a crucial role in Earth's climate system and global energy exchanges, contributing to equilibrating temperature distributions, regulating oceanic currents, and maintaining the overall stability of the planet's climate. Understanding and predicting the cryosphere's shifts is paramount for assessing its impact on the environment, ecosystems, and human societies.
    """)
    
    """_🎊 Presentation document_
    
    🧾 Discover more about our workshop discussions, download the latest presentation. 
    """
    
    download_pdf()
    
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Connecting...", 
    # "Contributions", 
    "Invited participants", 
    "Minimal Glossary", 
    "Frequently Asked Questions", 
    "References",
    "Never Asked Questions"])
    with tab1:
        st.markdown("## Une connexion fortuite ?")
        st_player.st_player("https://www.youtube.com/watch?v=zROrdF5IXC8")

    with tab2:
        invited_list = [
            "Sedhar Chozam, Oxford",
            "Stéphane Perrard, PMMH, Paris",
            "Véronique Dansereau, ..., Grenoble",
            "Jérôme Weiss, ..., Grenoble",
            "Florent Gimbert, ..., Grenoble",
            "Olivier Gagliardini, ..., Grenoble",
            "David Marsan, ..., Grenoble",
            "Benoit Roman, PMMH, Paris",
            "Jean-Jacques Marigo, ..., Pyrenées",
            "Maurice Rossi, Institut ∂'Alembert, Paris",
            "Flaviana Iurlano, DIMA, Genova",
            "Giuliano Lazzaroni, Dipartimento di Matematica e Informatica, Firenze",
            "Pierluigi Cesana, Fukuoka University, Kyushu-Japan",
            "Masato Kimura, Institute of Science and Engineering, Kanazawa-Japan",
            "Garth Wells, Department of Engineering, Cambridge",
            "Jorgen Dokken, Simula, Oslo",
            "Sebastien Neukirch, Institut ∂'Alembert, Paris",
            "Patrick Farrell, Mathematical Institute, ",
            "Lev Truskinovsky, ESPCI, Paris",
            "Gui-Qiang Chen, Mathematical Institute, Oxford",
        ]

        # st.markdown(f"# Contributions are {len(invited_list)} so far...")

        # Create a new dictionary from the sorted list
        # Splitting data into name, affiliation, and location
        data = [entry.split(', ') for entry in invited_list]
        headers = ["name", "affiliation", "location"]
        # print(data)
        # sorted_items = sorted(invited_list.items(), key=lambda x: x.split(', ')[0])
        # sorted_items = sorted(data.items(), key=lambda x: list(x[0])[0])
        # booklet_dict = dict(sorted_items)

        # Create a Pandas DataFrame
        df = pd.DataFrame(data)
        st.table(df)

    with tab4:
        display_dictionary(faq())

    with tab5:
        st.markdown("## A small drop _from_ the ocean (of bibliography)")
        bib_file = 'data/biblio.bib'
        bibliography = parse_bib_file(bib_file)
        for entry in bibliography:
            st.subheader(entry['title'])
            st.markdown(f"*{entry['author']}*")
            st.write(f"Published in {entry.get('journal', '_unknown_')}, {entry.get('year', '')}. [Link]({entry['url']})")

        uploaded_file = st.file_uploader("Contribute a BibTeX file", type=['bib'])

    with tab6:
        # display_dictionary(naq())
        st.write('`Never asked?`')
        pass

# list of ppl
# letter invitation pdf avec motivation
# comme ca verifient iteret et contribution
# catering in loco
# webapp / reseaux
# reserver salle
# abstract titles
# 0-1month conference: title
# tentative programme check conflicts
# mail: -2months, -1month, -1week, -1day
# follow ups, -1.5months, -0.5months, -1weeks
# ask restrictions for programme allocation
# from tday to day, time time, talks minutes
# work sessions, q&a, 25+5
# -1month mail: confirm information, constraints days, 
# agenda