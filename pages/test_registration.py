import streamlit as st
import json
import streamlit.components.v1 as components
import re

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)

map_float_to_gender = lambda value: "Male" if float(value) == 0 else "Female" if float(value) == 1 else "Everything else" if 0 < float(value) < 1 else ""

def is_valid_email(email):
    # Regular expression for a basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)
    
    return bool(match)

def is_valid_phone_number(phone_number):
    # Regular expression for a basic phone number validation
    # This example allows for optional country code, optional space or hyphen separators
    pattern = r'^(\+\d{1,3})?[-.\s]?\(?\d{1,}\)?[-.\s]?\d{1,}[-.\s]?\d{1,}$'
    
    # Use re.match to check if the phone number matches the pattern
    match = re.match(pattern, phone_number)
    
    return bool(match)

def dichotomy(name, question, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    key=key,
    question = question)


def collect_user_details():
    st.title("Stellazzurra Alliance Registration")

    # Form to collect user details
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    date_of_birth = st.date_input("Date of Birth")
    # gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    gender = dichotomy(name = first_name, question = "Does you gender matter? Black male, White female, and everyone else", key = "boundaries")
    if gender:
        st.write(f'You picked {gender}, that is {map_float_to_gender(gender)}')

    email = st.text_input("Email")
    if email and not is_valid_email(email):
        st.warning("Doesen't look like a valid email address.")
    else:
        st.success("We will be in touch soon.")
        
    phone_number = st.text_input("Phone Number")
    address = st.text_area("Address", value=
"""1st line 
2nd line
3rd line
"""
    )
    city = st.text_input("City")
    country = st.text_input("Country")

    # Form to collect user interests
    st.title("Are You Interested?")
    sport_category = st.text_input("Sport Category")
    category = dichotomy(name = first_name, question = "How do you play? Black as a player, White as an investor. You can play both, you mix...", key = "player")
    
    preferred_role = st.text_input("Preferred Role")

    # Submit button
    if st.button("Collect the data"):
        # Create JSON object
        user_data = {
            "personal_details": {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": str(date_of_birth),
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "city": city,
                "country": country,
            },
            "interests": {
                "sport_category": sport_category,
                "preferred_role": preferred_role,
            },
        }

        # Display the collected data
        st.title("Collected Data")
        st.json(user_data)

        # Save the data to a JSON file (you may want to store it in a database)
        with open("user_data.json", "w") as json_file:
            json.dump(user_data, json_file)
        st.success("Data has been successfully stored!")

if __name__ == "__main__":
    collect_user_details()