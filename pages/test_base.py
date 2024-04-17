import streamlit as st
from datetime import datetime
from streamlit_extras.mandatory_date_range import date_range_picker 
import streamlit_shadcn_ui as ui
from local_components import card_container
from pages.test_injection import CustomStreamlitSurvey
import re
from datetime import datetime, timedelta, date

def main():
    st.markdown("## <center> • Staying at Base • </center> ", unsafe_allow_html=True)
    survey = CustomStreamlitSurvey()

    # Two columns layout
    col1, col2 = st.columns([1, 1])

    # Date picker to select the rental period
    default_start = date.today() + timedelta(days=5)
    default_end = date.today() + timedelta(days=12)

    with col1:
        st.header("Period")
        date_range = date_range_picker("Select a date range", default_start=default_start, default_end=default_end)

    # Numeric input field for proposed price
    with col2:
        st.header("Value")
        proposed_price = st.number_input("Enter Proposed Value (in EUR)", min_value=0.0, step=1.0)

    switch_value = ui.switch(default_checked=True, label="Happy to share some extra details?", key="switch1")
    
    
    if switch_value:
        with st.expander("Personal Details", expanded=False):
            col1, col2 = st.columns([1, 1])
            with col1:
                name = st.text_input("Name", "")
                email = st.text_input("Email", "")
            with col2:
                phone = st.text_input("Phone Number", "")
                desired_bedrooms = st.number_input("Desired Number of Beds", min_value=1, max_value=2, step=1)
            additional_comments = st.text_area("Any additional comments or preferences?", "")

    # Submit button
    if st.button("Review"):
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

            **Personal Information:**
            - Name: {name}
            - Email: {email}
            - Phone Number: {phone}

            **Rental Preferences:**
            - Desired Number of Bedrooms: {desired_bedrooms}

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
                st.write(f"- Desired Number of Bedrooms: {desired_bedrooms}")
                st.subheader("Additional Comments:")
                st.write(additional_comments)

if __name__ == "__main__":
    main()
