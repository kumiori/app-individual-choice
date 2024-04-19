import hashlib
import random
from datetime import datetime, timedelta

import streamlit as st
import yaml
from lib.authentication import _Authenticate
from streamlit_authenticator.exceptions import RegisterError
from streamlit_extras.row import row
from yaml.loader import SafeLoader
from lib.survey import CustomStreamlitSurvey
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase
import streamlit_shadcn_ui as ui
import pandas as pd
import datetime
from streamlit_extras.mandatory_date_range import date_range_picker 
import re
import json

import streamlit_survey as ss


def check_existence(conn, key, table="access_keys", index = 'key'):
    if key == "":
        st.error("Please provide a key.")
        return

    # Check if the key already exists
    user_exists, count = conn.table(table) \
        .select("*") \
        .ilike(index, f'%{key}%') \
        .execute()

    return len(user_exists[1]) == 1


def insert_or_update_data(conn, signature, response_data, data_label:str ='path_001'):
    try:
        data = {
            data_label: json.dumps(response_data)
        }
        # st.write(data)
        # user_exists = check_existence(conn, signature)
        preferences_exists = check_existence(conn, signature, table="discourse-data", index='signature')
        
        if preferences_exists:
            # signature exists, update the existing record
            update_query = conn.table("discourse-data").update(data).eq('signature', signature).execute()

            if update_query:
                st.success("Data updated successfully.")
            else:
                st.error("Failed to update data.")
        else:
            # signature does not exist, insert a new record
            data = {
                'signature': signature,
                data_label: json.dumps(response_data)
            }
            insert_result = conn.table('discourse-data').upsert(data).execute()
            st.info("Preferences did not exist, yet. Accounted for preferences")
            
    except Exception as e:
        st.error(f"Error inserting or updating data in the database: {str(e)}")


def is_valid_phone(phone):
    phone_regex = r"^(\+\d{1,3})?[-. ]?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}$"
    phone_regex = r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$"
    phone_regex = r"^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$"

    phone_regexes = [
        r"^(\+\d{1,3})?[-. ]?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}$",
        r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$",
        r"^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$"
    ]

    for regex in phone_regexes:
        if re.match(regex, phone):
            return True
            
    # if re.match(phone_regex, phone):
    #     return True

    return False


if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Panel in Discourse ¶ Authors ¶Portal",
        page_icon="✨",
        layout="centered",
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


if 'selected_idea' not in st.session_state:
    st.session_state["selected_idea"] = None

ideas = list(set(["🦇", "✨", "👽", "😗", "🥹", "♥️", "❤️‍🔥", "🫠", "🥴", "👀", "🧞‍♂️", "🐎", "💫", "💨", "🏢", "🇫🇷", "☑️", "🔑", "🥖", "🕘", "🚧", "🪽", "✨", "☀️", "🔥", "🫂", "🧜🏾‍♂️", "👋🏾", "✉️", "🥤", "🚪", "💃", "🫡", "🎭", "🧉", "⏰", "🦹", "🕛", "🕶️", "💥", "🔐", "🕯️", "❤️", "🤌", "🇮🇹", "🍝", "🍕", "♾️", "🙏", "👏", "🔥", "🍷", "🪵", "☀️", "💞", "🌽", "💦", "💥", "🌻", "🎉", "🪄", "😎", "🗝️", "🛎️", "🧡", "🗝", "🚪", "🧼", "🧿", "💳", "💋", "🥩", "🧂", "🐚", "💦"]))

ideas = list(set({
    "🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬜", "⬛", 
    "🟣", "🟢", "🔵", "🟠", "🔴", "🟡", "🟣", "🟤", "⚫",
    "⚪", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "🟦",
    "🟩", "🟪", "🟫", "⬜", "⬛",
    "▪️", "▫️", "🔶", "🔷", "🔸", "🔹", "🔻", "🔺", "🟧",
    "🟨", "🟩", "🟦", "🟪", "🟫", "⬜", "⬛", "🟣", "🟢",
    "🔵", "🟠", "🔴", "🟡", "🟣", "🟤", "⚫", "⚪", "🔴",
    "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "🟦", "🟩", "🟪",
    "🟫", "⬜", "⬛",
    "🔶", "🔷", "🔸", "🔹", "🔻", "🔺"
}
))
st.markdown("`There may be small data discrepancies due to the time it takes to divide by zero.`")

