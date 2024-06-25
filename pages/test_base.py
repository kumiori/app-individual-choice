import streamlit as st
from datetime import datetime
from streamlit_extras.mandatory_date_range import date_range_picker 
import streamlit_shadcn_ui as ui
from local_components import card_container
from lib.survey import CustomStreamlitSurvey
import re
from datetime import datetime, timedelta, date
from lib.authentication import _Authenticate
import yaml
from yaml.loader import SafeLoader
import hashlib
from lib.io import conn, fetch_and_display_data, QuestionnaireDatabase as IODatabase
import json
# from streamlit_survey.survey_component import date_decoder

def insert_or_update_data(conn, signature, response_data, data_label:str ='path_001'):
    from lib.survey import date_decoder
    # Iterate over the key-value pairs in response_data
    serialised_dates = [date_decoder(date_obj) for date_obj in response_data['base-book']['value']]
    print(serialised_dates)
    response_data['base-book'] = serialised_dates
    # print(response_data)
    # st.write(response_data['athena-range-dates'])
    
    json.dumps(response_data, indent=2)
    
    try:
        st.json(response_data, expanded=False)
        
        if not signature:
            st.error("Please provide a signature.")
            return
        
        st.write(f"Checking existence of {signature}")
        user_exists = conn.table('base-guests').select('signature').eq('signature', signature).execute()
        st.write(user_exists)
        
        data = {
            'signature': signature,
            data_label: json.dumps(response_data)
        }
        st.json(data, expanded=False)
        
        insert_result = conn.table('base-guests').upsert(data).execute()
        st.toast("Accounted for preferences")
        st.write(insert_result)
            
    except Exception as e:
        st.error(f"Error inserting or updating data in the database: {str(e)}")


class Authenticate(_Authenticate):

    def register_user(self, form_name: str, description: None, webapp=None, preauthorization=True) -> bool:
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
        
        if register_user_form.form_submit_button('`Base` • `Key`'):
            
            if webapp:
                _webapp = webapp
            else:
                _webapp = self.webapp
            
            if description:
                access_key_hash = hashlib.sha256(str(description).encode()).hexdigest()
                if self.__register_credentials(access_key_hash, _webapp, preauthorization):
                    self.credentials['access_key'] = access_key_hash
                return True

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

        existing_access_key = self.get_existing_access_key(access_key)
        
        if existing_access_key:
            st.write("Access key already exists. Choose a different location or try again later.")
            return False
        
        data = {'key': access_key, 'webapp': webapp}
        response = self.supabase.table('access_keys').insert(data).execute()
        st.write(data, response)
        if response:
            return True


with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

description = ''
domain_name = 'base-guests'

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['cookie']['expiry_minutes'],
    config['preauthorized'],
    webapp = 'discourse-authors'
)


def main():
    st.markdown("## <center> • Staying at Base • </center> ", unsafe_allow_html=True)
    survey = CustomStreamlitSurvey()
    col0, col1, col2 = st.columns([.5, 1, .5])
    video_file = open('data/base_tour.mp4', 'rb')
    video_bytes = video_file.read()

    col1.video(video_bytes, 'rb')
    # st.toast("Your preferences have been saved!", icon="🚀")
    # Two columns layout
    col1, col2 = st.columns([1, 1])

    # Date picker to select the rental period
    default_start = date.today() + timedelta(days=5)
    default_end = date.today() + timedelta(days=12)

    with col1:
        st.header("Period")
        date_range = survey.mandatory_date_range(name="Select a date range",
                                                 label='base-book', 
                                                 id='base-book', 
                                                 default_start=default_start, 
                                                 default_end=default_end)

    # Numeric input field for proposed price
    with col2:
        st.header("Stay")
        proposed_price = survey.number_input("I am happy to pay (in EUR)", min_value=0.0, step=1.0)

    switch_value = ui.switch(default_checked=True, label="Happy to share some extra details?", key="switch1")
    
 
    if switch_value:
        with st.expander("Comunication Details", expanded=False):
            col1, col2 = st.columns([1, 1])
            pages = survey.pages(2, on_submit=lambda: st.success("Thank you! Review your preferences below"))
            with pages:
                if pages.current == 0:
                    with col1:
                        name = survey.text_input("Name", help="Please enter your full name", key="name")
                        email = survey.text_input("Email", help="Please enter your email address", key="email")
                    with col2:
                        phone = survey.text_input("Phone Number", help="Please enter your phone number", key="phone")
                        number_guests = survey.number_input("Number of Guests", min_value=1, max_value=2, step=1)
                    
                    additional_comments = survey.text_area("Any additional comments or preferences?", help="Please enter any additional comments or preferences", key="comments")
                
                elif pages.current == 1:
                    survey.select_slider("Checkout Options", options=["Clean & check-out", "Check-out & Clean"], key="slider")
                    with col1:
                        # clean = ui.switch(default_checked=True, label="Clean & check-out", key="clean_checkout")
                        st.markdown('### Clean & check-out')
                        st.write(f'_I will leave the place clean and tidy. Then I will check-out._')

                    with col2:
                        # checkout = ui.switch(default_checked=not clean, label="Check-out & Clean", key="checkout")
                        st.markdown('### Check-out & Clean')
                        st.write(f'_I will leave the place tidy. After I check-out, someone will clean._')
                    
    # Submit button
    if st.button("Review", use_container_width=True):
        phone_regex = r"^(\+\d{1,3})?[-. ]?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}$"
        phone_regex = r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$"
        phone_regex = r"^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$"
    
        num_nights = abs((date_range[0] - date_range[1]).days)

        st.write(f"Selected Stay: {num_nights} nights")
        # st.write(f"Start - End Date:", [date.strftime("%d %B, %Y") for date in date_range] )
        st.write(f"From {date_range[0].strftime('%d %B, %Y')} to {date_range[1].strftime('%d %B, %Y')} " )
        st.write("Proposed Price:", proposed_price)
        st.write("Share Personal Details:", "Yes" if switch_value else "No")

        if switch_value:
            if phone and not re.match(phone_regex, phone):
                st.error("The phone number doesn't look right (must start with a +).")

            review_info = f"""
            **Review Information:**

            **My Information:**
            - Name: {name}
            - Email: {email}
            - Phone Number: {phone}

            **Rental Preferences:**
            - {number_guests} Guests

            **Additional Comments:**
            {additional_comments}
            """

            # st.write(review_info)
            # Using columns layout to split review_info
            col1, col2 = st.columns(2)

            # Displaying review information in two columns
            with col1:
                st.subheader("Personal Information:")
                st.write(f"- Name: {name}\n- Email: {email}\n- Phone Number: {phone}")

            with col2:
                st.subheader("Rental Preferences:")
                st.write(f"- Desired Number of Bedrooms: {number_guests}")
                st.subheader("Additional Comments:")
                st.write(additional_comments)

        # st.json(survey.data)
    
    try:
        signature = hashlib.md5(str(survey.data).encode("utf-8")).hexdigest()
        # st.write(f'`{signature}`')
        if authenticator.register_user(' Check in ', description = signature, webapp=domain_name,  preauthorization=False):
            st.success(f'Very good 🎊. Here is a key 🗝️ for you, a short string of characters, keep it 🤖 handy.\
                ✨ <`{ authenticator.credentials["access_key"] }`> ✨.        \
                You will use it for access 💫')
            try:
                # response_data_json = json.loads(personal_data.data)
                response_data_json = survey.data
                insert_or_update_data(conn, signature, response_data_json, data_label='personal_data')
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please provide a valid JSON string.")

    except Exception as e:
        st.error(e)




if __name__ == "__main__":
    main()
