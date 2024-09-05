import streamlit as st
if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Questions and Perspectives",
        page_icon="👋",
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

import numpy as np
import streamlit_survey as ss
from lib.survey import CustomStreamlitSurvey
from lib.io import (
    create_button, create_checkbox, create_dichotomy, create_equaliser, create_equaliser,
    create_globe, create_next, create_qualitative, create_textinput,
    create_yesno, create_yesno_row, fetch_and_display_data, conn
)
# from lib.texts import stream_text, _stream_once
from datetime import datetime, timedelta
from streamlit_extras.stateful_button import button as stateful_button 
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import philoui as ph
from philoui.texts import hash_text, stream_text, _stream_once
from philoui.geo import get_coordinates, reverse_lookup
from philoui.authentication_v2 import AuthenticateWithKey
from philoui.survey import create_flag_ui
# from philoui.io import check_existence
from philoui.survey import date_decoder

import json
import os
import random
# from streamlit_authenticator import Authenticate
from philoui.authentication_v2 import AuthenticateWithKey

# from pages.test_alignment import get_next_image
import streamlit_shadcn_ui as ui
import yaml
from yaml import SafeLoader

import time
import string
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase

if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()
  
if 'questions' not in st.session_state:
    st.session_state['questions'] = {}
    
if 'serialised_data' not in st.session_state:
    st.session_state.serialised_data = {}
    
# Initialize the session state for scratches if not already done
if 'scratches' not in st.session_state:
    st.session_state["scratches"] = {}