# Define the list of conference contributions and corresponding authors
contributions = [
    "Le Gai Savoir", "The Aftermath Of Political Violence", "Engagement with the Sea",
    "Retribution and Reform", "Âmes de Paname", "Pulse", "We Are Enough", "Rethinking Solutions", "Je Suis l'Eau", 
    "A Fantasy Of Stochastic Moral Guardians", "Encoded in Writing",
    "Moon Module", "Navigating Social Interactions"
]

authors = [
    "Ariane Ahmadi", "Sophie Wahnich", "Antonia Taddei", "Gabrielle Dyson",
    "Bianca Apollonio", "Giorgio Funaro", "Roger Niyigena Karera", "Graziano Mazza",
    "Alessandra Carosi", "Claire Glanois", "Andrés León Baldelli",
    "H. Genevois, L. White-Bouckaert", "FLCALB"
]

questions = [
    "Philosophy Street?", "Revolution au présent?", "Contract with the Elements?",
    "Damage Claim?", "Generation?", "Immersive?", "Art and Society?", "Shamans speak?", "Experimental?",
    "Sub•Super-Liminal?", "Writing where?", "Moon Performance?", "Games Understood?"
]


with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
class Authenticate(_Authenticate):

    def register_user(self, form_name: str, match: bool=False, preauthorization=True) -> bool:
        """
        Creates a register new user widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        location: str
            The location of the register new user form i.e. main or sidebar.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """
        if preauthorization:
            if not self.preauthorized:
                raise ValueError("preauthorization argument must not be None")

        register_user_form = st.form(form_name)

        col1, _, col2 = st.columns([2, .1, 2])
        
        register_user_form.subheader(form_name)
        self._apply_css_style()
        
        access_key_hash = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
        if register_user_form.form_submit_button('`Here` • `Now`'):
            if match:
                if self.__register_credentials(access_key_hash, self.webapp, preauthorization):
                    self.credentials['access_key'] = access_key_hash
                return True
            else:
                st.success(f'Well 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
                    This is yours <`{ hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest() }`>.        \
                    Keep it in your pocket, add it to your wallet...keep it safe 💭. It will open only if the match holds 🕯️')
                raise RegisterError('Speaking of matches, have you watched the movie `The Match Factory Girl`, by Aki Kaurismäki? 🎥')

    def _apply_css_style(self):
        # with st.container(border=False):
        st.write('<span class="custom-button"/>', unsafe_allow_html=True)

        st.write("""
        <style>
            div[data-testid="stForm"]
                button {
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
            height: 5em;
            border-radius: 4px;
            }
        </style>
        """, unsafe_allow_html=True)

    def __register_credentials(self, access_key: str, webapp: str, preauthorization: bool):
        """
        Adds to credentials dictionary the new user's information.

        Parameters
        ----------
        username: str
            The username of the new user.
        name: str
            The name of the new user.
        password: str
            The password of the new user.
        email: str
            The email of the new user.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        """
        # if not self.validator.validate_username(username):
        #     raise RegisterError('Username is not valid')
        # if not self.validator.validate_name(name):
        #     raise RegisterError('Name is not valid')
        # if not self.validator.validate_email(email):
        #     raise RegisterError('Email is not valid')
        
        existing_access_key = self.get_existing_access_key(access_key)
        
        if existing_access_key:
            st.write("Access key already exists. Choose a different location or try again later.")
            return False
        
        data = {'key': access_key, 'webapp': webapp}
        response = self.supabase.table('access_keys').insert(data).execute()
        # st.write(data, response)
        if response:
            return True
    
# Initialize session_state variables
if 'selected_contribution' not in st.session_state:
    st.session_state["selected_contribution"] = None

if 'selected_author' not in st.session_state:
    st.session_state["selected_author"] = None

if "access_key" not in st.session_state:
    st.session_state['access_key'] = ''

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['cookie']['expiry_minutes'],
    config['preauthorized'],
    webapp = 'discourse-authors'
)


