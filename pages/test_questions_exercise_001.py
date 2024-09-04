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
### We are creatively imagining and sharing perspectives on _how to interact and relate with an audience_, inspiring new views in a social contract.

Our aim is to create an experience that connects, integrating our diverse ideas and perspectives. 

 Connect with your _access key_ and share your views to clear the horizon.
"""

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

if st.session_state['authentication_status'] is None:
    stream_once_then_write("### Towards our conference in Athens _Europe in Discourse_. Exercise 01.")
    
    cols = st.columns([1,3,1])
    with cols[1]:
        stream_once_then_write(intro_text)

if st.session_state['authentication_status']:
    st.toast('Initialised authentication model')
    authenticator.logout()
    st.write(f'`Your signature is {st.session_state["username"][0:4]}***{st.session_state["username"][-4:]}`')
    # practical_questions()
    first_self_inflicted_exercise()
    
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main', fields = fields_connect)
    st.warning('Please use your access key')
    # # try:
    # #     match = True
    # #     success, access_key, response = authenticator.register_user(data = match, captcha=True, pre_authorization=False, 
    # #                                                                 fields = fields_forge)
    # #     if success:
    # #         st.success('Registered successfully')
    # #         st.toast(f'Access key: {access_key}')
    # #         st.write(response)
    # except Exception as e:
    #     st.error(e)
