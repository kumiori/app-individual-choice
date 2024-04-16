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
        with cols[0]:
            ui.metric_card(title="Total count", content=item_count, description="Keys forged", key="card1")
        with cols[1]:
            ui.metric_card(title="Total funding", content="0.01 €", description="Since the start", key="card2")
        with cols[2]:
            ui.metric_card(title="Pending invites", content="10", description="This is an art", key="card3")
        with cols[3]:
            st.markdown("### Panel")
            ui.badges(badge_list=[("experiment", "secondary")], class_name="flex gap-2", key="viz_badges2")
            ui.badges(badge_list=[("production", "primary")], class_name="flex gap-2", key="viz_badges3")
            
        # st.error('🐉 Some content is new')
        key = st.session_state["access_key"] if st.session_state["access_key"] else authenticator.credentials["access_key"]
        no_key = 'unknown'
        st.write(f'Welcome, your key is `<{ key }>` 💭 keep it safe.')
        st.success('🐉 Wonderful, we made it work!')
        
        """_🎊 Booklet download_
        
        🧾 Discover more about our panel discussions, download the latest the booklet. 
        """
        
        download_pdf()
        
        authenticator.logout('Commit my changes / Disconnect', 'main', key='disconnect')
        # add_vertical_space(13)
        st.divider()


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
    