survey = CustomStreamlitSurvey()
personal_data = CustomStreamlitSurvey(label="personal")

def create_connection(key, kwargs = {}):
    authenticator = kwargs.get('authenticator')
    survey = kwargs.get('survey')
    match = kwargs.get('match', False)
    if st.session_state["authentication_status"] is None:
        try:
            if authenticator.register_user(' Check • Point ', match = match,  preauthorization=False):
                st.success(f'Very good 🎊. We have created a key 🗝️ for you. Keys are a short string of characters, these 🤖 days.\
                    💨 Here is one for your access ✨ <`{ authenticator.credentials["access_key"] }`> ✨.        \
                    Keep it in your pocket, add it to your wallet...keep it safe 💭. You will use it to access to the authors mainframe 💫 at the top of the page.')
        except Exception as e:
            st.error(e)
            
    else:
        st.warning("We are already connected, re•enter using your key.")


# Shuffle the lists

# Get the correct association
correct_association = {num: word for num, word in zip(contributions, authors)}

correct_association = {
    contribution: {"author": author, "question": question}
    for contribution, author, question in zip(contributions, authors, questions)
}

# st.write(correct_association)
# Shuffle the lists
random.shuffle(contributions)
random.shuffle(authors)


def commit_to_state(data_type, value):
    if data_type == "word":
        st.session_state["selected_contribution"] = value
    elif data_type == "number":
        st.session_state["selected_author"] = value