# ============================== AUTH ===========================
with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = AuthenticateWithKey(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
fields_connect = {'Form name':'Connect', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}
fields_forge = {'Form name':'Forge access key', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}

# ===============================================================



survey = CustomStreamlitSurvey('Question map')

def stream_once_then_write(text):
    text_hash = hash_text(text)
    if text_hash not in st.session_state["read_texts"]:
        stream_text(text)
        st.session_state["read_texts"].add(text_hash)
    else:
        st.markdown(text)
        
cols = st.columns(4)
db = IODatabase(conn, "discourse-data")

data = db.fetch_data()
df = pd.DataFrame(data)

item_count = len(df)

with cols[0]:
    ui.metric_card(title="Total count", content=item_count, description="Participants, so far.", key="card1")
with cols[1]:
    ui.metric_card(title="Total GAME", content="0.1 €", description="Since  _____ we start", key="card2")
with cols[2]:
    ui.metric_card(title="Pending invites", content="14", description="...", key="card3")
with cols[3]:
    st.markdown("### Questions")
    ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")
    ui.badges(badge_list=[("production", "primary")], class_name="flex gap-2", key="viz_badges3")

# def create_flag_ui(pages, survey):
#     # Checkbox to flag the question
#     flag_question = st.checkbox(f"This question (Q{pages.current + 1}) is inappropriate, misplaced, ill-formed, abusive, unfit, or unclear")

#     # If the question is flagged, show a text input for the user to provide details
#     flag_reason = ""
    
#     if "flagged_questions" not in survey.data:
#         survey.data["flagged_questions"] = {}

#     if flag_question:
#         flag_reason = st.text_area("Let me specify why I think this question is inappropriate or unclear...")
#         survey.data["flagged_questions"][f"Question {pages.current + 1}"] = {
#                         "reason": flag_reason
#                     }
        
def mask_string(s):
    return f"{s[0:4]}***{s[-4:]}"

def serialise_data(raw_data):
    serialised_dates = [date_decoder(date_obj) for date_obj in raw_data['athena-range-dates']['value']]
    serialised_data = {**raw_data, 'athena-range-dates': serialised_dates}
    return serialised_data

@st.dialog('Cast your preferences')
def _submit():
    # st.write('Thanks, expand below to see your data')    
    signature = st.session_state["username"]
    
    with st.spinner("Checking your signature..."):
        # time.sleep(2)
        preferences_exists = db.check_existence(signature)
        st.write(f"Integrating signature preferences `{mask_string(signature)}`")
        _response = "Yes!" if preferences_exists else "Not yet"
        st.info(f"Some of your preferences exist...{_response}")
        serialised_data = st.session_state['serialised_data']

        try:
            data = {
                'signature': signature,
                'practical_questions_01': json.dumps(serialised_data)
            }
            query = conn.table('discourse-data')                \
                   .upsert(data, on_conflict=['signature'])     \
                   .execute()
            
            if query:
                st.success("🎊 Preferences integrated successfully!")
                
        except Exception as e:
            st.error("🫥 Sorry! Failed to update data.")
            st.write(e)
    
    
intro_text = """
We are exploring collective values and a shared purpose through rethinking _how to interact and relate in a community_, inspiring new views in a social contract.

Our aim is to create an experience that connects, integrating our diverse ideas and perspectives. 

As part of this, we are considering options to share certain aspects of this experience, maybe even accommodation. Connect with your _access key_ and share your preferences to help us make the best decisions.
"""

def practical_questions():

    with st.expander("Questions, practical philosophy", expanded=False, icon=":material/step_over:"):

        pages_total = 10
        pages = survey.pages(pages_total, 
                # on_submit=lambda: st.success("Thank you!")
                on_submit=lambda: _submit(),
                )
        st.markdown("### $\mathcal{W}$elcome to the $\mathcal{Q}$uestion Map")
        st.progress(float((pages.current + 1) / pages_total))
        with pages:
            if pages.current == 0:
                stream_once_then_write('### Asking questions is a real challenge...')
                stream_once_then_write('### Questions are like problems. \
                                       Like problems, they sometimes lack answers or solutions. But why? \
                                       Maybe, they are not well-formed, or they are not clear enough...')
                
                # st.write(st.session_state["read_texts"])

                st.markdown("### Are you happy to go forward?")

                go_forward = survey.radio(
                    "go_forward", options=["Neither Yes nor No", "Yes", "No"], index=0,
                    label_visibility="collapsed", horizontal=True
                )
                if go_forward == "Yes":
                    st.balloons()
                else:
                    st.markdown(
                        """
                        <style>
                        .element-container:has(style){
                            display: none;
                        }
                        #button-after {
                            display: none;
                        }
                        .element-container:has(#button-after) {
                            display: none;
                        }
                        .element-container:has(#button-after) ~ div button {
                            background-color: #3a3b3c;
                            cursor: not-allowed;
                            color: #71717a;
                            border: 1px solid #27272a;
                            opacity: 0.7;
                            pointer-events: none; 
                            }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

                    if go_forward == "No":
                        st.info("Wonderful, we'll meet another time.")
                        
                    elif go_forward == "Neither Yes nor No":
                        st.warning("Please, take your time to choose.")

                    st.divider()
                    create_flag_ui(pages, survey)
                    
            elif pages.current == 1:
                stream_once_then_write("### To ensure everyone\'s travel preferences are accommodated, we need to know how you plan to get to Athens.")
                stream_once_then_write("What type of transportation do you wish to use to travel to Athens? (e.g., plane, train, bus, car)")
                options = ["Plane", "Train", "Bus", "Car", "Bike", "Other"]
                survey.multiselect("Travel modes:", options=options)
                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 2:
                st.markdown("### Departure Location")
                stream_once_then_write("### Knowing your departure point helps us coordinate travel logistics and support.")
                stream_once_then_write("Where will you be departing from to reach Athens?")
                location = survey.text_input("Departure location", id='departure_location', help="My departure location.")
                

                if location:
                    coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
                    with st.spinner():
                        _lookup = reverse_lookup(st.secrets.opencage["OPENCAGE_KEY"], coordinates)
                    if _lookup:
                        st.write(f"Oh! We think we understand where you will be coming from: {_lookup[0][0]['annotations']['flag']}@{coordinates}")
                        # st.write(f"Coordinates: {coordinates}")
                    survey.data["departure_location_coordinates"] = {"label": "departure_location_coordinates", "value": coordinates}
                    
                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 3:

                st.markdown("### Accommodation Preferences")
                stream_once_then_write("### ")
                stream_once_then_write("### We've compiled a list of potential accommodations and want to ensure everyone's preferences are accounted for and everyone is comfortable with the options.")
                # stream_once_then_write("How much do you like each of them? (Please rate from 0 to 1.)")
                st.page_link("https://www.airbnb.com/wishlists/1557728571",
                            label="> Open accommodation options wishlist (external link)", icon="🌎")
                st.markdown("### Is there anything you liked?") 
                sentiment_mapping = ["one", "two", "three", "four", "five"]
                selected = st.feedback("faces")
                responses = [
                    "Great insight! Let's move forward.",
                    "Lovely, thanks for sharing! Let's take the next step.",
                    "Glad to hear it! Onward to the next step.",
                    "Perfect, that\'s helpful! Let's continue our journey.",
                    "Thank you for feedback! Ready to proceed?"
                ]
                if selected is not None:
                    random.shuffle(responses)
                    st.markdown(f"{responses[selected]}")
                    # st.markdown(f"You selected: {sentiment_mapping[selected]}")            
                    survey.data["accommodation_feedback"] = {"label": "accommodation_feedback", "value": selected}
                
                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 4:
                st.markdown("### Stay Duration")
                stream_once_then_write("### To arrange and coordinate accommodations and other logistics effectively, let's share our travel dates.")
                stream_once_then_write("### Our panel discussion is set for September 26-27, 2024. Could you provide a _tentative_, _estimated_ date range for your stay in Athens?")
                default_start = datetime(2024, 9, 24)
                default_end = default_start + timedelta(days=5)
                date_range = survey.mandatory_date_range(name = "Which days to stay in Athena?",
                    label = "athena-dates", 
                    id='athena-range-dates', 
                    default_start=default_start, 
                    default_end=default_end
                )
                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 5:
                st.markdown("### Financial Support Needs")
                stream_once_then_write("### We all have different conditions and arrangements. To provide assistance where needed, we need to know if you require financial support for the trip.")
                stream_once_then_write("Is this the case?")
                financial_support = survey.radio("Financial support", horizontal=True, options=["Yes", "No"], index=1)
                if financial_support ==  "Yes":
                    stream_once_then_write("Please specify the kind of support you require.")
                    # travel, accommodation, or food
                    options = ["Travel", "Accommodation", "Food", "Conference fee", "Other"]
                    selected_options = survey.multiselect("Financial Support:", id="Financial details", options=options, key = "kind_financial_support")
                    
                    if "Other" in selected_options:
                        other_details = survey.text_input("Please specify other financial support needs:", key="other_financial_support")

                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 6:
                st.markdown("### Session Participation 1/2")
                stream_once_then_write("### This may be the most difficult question today. Your opinion matters...")
                stream_once_then_write("""### to find alignment and testing a tangible way to coordinate.""")
                
                with st.spinner("Let's phrase this properly..."):
                    time.sleep(3)
                txt_1 = """We\'ve been presented with the opportunity to integrate our work into a plenary session during the conference. Specifically, Ruth Wodak\'s talk on _“Coping with crises, fear, and uncertainty._” aligns strikingly with our discussions and ideas."""
                txt_2 = """Ruth Wodak is a renowned linguist and professor, and bringing our “results” into her plenary could significantly amplify our exposure and trace. This requires enthusiasm and collaboration to connect with Ruth Wodak and the University\'s Provost, Themis P. Kaniklidou, to present our ideas compellingly."""
                stream_once_then_write(txt_1)
                stream_once_then_write(txt_2)
                stream_once_then_write("#### Let's find out together whether this is a good idea...")
                st.markdown("Here are a few references, if you want to have more elements, before going _Next_:")
                st.page_link("https://en.wikipedia.org/wiki/Ruth_Wodak",
                    label="> Ruth Wodak on wikipedia (external link)", icon="📣")
                st.page_link("https://www.youtube.com/results?search_query=Ruth+Wodak",
                    label="> Ruth Wodak on youtube (external link)", icon="📺")
                st.page_link("https://www.hauniv.edu/about/latest-news/item/567-new-provost",
                    label="> University\'s Provost, Themis P. Kaniklidou (external link)", icon="🎓")

                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 7:
                st.markdown("### Session Participation 2/2")
                txt_1 = """### $\mathcal{Q}$uestion: Do you feel confident about the opportunity to expand our scope through R. Wodak's plenary session? Do you think it\'s a good idea?"""
                stream_once_then_write(txt_1)
                with st.spinner("Use this new strange interface below to tell..."):
                    time.sleep(5)
                    stream_once_then_write("### Black or White - plus all the shades of gray.")
                inverse_choice = lambda x: 'Good idea! 🥲' if x == 0 else 'Not a good idea' if x == 1 else 'sounds reasonable ✨' if x < .5 else "doesn't sound great"

                executive = create_dichotomy(key = "executive", id= "executive",
                                            kwargs={'survey': survey,
                                                'label': 'resonance', 
                                                'question': 'Click to express your viewpoint: the gray area represents uncertainty, the extremes: clarity.',
                                                'gradientWidth': 50,
                                                'height': 250,
                                                'title': '',
                                                'name': 'intuition',
                                                'messages': ["Yes, it's a good idea", "No, it's not a good idea", "I'm not sure"],
                                                'inverse_choice': inverse_choice,
                                                'callback': lambda x: ''}
                )
                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 8:
                # we have collected the data
                
                st.markdown("### Thank you for your participation!")
                stream_once_then_write("### _You_ have collected _your_ preferences, to be  integrated for the best _collective_ decisions.")
                current_date = datetime.now().strftime("%Y-%m-%d")
                raw_data = survey.data
                # serialised_dates = [date_decoder(date_obj) for date_obj in raw_data['athena-range-dates']['value']]
                # serialised_data = {**raw_data, 'athena-range-dates': serialised_dates}
                serialised_data = serialise_data(raw_data)
                stream_once_then_write("### Below are your responses. Download them - if anything happens, they are in a safe place.")
                st.json(serialised_data, expanded=False)
                # survey.download_button("Export Survey Data", use_container_width=True)
                csv_filename = f"my_responses_question_map_1_{current_date}.data"

                if st.download_button(label=f"Download datafile", use_container_width=True, data=json.dumps(serialised_data), file_name='my_responses_question_map_1.csv', mime='text/csv', type='primary'):
                # if st.download_button(label=f"Download: {csv_filename}", use_container_width=True, data=json.dumps(serialised_data), file_name='my_responses_question_map_1.csv', mime='text/csv', type='primary'):
                    st.success(f"Saved {csv_filename}")
                    stream_once_then_write("The file may not be friendly to read, but it's there ;)")
                
                # add serialised data to session state
                st.session_state['serialised_data'] = serialised_data
                    
                st.divider()
                create_flag_ui(pages, survey)
                    
            elif pages.current == 9:
                st.markdown("### Thank you again! ")
                stream_once_then_write("### Time now to integrate your preferences with the others'.")
                stream_once_then_write("### Submit your raw preferences and let's see if we can make sense of all ours.")
                st.divider()
                stream_once_then_write("### _In the next episode..._")
                stream_once_then_write("### We will `visualise` our individual preferences and share more _general_ questions and perspectives.")


def add_scratch(scratch_number):
    st.write(f"Adding scratch {scratch_number}")
    st.session_state["scratches"][f'Scratch {scratch_number}'] = st.text_input(f'Scratch {scratch_number}', key=f'scratch_{scratch_number+1}')
    if scratch_number < 5:
        st.button("Add another scratch", on_click=add_scratch, args=(scratch_number + 1,), key=f'add_scratch_{scratch_number+1}')
    else:
        st.write("Maximum number of scratches reached.")
        st.button("Clear scratches", on_click=lambda: st.session_state["scratches"].clear(), key="clear_scratches")

def first_self_inflicted_exercise():
    from streamlit_lottie import st_lottie

    survey = CustomStreamlitSurvey('First exercise')

    with st.expander("Collaborative Decision-Making Exercise", expanded=True, icon=":material/cruelty_free:"):
        pages_total = 10
        pages = survey.pages(pages_total, 
                on_submit=lambda: _submit(),
                )
        st.markdown("### $\mathcal{W}$elcome to our $\mathcal{F}$irst Exercise")
        st.progress(float((pages.current + 1) / pages_total))
        with pages:
            if pages.current == 0:
                """
**Outlook:**
- _Our discourse_ is to invite the audience to co-create a 'social contract from scratch.'
- For practical purposes, a 'contract' is an understanding or agreement; it is social because it involves _people_; and it is from scratch because it is built from the ground up. 
- In our case, it is a _collective_ understanding that leaves a _transparent_ trace.
- This involves thinking and proposing together from _starting lines_ —or "scratches."
- We have very many unique points: connecting them (connecting us) is our strentgh. We're building something different, a stepping stone for something "bigger."

**How It Works:**
- The process will involve playful interaction, thought-provoking questions, and a melting pot of ideas.

**Your Role:**
#### Engage in the collaborative process of building the ‘social contract from scratch.' This involves contributing questions, perspectives, and insights
"""
            elif pages.current == 1:
                st.subheader("Your Role in Building the Social Contract")
                st.write("Your input and collaboration is crucial in this phase, helping bringing clarity in the process of this collective initiative. Let's work together with creativity")
                
                """
                We shall picture  _How to imagine our panel session?_
                
                We are the Athena collective, a rich and diverse group of individuals with varying perspectives and expertise. Let's imagine (we are creatives). _We are creating a community together, how are our interactions, what governs them, who governs them, how do we care for each other within this context, how do we care about our context?_
                
                We think and build together, from the simple to the complex, from the small to the large, crafting our own shared understanding... 
                
                """     
                
                # with st.echo():
                st_lottie("https://lottie.host/79eac97c-2090-4460-8f31-972f1971fb92/u6yK3lWfDc.json")
                      

            elif pages.current == 2:
                                                
                # Function to collect scratches
                def collect_scratches():
                    scratches = {}
                    scratch_1 = st.text_input("Scratch 1", key="scratch_1")
                    if scratch_1:
                        scratches["Scratch 1"] = scratch_1
                        scratch_2 = st.text_input("Scratch 2", key="scratch_2")
                        if scratch_2:
                            scratches["Scratch 2"] = scratch_2
                            scratch_3 = st.text_input("Scratch 3", key="scratch_3")
                            st.session_state["scratches"]["Scratches"] = scratches
                            if scratch_3:
                                scratches["Scratch 3"] = scratch_3
                                scratch_4 = st.text_input("Scratch 4", key="scratch_4")
                                if scratch_4:
                                    scratches["Scratch 4"] = scratch_4
                                    scratch_5 = st.text_input("Scratch 5", key="scratch_5")
                                    if scratch_5:
                                        scratches["Scratch 5"] = scratch_5
                                        st.session_state["scratches"]["Scratches"] = scratches
                                        
                    return scratches
                # Keywords Input Section
                
                """
                We propose to build this understanding not from a blank state but from _a point of departure_. In sports, “scratch” refers to the starting line of a race.
                For us, it is the starting point for discourse. 
                
                A scratch is a concept, a hook, or a keyword that can be drawn from our contributions, personal interests, professional expertise, or human sensitivity.
                
                """
                st.write("### Scratch your _Scratches_")
                st.write("Let's identify key concepts or prompts to initiate dialogue. Let's scratch the surface of our thoughts and ideas. Let's collect five each, if nothing comes to mind, just scratch the _first idea that comes to mind_ or the word 'scratch'.")
                # keywords = st.text_area("Input your keywords (e.g., Ocean)", "")
                scratches = collect_scratches()
                # inject in survey data
                survey.data["scratches"] = scratches
                st.write(scratches)
                
            elif pages.current == 3:

                # Questions Input Section
                st.write("### List of Questions for Discussion")
                """
                ### These questions can invite participation, challenge assumptions, and inspire collective reflection."""
                """
                Based on my contribution to the panel discussion at the Europe in Discourse conference, I would like to propose (up to) three key questions to guide our interaction with the audience. These questions should spark meaningful dialogue, encourage diverse perspectives, and foster a deeper understanding of the topics at hand. 
                """
                def collect_questions():
                    questions = {}
                    question_1 = st.text_input("Question 1", key="question_1")
                    questions["Question 1"] = question_1
                    question_2 = st.text_input("Question 2", key="question_2")
                    questions["Question 2"] = question_2
                    question_3 = st.text_input("Question 3", key="question_3")
                    questions["Question 3"] = question_3
                    st.session_state["questions"] = questions
                    if question_3:
                        survey.text_area("Question Extended", key="question_extended", help="I want to provide more on the questions", value="Let's expand...")
                    return questions

                questions = collect_questions()
                st.write(questions)
                # inject in survey data
                survey.data["questions"] = questions
                # Problem Input Section
                st.write("### Are there any potential problems in sight?")
                """
                _Problems are great source of inspiration._
                """


            elif pages.current == 4:
                
                """
                # Problems sometimes are the best source of inspiration.
                """
                                
                """
                Organising a panel discussion requires careful coordination among many participants
                
                Resources, everyone's preferences, and constraints are key. 
                
                Given these complexities, problems may arise. 
                
                Do you see any potential issues that could hinder our progress? 
                """

                problems = survey.text_area("Problems: your thoughts and suggestions", id="problems")
                
                """
                Can you foresee possible approaches or solutions to these questions? Please share your thoughts on how we can anticipate and address any obstacles to ensure a smooth and effective panel discussion.
                """
                solutions = survey.text_area("Solutions: Your thoughts and suggestions", id="solutions")
                
                """
                ### Let's imagine some possible scenarios..."""
                
            elif pages.current == 5:
                # Plan B Section
                st.write("### Plan B (A Possible Case Scenario)")
                """
                ### Thank you for contributing to our panel discussion. 
                
                As we continue to refine our approach, we'd like to ask you to think about a Plan B scenario. 
                
                This isn't necessarily the worst-case situation, but rather a backup plan that can be activated if certain elements don't unfold as expected.

                ### What key parts of our plan might not go as intended? 
                
                Perhaps the technology won't function as smoothly, audience engagement may be lower than expected, or specific logistical aspects might face delays. In these cases, what alternatives or adjustments could we consider to ensure our presentation and discussions remain impactful?

                Describe a hypothetical Plan B, if some things don't go according to plan.
                """
                plan_b = survey.text_area("Plan B", id = "plan_b")


            elif pages.current == 6:
                st.write("### Plan $\Omega$ (A Worst Case Scenario)")
                """Thank you again for your contributions."""
                """
                Now, let's consider a **worst-case scenario** — what might happen if things don't go as planned. Everything seems doomed?

                What if the audience isn't engaged, or the discussion doesn't flow as expected? 

                How does a _worst-case scenario_ look like, for us? Consider what could go wrong and how we could still turn the situation around. Can still deliver a meaningful and productive session?
                """
                plan_omega = survey.text_area("Plan $\Omega$", id="plan_omega")
                
            elif pages.current == 7:
                
                # Plan A Section
                st.write("### Describe Plan $A$ (Best Case Scenario)")
                st.write("Detail how things should ideally work out.")
                
                """
                Now, we'd like to envision a Plan A — the best-case scenario for our panel discussion. 
                
                ## Imagine everything unfolds perfectly. How does it look like?
                
                The technology works seamlessly? Audience participation is high, food is great and our messages resonate deeply with everyone involved?

                What does _success_ look like to you? For example, perhaps the discussions spark new collaborations, or our interactive tools lead to unexpected insights. Thematic segments could flow together naturally, leading to productive dialogue and an engaged audience that is inspired to take action.

                Please describe your Plan A - the best case scenario for our panel discussion, as you envision it.
                
                Don't worry about being too detailed or specific; we're looking for a broad _sense_.
                """
                
                plan_a = survey.text_area("Describe Plan A", id="plan_a")
            
            elif pages.current == 8:
                """
                ### Let's reflect on the possible outcomes and the broader impact we aim to achieve. 
                
                
                • New Future Events: 
                    Future gatherings and dialogues? This session spark a new series of 
                    events that bring people together to rethink?
                • New Grassroots & Participatory Policies in EU Regulation: 
                    This session could influence new grassroots-driven initiatives. 
                    What if citizen participation played a central role in 
                    shaping EU regulations and governance?
                • Pilot Projects (Singular Perturbations & Counterexamples): 
                    The value of counterexamples and pilot projects. _Can_ we initiate 
                    small-scale experiments that challenge conventional norms and offer 
                    alternative models?
                • Remote Collaborative Working Groups: What if... we continue working 
                    together beyond this session? Remote, interdisciplinary, collaborative 
                    working groups can sustain exploration of new ideas, pushing forward innovative
                    solutions.
                • Observatory of Perceptions: Creating an “observatory,” not for stars, 
                    but for points-of-view, where we continually assess public views, 
                    challenges, priorities, and societal shifts. An ongoing dialogue to 
                    monitor and better understand societal transformations.
                • Executive Actions: Consider the direct actions that could emerge 
                    from this session. Concrete executive decisions! Launch new initiatives, or even 
                    immediate changes within existing structures.

            Which of these potential outcomes excites you the most? What role do you envision playing in helping bring one or more of these to life? 
"""
                """
                        By adjusting the sliders, express your level of interest or engagement in each category.
        
                """
        
                # st.write(engage)
                equaliser_data = [
                    ("New Future Events", ""),
                    ("New Grassroots & Participatory Policies in EU Regulation", ""),
                    ("Pilot Projects (Singular perturbations & Counterexamples)", ""),
                    ("Remote Collaborative Working Groups", ""),
                    ("Observatory of Perceptions", ""),
                    ("Executive Actions", "")
                    ]

                create_equaliser(key = "equaliser", id= "equaliser", kwargs={"survey": survey, "data": equaliser_data})
                
                st.text_input("Other outcomes?", key="outcomes")
                
            elif pages.current == 9:
                st.write("### Thank you for your participation!")
                st.session_state['serialised_data'] = survey.data
                """
                You can double-check the data you've provided, below. If everything looks good, hit the _Submit_ button to integrate them.
                
                Additionally, you can download the responses for your records.
                
                """
                with st.container():
                    st.json(survey.data, expanded=False)
                    csv_filename = f"my_responses_first_exercise_{datetime.now().strftime('%Y-%m-%d')}.data"
                    if st.download_button(label=f"Download Panel session 01", use_container_width=True, data=json.dumps(survey.data), file_name=csv_filename, mime='text/csv', type='secondary'):
                        st.success(f"Saved {csv_filename}")
                
                
                # with st.expander("As a side note (on singularity)", expanded=False):
                    """
                    The concept of singularity—often referred to as the technological singularity—is tied to the idea that at some point in the future, _some_ intelligence (e.g. AI) could surpass human intelligence. This event, sometimes envisioned as a rapid, transformative moment, has profound implications for knowledge, power, ethics, and society as a whole. It's seen as a “point of no return,” where human control over technology could become irrelevant.

                    Some viewpoints frame singularity as the gateway to the everything-unknown. It could give us rapid access to vast knowledge and capabilities that are currently beyond our comprehension. But it also opens up questions of forbidden realms, like control over life itself, or the blurring boundaries between _this_ and _that_ (e.g. human and machine).

                    There's also a strong fear element. Will humans lose control over what they have created? 
                    Would our understanding of ethics, freedom, _and choice_ (!) hold up in such a radically different reality? The singularity, in this sense, becomes not just a technological leap but an existential challenge.

                    It could represent an entrance to limitless possibilities, where creativity, thought, and innovation expand beyond anything we could imagine. Or it could usher in an era where those who understand and control such advancements wield unimaginable power, which poses its own dangers.

                    In essence, the singularity offers a fast route to answers that humanity has been chasing for millennia, but whether we are ready for those answers—or the questions they raise—is an entirely different matter.
                    
                    Who is ready? Who is not? Who is willing to take the leap? Who is not?

                    """

        st.json(survey.data, expanded=False)
def create_button_with_styles(key, survey, label, bg_color="gray", image_url=None):
    image_style = f'background-image:url("{image_url}") fixed center;' if image_url else ""
    with stylable_container(
        key=key,
        css_styles=f"""
        {{
            [data-testid="baseButton-primary"] {{
                box-shadow: 0px 10px 14px -7px #3e7327;
                {image_style}
                background-color: {bg_color};
                border-radius:4px;
                border:1px solid #4b8f29;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 150px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }}
            [data-testid="baseButton-primary"]:hover {{
                background-color:#72b352;
                cursor: arrow;
            }}
            [data-testid="baseButton-primary"]:active {{
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }}
        }}
        """,
    ):
        return survey.button(label, type='primary', use_container_width=True, key=key)
           
def general_questions():
    general = CustomStreamlitSurvey('General map')
    with st.expander("Questions, general perspectives", expanded=False, icon=":material/recenter:"):
        pages_total = 10
        pages = general.pages(pages_total, 
                # on_submit=lambda: st.success("Thank you!")
                on_submit=lambda: _submit,
                )
        st.markdown("### Global Perspectives")
        st.progress(float((pages.current + 1) / pages_total))
        with pages:
            if pages.current == 0:
                stream_once_then_write('### Understanding how the collective feels about global questions can shape our discussions and presentations.')
                stream_once_then_write('### A birds\' eye view of our views can help us warm up and get ready for the journey ahead.')
                stream_once_then_write('### Please, pardon the generality of the question ^ Without going into the details, how do you feel about what\'s happening in the world today?.')
                options = ["Positive", "Neutral", "Negative", "Hopeful", "Anxious", "Indifferent", "Other"]
                general.multiselect("Feeling mode:", options=options)
            if pages.current == 1:
                stream_once_then_write('### Your energy and mood levels are important for our collaborative activities and ensuring a supportive environment.')
                stream_once_then_write('### How do you feel right now?')
                stream_once_then_write('Are you experiencing high or low energy? Are you feeling positive or negative?')

                
                col1, _, col2 = st.columns([1, .1, 1])
                with col1:
                    st.markdown('## <center> Negative </center>', unsafe_allow_html=True)
                    open_play = create_button_with_styles("play_button", "High energy / Negative", "gray", "data/qrcode_1.png")
                    open_bet = create_button_with_styles("bet_button", "Low energy / Negative", "red", "data/qrcode_1.png")

                with col2:
                    st.markdown('## <center> Positive </center>', unsafe_allow_html=True)
                    open_betray = create_button_with_styles("betray_button", "High energy / Positive", "black")
                    open_move = create_button_with_styles("move_button", "Low energy / Positive", "green")
                    
                    if open_betray:
                        betray.open()
                        
                    if open_move:
                        modal.open(src=src_100K)


if st.session_state['authentication_status'] is None:
    stream_once_then_write("### Towards our conference in Athens _Europe in Discourse_")
    
    cols = st.columns([1,3,1])
    with cols[1]:
        stream_once_then_write(intro_text)

if st.session_state['authentication_status']:
    st.toast('Initialised authentication model')
    authenticator.logout()
    st.write(f'`Your signature is {st.session_state["username"][0:4]}***{st.session_state["username"][-4:]}`')
    practical_questions()
    # first_self_inflicted_exercise()
    
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main', fields = fields_connect)
    st.warning('Please use your access key')
