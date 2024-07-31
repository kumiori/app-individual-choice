import streamlit as st

options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('You selected:', options)


import streamlit as st
from datetime import date
from lib.survey import CustomStreamlitSurvey

# Initialize survey
survey = CustomStreamlitSurvey()

# Debugging: Print out input types and values
def debug_input(label, value):
    st.write(f"{label}: {value} (Type: {type(value)})")

# Travel Expenses Estimate
travel_expense_text = """
Traveling to Athens is coming. Let's estimate the cost of the travel. Make a rough estimate and enter it below. This will include flights, trains, or any other modes of transportation you'll be using to get to the conference.
"""
travel_expense = st.number_input("Travel Expenses Estimate", help=travel_expense_text)
debug_input("Travel Expenses Estimate", travel_expense)

# Travel Type
travel_type_text = """
How will you be traveling to Athens? Select the type of travel you prefer. Whether it's by air, rail, road, or sea, knowing this helps us find options.
"""
travel_types = ["Air", "Rail", "Road", "Sea"]
selected_travel_type = st.selectbox("Travel Type", travel_types, help=travel_type_text)
debug_input("Travel Type", selected_travel_type)

# Dates Stay in Athens
dates_stay_text = """
To make sure we have everything ready for your stay, please let us know the dates you wish to be in Athens. Select the start and end dates of this trip.
"""
start_date = st.date_input("Start Date", help=dates_stay_text, value=date.today())
end_date = st.date_input("End Date", help=dates_stay_text, value=date.today())
debug_input("Start Date", start_date)
debug_input("End Date", end_date)

# Food Preferences
food_preferences_text = """
Everyone has different tastes and dietary needs. Please select your food preferences from the options below. This will help us ensure that we find delicious choices.
"""
food_options = ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"]

selected_food_preferences = survey.multiselect("Food Preferences", id='asd', options = food_options, help=food_preferences_text)
debug_input("Food Preferences", selected_food_preferences)

# Assuming you are using the CustomStreamlitSurvey object in some manner
# survey.add_question("travel_expense", travel_expense)
# survey.add_question("travel_type", selected_travel_type)
# survey.add_question("start_date", start_date)
# survey.add_question("end_date", end_date)
# survey.add_question("food_preferences", selected_food_preferences)

# Display survey
# survey.display()

# Process survey data
# if survey.is_submitted():
survey_data = survey.data
st.write("Survey Data:", survey_data)
    # Here you can process the data further or store it in a database