# Main Streamlit app
def main():
    st.markdown("# <center>• Welcome •</center>", unsafe_allow_html=True)
    st.markdown("# <center>The Social Contract from Scratch</center>", unsafe_allow_html=True)
    st.markdown("## <center>`platform for authors and contributors`</center>", unsafe_allow_html=True)
    st.markdown("`This platform is a real-pseudo-time system for gathering and understanding how we can best interact and coordinate, in our own way.`")
    # st.write("This is a simple way to connect the who and the what.")

    # st.write("🔑")
    # st.write(st.session_state["authentication_status"])
    # st.write(authenticator.credentials["access_key"])
    # st.write(authenticator)
    authenticator.login('🎶 • Do you have an access key?', key='author_access')

    if st.session_state["authentication_status"]:
        st.balloons()
        now = datetime.datetime.now()
        st.markdown(f"# _Today_ is {now.strftime('%A')}, {now.strftime('%d')} {now.strftime('%B')} {now.strftime('%Y')}")

        cols = st.columns(4)
        db = IODatabase(conn, "access_keys")

        data = db.fetch_data()
        df = pd.DataFrame(data)
        item_count = len(df)
        
        # st.write(df)
        
        with cols[0]:
            ui.metric_card(title="Total count", content=item_count, description="Keys forged", key="card1")
        with cols[1]:
            ui.metric_card(title="Total funding", content="0.01 €", description="Since the start", key="card2")
        with cols[2]:
            ui.metric_card(title="Pending invites", content="13", description="This is an art", key="card3")
        with cols[3]:
            st.markdown("### Panel")
            ui.badges(badge_list=[("experiment", "secondary")], class_name="flex gap-2", key="viz_badges2")
            ui.badges(badge_list=[("production", "primary")], class_name="flex gap-2", key="viz_badges3")
            
        # st.error('🐉 Some content is new')
        key = st.session_state["access_key"] if st.session_state["access_key"] else authenticator.credentials["access_key"]
        no_key = 'unknown'
        st.write(f'Welcome, your key is `<{ key }>` 💭 keep it safe.')
        st.success('🐉 Wonderful, we made it work!')
        
        st.divider()
        st.title('Step 0: What is this all about?')
        
        """_🎊 Booklet download_
        
        🧾 Discover more about our panel discussions, download the latest booklet. 
        """
        
        download_pdf()

        st.divider()


        st.title('Step 1: Share preferences and some details')
            
        switch_value = ui.switch(default_checked=False, label="I am happy to share some extra details", key="switch1")
        
        
        if switch_value:
            """
            Some explaination is in order...
            """
            with st.expander("Personal Details", expanded=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    signature = personal_data.text_input("Signature", id='signature', key="signature", value=key)
                    name = personal_data.text_input("Name", id="name", key="name")
                    email = personal_data.text_input("Email", id="email", key="email")
                with col2:
                    phone = personal_data.text_input("Phone Number (starting with +)", id="phone", key="phone")
                    default_start = datetime.datetime(2024, 9, 24)
                    default_end = default_start + timedelta(days=5)
                    # date_range = personal_data.mandatory_date_range("Which days to stay in Athena?", id='athena-range-dates', 
                    #                                              default_start=default_start, default_end=default_end)
                    date_range = date_range_picker("Which days to stay in Athena?", 
                                                #    id='athena-range-dates', 
                                                    default_start=default_start, default_end=default_end)
                additional_comments = personal_data.text_area("Any additional comments or preferences?", id="extra", key="extra")
            
            color = st.color_picker('Favourite colour?', '#00f900')

            if st.button("Review preferences"):

                num_nights = abs((date_range[0] - date_range[1]).days)
                
                col1, col2 = st.columns(2)
                with col2:
                    st.title(f"{num_nights} nights in Athena")
                    if phone:
                        if is_valid_phone(phone):
                            st.success("✅ Seems a valid phone number")
                        else:
                            st.error("❌ We failed to check, seems an invalid phone number?")

                # Displaying review information in two columns
                with col1:
                    st.subheader("Personal Information:")
                    st.write(f"- Name: {name}\n- Email: {email}\n- Phone Number: {phone if phone else 'not provided'}")

                st.markdown("### All the personal data")
                st.json(personal_data.data, expanded=False)

            # if st.button("Clear Session"):
            #     # Clear session state
            #     st.session_state.clear()

            if st.button("Save preferences"):
                signature_exists = check_existence(conn, key)
                st.write('`Wonderful.`' if signature_exists else 'The key does not correspond to a locked door.')
                try:
                    # response_data_json = json.loads(personal_data.data)
                    response_data_json = personal_data.data
                    insert_or_update_data(conn, key, response_data_json, data_label='personal_data')
                except json.JSONDecodeError:
                    st.error("Invalid JSON format. Please provide a valid JSON string.")

                pass

            st.divider()
            st.write("Next steps")
            st.write("""
            - [X] Download the booklet
            - [X] Save your preferences
            - [?] Disconnect
            - [ ] Display information
            - [ ] Update data
            - [ ] Overview of the mission
            
            """)

        st.title('Step 2: A first mission estimate')
        """ ## The rationale:
            (contributors + support) * days * perdiem[0] * days
    
    Where: contributors = 14, support = 3, perdiem[0]* = 167, days = 5
    
    *: cf. Direction générale des Finances publiques, frais de mission.
        https://www.economie.gouv.fr/dgfip/mission_taux_chancellerie/frais_resultat/GR
        """
        
        contributors = 14
        support = 3
        perdiem = [167, 167, 167, 152, 152]
        days = 5
        ub = (contributors + support ) * days * perdiem[0] * days
        st.markdown(f"## Estimate: {ub} EUR")
        st.write("`Remark: this is an upper bound, excluding flights.`")
        authenticator.logout('(Save my preferences &) Disconnect', 'main', key='save-disconnect')
        authenticator.logout('Disconnect', 'main', key='disconnect')
        # add_vertical_space(13)
        st.divider()
        
    st.title('Step 3: Display information')
    
    st.markdown('https://t.me/+upPANq0yNnBmMzhk')

    if st.session_state["authentication_status"] is None:
        st.markdown("## <center>...otherwise, let's create one</center>", unsafe_allow_html=True)
        st.title("You connect (yourself) to a Title")
        if st.button("To reset choice, clear the memory", use_container_width=True):
            clear_session_state()
            st.info("Forgot names and titles.", icon="🫧")

        col1, col2, col3 = st.columns([1, 2, 1])

        random.shuffle(contributions)
        random.shuffle(authors)

        # Create buttons for each number-word pair

        if st.session_state["selected_author"] is None:
            icon_row = row(5)
            # st.write('<span class="custom-authors">asd</span>', unsafe_allow_html=True)
            for num in authors:
                if icon_row.button(
                    str(num),
                    key = f"button_{num}",
                    use_container_width=True,
                    type='primary',
                    on_click = commit_to_state, args = ["number", num]):
                    st.session_state["selected_author"] = num
                    if st.session_state["selected_contribution"] is not None:
                        check_answer()

            # st.write("""
            #     <style>
            #         div[data-testid="stVerticalBlockBorderWrapper"]:has(
            #             >div>div>div[data-testid="element-container"] .custom-authors 
            #         ) button {
            #             outline: 2px solid red;
            #             border-radius: 2px; 
            #         }
            #     </style>
            #     """, unsafe_allow_html=True)
        else:
            col1.markdown(
                f"# 🧐 {st.session_state['selected_author']}",
                unsafe_allow_html=True,
            )

        if st.session_state["selected_contribution"] is None:
            icon_row = row(5)
            for word in contributions:
                if icon_row.button(
                    word,
                    key = f"button_{word}",
                    type = "secondary",
                    use_container_width=True,
                    on_click = commit_to_state, args = ["word", word]):
                    st.session_state["selected_contribution"] = word
                    if st.session_state["selected_author"] is not None:
                        check_answer()
        else:
            col3.markdown(
                f"# 🧾 {st.session_state['selected_contribution']}",
                unsafe_allow_html=True,
            )
            
    match = True
    if st.session_state["selected_author"] is not None \
        and st.session_state["selected_contribution"] is not None \
        and st.session_state["authentication_status"] is None:
        col2.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        if col2.button("Review and Connect", use_container_width=True):
            st.info(
                ""
                # correct_association[st.session_state["selected_contribution"]]["question"] \
                + "¿ 🧐$\Longleftrightarrow$🧾 ? " \
                # + f" {st.session_state['selected_author'].split()[0]}")
                + "Before we forge a key please double-check, then click the button below to check-in.")
            st.markdown("Matching 🧐 with 🧾 is a simple way to allow access to the authors. Then checkpointing `Here•Now` below will forge a `<key>` for your access. If the match 🧐 with 🧾 is correct, the key will open the door. Otherwise, opening will graciously fail.")
    
        create_connection(key = "authors", kwargs = {"survey": survey, "authenticator": authenticator, "match": check_answer()})

    

def download_pdf():
    pdf_file_path = "data/SocialContractFromScratch-Panel.pso.pdf"

    with open(pdf_file_path, "rb") as f:
        pdf_bytes = f.read()
        
        
    st.download_button(label="Panel Booklet • from Scratch (PDF)", data=pdf_bytes, 
                       file_name=f"athens_panel_contract_from_scratch-{st.session_state['selected_author']}.pdf", mime="application/pdf",
                       use_container_width=True)

# Display the download button
def clear_session_state():
    st.session_state["selected_author"] = None
    st.session_state["selected_contribution"] = None

def check_answer():
    selected_author = st.session_state["selected_author"]
    selected_contribution = st.session_state["selected_contribution"]
    correct_author = correct_association[selected_contribution]['author']

    if selected_author == correct_author:
        # st.success("Correct!")
        return True
    else:
        # st.error("Incorrect. Try again.")
        return False

if __name__ == "__main__":
    
    # Add a button to clear session state

    # st.markdown("""
    # <style>
    # .custom-button {
    # background-color: #4CAF50;
    # color: white;
    # padding: 14px 20px;
    # margin: 8px 0;
    # border: none;
    # cursor: pointer;
    # width: 100%;
    # height: 5em;
    # border-radius: 4px;
    # }
    # .custom-button:hover {
    # opacity: 0.8;
    # }
    # </style>
    # ### <button class="custom-button">`Check • In`</button>
    # """, unsafe_allow_html=True)

    main()
    # st.write(st.session_state["authentication_status"])
    # st.write(authenticator.credentials["access_key"])
    