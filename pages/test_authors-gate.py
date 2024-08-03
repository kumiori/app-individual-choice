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
import webcolors

import streamlit_survey as ss
# from streamlit.elements.utils import _shown_default_value_warning
_shown_default_value_warning = True


def get_color_name(hex_color):
    try:
        color_name = webcolors.hex_to_name(hex_color)
        return color_name
    except ValueError:
        return None

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

def fetch_and_display_personal_data(conn, kwargs):
    # Fetch all data from the "questionnaire" table
    table_name = kwargs.get('database')
    signature = kwargs.get('key')
    # st.write(f"Fetching data from the {table_name} table.")
    response = conn.table(table_name).select("*").eq('signature', signature).execute()

    # Check if there is any data in the response
    if response and response.data:
        data = response.data
        _data = []

        # Display the dataset
        for item in data:
            # st.write(f"ID: {item['id']}")
            updated_at = datetime.datetime.fromisoformat(item['updated_at'][:-6])
            st.write(f"Preferences updated at: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            # st.write(f"Updated At: {item['updated_at']}")
            st.write(f"Signature: {item['signature']}")

            # Parse and display personal data
            personal_data = json.loads(item['personal_data'])
            st.write("Personal Data:")
            for key, value in personal_data.items():
                if key == "athena-range-dates":
                    continue  # Skip displaying this key-value pair
                if isinstance(value, dict):
                    st.write(f"- {key}: {value['value']}")
                else:
                    st.write(f"- {key}: {value}")

            # Convert and display datetime objects
            if 'athena-range-dates' in personal_data:
                st.write("Athena stay - range dates:")
                for date_obj in personal_data['athena-range-dates']:
                    date = datetime.datetime(date_obj['year'], date_obj['month'], date_obj['day'])
                    st.write(date.strftime("%Y-%m-%d"))

            # st.write("Path 001:", item['path_001'])
            st.write("Created At:", item['created_at'])
    else:
        st.write(f"No data found in the {table_name} table.")
    return _data

def fetch_personal_data(conn, kwargs):
    # Fetch all data from the "questionnaire" table
    table_name = kwargs.get('database')
    signature = kwargs.get('key')
    response = conn.table(table_name).select("*").eq('signature', signature).execute()

    if response and response.data:
        return response.data
    else:
        st.write(f"No data found in the {table_name} table.")
        return None

def display_personal_data(data):
    if data:
        for item in data:
            updated_at = datetime.datetime.fromisoformat(item['updated_at'][:-6])
            st.write(f"Preferences updated at: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"Signature: {item['signature']}")

            personal_data = json.loads(item['personal_data'])
            st.write("Personal Data:")
            for key, value in personal_data.items():
                if key == "athena-range-dates":
                    continue  # Skip displaying this key-value pair
                if isinstance(value, dict):
                    st.write(f"- {key}: {value['value']}")
                else:
                    st.write(f"- {key}: {value}")

            if 'athena-range-dates' in personal_data:
                st.write("Athena stay - range dates:")
                for date_obj in personal_data['athena-range-dates']:
                    date = datetime.datetime(date_obj['year'], date_obj['month'], date_obj['day'])
                    st.write(date.strftime("%Y-%m-%d"))

            st.write("Created At:", item['created_at'])
            
            
def insert_or_update_data(conn, signature, response_data, data_label:str ='path_001'):
    from lib.survey import date_decoder
    # Iterate over the key-value pairs in response_data
    serialised_dates = [date_decoder(date_obj) for date_obj in response_data['athena-range-dates']['value']]
    # print(serialised_dates)
    response_data['athena-range-dates'] = serialised_dates
    # print(response_data)
    # st.write(response_data['athena-range-dates'])
    
    json.dumps(response_data, indent=2)
    
    try:
        st.json(response_data, expanded=False)
        # __import__('pdb').set_trace()
        # st.write((response_data))
        data = {
            data_label: json.dumps(response_data)
        }
        
        if not signature:
            st.error("Please provide a signature.")
            return
        
        # user_exists = check_existence(conn, signature)
        st.write(f"Checking existence of {signature}")
        preferences_exists = check_existence(conn, signature, table="discourse-data", index='signature')
        st.info(f"Preferences exist: {preferences_exists}")
        
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
            st.json(data, expanded=False)
            
            insert_result = conn.table('discourse-data').upsert(data).execute()
            st.info("Preferences did not exist yet. Accounted for preferences")
            st.write(insert_result)
            
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
        st.markdown("### _Known issues:_")
        st.info(""" 
                1. The date picker for the stay in Athens (in the section 'personal informations') is often picky. If it shows an error message (`TypeError: list indices must be integers or slices, not str`), try reloading the page.
                """)
        
        st.divider()
        st.title('Step 0: What is this all about?')
        
        """
        
        ### The social contract is a foundational concept in political philosophy, suggesting that individuals consent, either `implicitly` or _explicitly_, to form a society and abide by its rules, norms, and laws _for mutual benefit_. 
        
        ### In exchange for giving up `certain` _freedoms_, individuals receive protection and order provided by the governance structure. This _is the idea..._
        
        # _historically_ articulated by philosophers, we address
        ## _in the social contract_ questions of `legitimacy`, _authority_, and `the origins` of societal organisation. We articulate this discourse `with you` because, right now, 
        # _who else's voice is to be heard_?
        
        """
        
        """_🎊 Booklet download_
        
        🧾 Discover more about our panel discussions, download the temporary booklet. 
        """
        
        download_pdf()

        st.divider()


        st.title('Step 1: Share preferences and some details')
            
        switch_value = ui.switch(default_checked=False, label="Account for my preferences", key="switch1")
        
        
        if switch_value:
            """
            Some explaination is in order...
            """
        with st.expander("Personal Details", expanded=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                signature = personal_data.text_input("Signature", id='signature', key="signature", value=key)
                name = personal_data.text_input("Name", id="name", key="name")
                email = personal_data.text_input("Email", id="email", key="email")
            with col2:
                phone = personal_data.text_input("Phone Number (starting with +)", id="phone", key="phone")
                default_start = datetime.datetime(2024, 9, 24)
                default_end = default_start + timedelta(days=5)
                date_range = personal_data.mandatory_date_range(name = "Which days to stay in Athena?",
                                                                label = "athena-dates", 
                                                                id='athena-range-dates', 
                                                                default_start=default_start, 
                                                                default_end=default_end
                                                                )
                # date_range = date_range_picker("Which days to stay in Athena?", 
                #                             #    id='athena-range-dates', 
                #                                 default_start=default_start, default_end=default_end)
                color = st.color_picker('Favourite colour?', '#00f900')
                
            additional_comments = personal_data.text_area("Any additional comments or preferences?", id="extra", key="extra")
        

        if st.button("Review preferences"):

            num_nights = abs((date_range[0] - date_range[1]).days)
            
            col1, col2 = st.columns(2)
            # if email is empty show a toast asking to input a valid email
            if not email:
                st.toast("Please provide a valid email address", icon="⚠️")
                
            with col2:
                st.title(f"{num_nights} nights in Athena")
                if phone:
                    if is_valid_phone(phone):
                        st.success("✅ Seems a valid phone number")
                    else:
                        st.error("❌ We failed to check, seems an invalid phone number?")
                color_name = get_color_name(color)
                if color_name:
                    st.write(f"This is a {color_name} color!")
                else:
                    st.write("Could not determine the color name. This look like your favourite colour!")
                square_html = f'<div style="width: 330px; height: 10px; background-color: {color};"></div>'
                st.markdown(square_html, unsafe_allow_html=True)                        

            # Displaying review information in two columns
            with col1:
                st.subheader("Personal Information:")
                st.write(f"- Name: {name}\n- Email: {email}\n- Phone Number: {phone if phone else 'not provided'}")
                    
            st.markdown("### All the personal data")
            st.json(personal_data.data, expanded=False)

        if st.button("Save preferences"):
            # Check if key is non-empty, otherwise check the next condition
            if key:
                _key = key
            # Check if authenticator.credentials["access_key"] is non-empty, otherwise check the next condition
            elif authenticator.credentials["access_key"]:
                _key = authenticator.credentials["access_key"]
            # If none of the above conditions are met, assign the value of signature
            else:
                _key = signature
            
            st.session_state["access_key"] = _key
            signature_exists = check_existence(conn, _key)
            
            st.write('`Wonderful.`' if signature_exists else 'The key does not correspond to a locked door.')
            try:
                # response_data_json = json.loads(personal_data.data)
                response_data_json = personal_data.data
                insert_or_update_data(conn, _key, response_data_json, data_label='personal_data')
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please provide a valid JSON string.")

            pass
        
    
        with st.expander("Show personal data", expanded=False):
            
            signature = st.text_input("Signature", key="fetch-signature", value=st.session_state["access_key"])
            if st.button("Fetch preferences"):
                fetch_and_display_personal_data(conn,
                                                kwargs = {"key" : signature, 
                                                            "database": "discourse-data", 
                                                            "index": 'signature'})

        st.divider()
        
        travel_expense_text = """
        ## Travelling smooth 
                
Traveling to Athens is coming. Let's estimate the cost of the travel. Make a rough estimate and enter it below. This will include flights, trains, or any other modes of transportation you'll be using to get to the conference.
"""
        st.markdown(travel_expense_text)
        personal_data.number_input("Travel expenses", key="travel_expenses", min_value=0, help=travel_expense_text)    
        
        travel_type_text = """
How will you be traveling to Athens? Select the type of travel you prefer. Whether it's by air, rail, road, or sea, knowing this helps us find options.
"""
        st.markdown(travel_type_text)

        
        travel_type = personal_data.multiselect("Travel type", 
                                     id = 'travel_preferences', options= ["Air", "Rail", "Road", "Sea"])
        
        
        food_preferences_text = """
Everyone has different tastes and dietary needs. Please select your food preferences from the options below. This will help us ensure that we find delicious choices.
"""
        st.markdown(food_preferences_text)
        
        food_preferences = personal_data.multiselect("Food preferences", id = 'food_preferences', options = ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free"], key="food_preferences", help=food_preferences_text)
        st.json(personal_data.data, expanded=True)

        if st.button("Fetch preferences", key="fetch_preferences_extra"):
            st.write(f'sig {signature}')
            _data = fetch_personal_data(conn, kwargs = {"key" : signature,
                                                "database": "discourse-data",
                                                "index": 'signature'})
            st.json(_data, expanded=True)

        if st.button("Save preferences", key="save_preferences_extra"):
            if key:
                _key = key
            # Check if authenticator.credentials["access_key"] is non-empty, otherwise check the next condition
            elif authenticator.credentials["access_key"]:
                _key = authenticator.credentials["access_key"]
            # If none of the above conditions are met, assign the value of signature
            else:
                _key = signature
            
            st.session_state["access_key"] = _key
            signature_exists = check_existence(conn, _key)
            
            st.write('`Wonderful.`' if signature_exists else 'The key does not correspond to a locked door.')
            try:
                response_data_json = personal_data.data
                st.json(response_data_json, expanded=True)
                insert_or_update_data(conn, _key, response_data_json, data_label='personal_data')
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please provide a valid JSON string.")

            pass
        

        st.write("Next steps")
        st.write("""
        - [X] Download the booklet
        - [X] Save your preferences
        - [?] Disconnect
        - [ ] Display information
        - [ ] Update data
        - [ ] Overview of the mission
        
        """)

        st.title('Step 2: An upper bound estimate')
        
        contributors = 14
        support = 3
        perdiem = [167, 167, 167, 152, 152]
        days = 5
        ub = (contributors + support ) * days * perdiem[0] * days

        fast_estimate = """ ## The rationale:

To estimate the financial resources required for our collective scientific mission, we can adopt a straightforward approach based on the publicly available standard rates provided by CNRS (Centre National de la Recherche Scientifique). 

Because two members of the authors collective are CNRS agents, it is reasonable to extend the same rates to the other participants.

By multiplying the number of participants expected to attend the mission by the estimated number of days they will stay times the official perdiem rate, we derive an initial estimate of the total cost. It's important to note that this calculation serves as an upper bound and is intended for simplicity and transparency. 

Our subsequent challenge will be to carefully devote the allocation of resources to ensure efficient and effective utilization throughout the mission.

The formula is simple: ```(contributors + support) * days * perdiem[0] = upper bound```
    
Where: contributors = 14, support = 3, perdiem[0]* = 167 EUR, days = 5

This is a rough estimate that will be refined aggregating _our_ preferences.
"""
        # st.markdown(f"## Fast estimate (upper bound): {ub} EUR")

        """    
> Ref: cf. Direction générale des Finances publiques, frais de mission.
        https://www.economie.gouv.fr/dgfip/mission_taux_chancellerie/frais_resultat/GR
"""
        st.write("`Remark: this is an upper bound, excluding flights.`")
        authenticator.logout('(Save my preferences &) Disconnect', 'main', key='save-disconnect')
        authenticator.logout('Disconnect', 'main', key='disconnect')
        # add_vertical_space(13)
        st.divider()


        # Title
        st.title("Budget Estimator for Conference Trip")

        """
### Planning our upcoming conference trip to Athens just got easier. 

# This tool helps us calculate the estimated budget for travel, accommodation, and delicious food expenses. Make an estimate: input the daily costs for accommodation and food, along with the approximate travel expenses. The tool will then calculate the total estimated budget for our group.

We can ensure that we have a clear understanding of the financial requirements and make necessary arrangements. 

## Thank you for your participation!
        
        """
        
        # Input fields for per diem and travel expenses
        accommodation_per_day = st.number_input("Accommodation cost per day (EUR):", min_value=0)
        food_per_day = st.number_input("Food cost per day (EUR):", min_value=0)
        travel_cost_per_person = st.number_input("Approximate travel cost per person (EUR):", min_value=0)
        conference_fee_per_person = 250  # Fixed conference fee per person

        # Number of participants and days of stay
        num_participants = 17
        average_days_of_stay = 5

        # Print number of participants and average days of stay
        st.write(f"Number of Participants: {num_participants}")
        st.write(f"Average Days of Stay: {average_days_of_stay}")
        
        # Calculate total expenses
        total_accommodation = num_participants * average_days_of_stay * accommodation_per_day
        total_food = num_participants * average_days_of_stay * food_per_day
        total_travel = num_participants * travel_cost_per_person
        total_conference_fees = num_participants * conference_fee_per_person
        total_expenses = total_accommodation + total_food + total_travel + total_conference_fees

        # Display the budget estimate
        st.subheader("Budget Estimate")
        st.write(f"Total Accommodation Cost: EUR {total_accommodation}")
        st.write(f"Total Food Cost: EUR {total_food}")
        st.write(f"Total Travel Cost: EUR {total_travel}")
        st.write(f"Total Conference Fees: EUR {total_conference_fees}")
        st.write(f"**Total Estimated Budget: EUR {total_expenses}**")

        # add button to submit estimate 
        if st.button("Submit Estimate"):
            st.success("Estimate submitted successfully!")
            st.toast("Thank you for submitting the estimate.")









        
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
    