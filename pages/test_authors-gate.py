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

# Define the list of conference contributions and corresponding authors
contributions = [
    "Le Gai Savoir", "The Aftermath Of Political Violence", "Engagement with the Sea",
    "tbaGD", "Âmes de Paname", "Pulse", "We Are Enough", "Rethinking Solutions", "Je Suis l'Eau",
    "A Fantasy Of Stochastic Moral Guardians", "tbaALB"
]

authors = [
    "Ariane Ahmadi", "Sophie Wahnich", "Antonia Taddei", "Gabrielle Dyson",
    "Bianca Apollonio", "Giorgio Funaro", "Roger Niyigena Karera", "Graziano Mazza",
    "Alessandra Carosi", "Claire Glanois", "Andrés León Baldelli"
]

questions = [
    "Philo1??", "Revolution au pres?", "Social Contract?",
    "Fermentation?", "Generation?", "Immersive?", "Art?", "Shaman?", "Experimental?",
    "Liminal?", "Writing?"
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
        
        access_key_hash = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
        if register_user_form.form_submit_button('`Here` • `Now`'):
            # now = datetime.now()
            # st.write(now) 
            if match:
                if self.__register_credentials(access_key_hash, preauthorization):
                    self.credentials['access_key'] = access_key_hash

                return True
            else:
                st.error("now") 
                
                raise RegisterError('We forget the `where`, there...?')


    def __register_credentials(self, access_key: str, preauthorization: bool):
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
        
        data = {'key': access_key}
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
    config['preauthorized']
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
                    Keep it in your pocket, add it to your wallet...keep it safe 💭. You will use it to re•open the connection 💫')
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
    st.title("Match the Number with the Word!")
    st.write("Match the number with the corresponding word.")

    col1, col2, col3 = st.columns([1, 2, 1])
    # Display the correct association
    st.write("Correct Association:")
    # for num, word in correct_association.items():
        # st.write(f"{num}: {word}")

    random.shuffle(contributions)
    random.shuffle(authors)

    # Create buttons for each number-word pair

    if st.session_state["selected_author"] is None:
        icon_row = row(5)
        for num in authors:
            if icon_row.button(
                str(num),
                key = f"button_{num}",
                use_container_width=True,
                on_click = commit_to_state, args = ["number", num]):
                st.session_state["selected_author"] = num
                if st.session_state["selected_contribution"] is not None:
                    check_answer()
    else:
        col1.markdown(
            f"# {st.session_state['selected_author']}",
            unsafe_allow_html=True,
        )

    if st.session_state["selected_contribution"] is None:
        icon_row = row(5)
        for word in contributions:
            if icon_row.button(
                word,
                key = f"button_{word}",
                use_container_width=True,
                on_click = commit_to_state, args = ["word", word]):
                st.session_state["selected_contribution"] = word
                if st.session_state["selected_author"] is not None:
                    check_answer()
    else:
        col3.markdown(
            f"# {st.session_state['selected_contribution']}",
            unsafe_allow_html=True,
        )
    
    match = True
    if st.session_state["selected_author"] is not None and st.session_state["selected_contribution"] is not None:
        if st.button("Check Answer"):
            # match = check_answer()
            st.info(correct_association[st.session_state["selected_contribution"]]["question"])
        # st.json(st.session_state, expanded=False)
    
        create_connection(key = "authors", kwargs = {"survey": survey, "authenticator": authenticator, "match": check_answer()})

        col2.divider()
    
def clear_session_state():
    st.session_state["selected_author"] = None
    st.session_state["selected_contribution"] = None

def check_answer():
    selected_author = st.session_state["selected_author"]
    selected_contribution = st.session_state["selected_contribution"]
    correct_author = correct_association[selected_contribution]['author']
    # st.write(f"selected_author {selected_author}")
    # st.write(f"correct_author {correct_author}")
    if selected_author == correct_author:
        # st.success("Correct!")
        return True
    else:
        # st.error("Incorrect. Try again.")
        return False

if __name__ == "__main__":
    
    # Add a button to clear session state
    if st.button("Clear Session State"):
        clear_session_state()
        st.info("Session state cleared.")
    
    main()