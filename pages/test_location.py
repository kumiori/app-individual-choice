import streamlit as st
import streamlit_survey as ss
from st_supabase_connection import SupabaseConnection
from streamlit_extras.streaming_write import write as streamwrite 
import json


def insert_data(conn, location, response_data):
    # Insert the response_data into the PostgreSQL table
    api = conn.table("gathering")
    api.upsert([
        {"location": location, "response_data": response_data}
    ]).execute()
    st.write("Data stored in the table.")

conn = st.connection("supabase", type=SupabaseConnection)

def main():
    st.title("Positioning our Streams")

    params = st.query_params
    st.write(params)
    # {"show_map": ["True"], "selected": ["asia", "america"]}
    col1, col2, col3 = st.columns(3)

    survey = ss.StreamlitSurvey("Home")
    # Question 1 in the first column
    with col1:
        current_local_time = survey.timeinput("What is your current local time? Sorry to ask..")

    # Question 2 in the second column
    with col2:
        st.write("We start by showing something we have never seen...Where are you located now?")
        localisation = survey.text_input("location", help="Enter the name of your birthplace.")

    # Question 3 and 4 in the third column
    with col3:
        # birthplace = survey.text_input("Where were you born?", help="Enter the name of your birthplace.")
        lucky_number = survey.number_input("What's your lucky number?", min_value=0, max_value=100000000)

    # Get user input for location

    st.json(survey.data)
    
    _table = "gathering"
    
    response_data = st.text_area("Update Data (JSON)", "{}", key="update_json")

    if st.button("Wish you luck", key="update"):
        try:
            response_data_json = json.loads(response_data)
            st.write(survey.data["location"]["value"])
            # insert_data(conn, survey.data["location"]["value"], response_data_json)
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please provide a valid JSON string.")

if __name__ == "__main__":
    main()
