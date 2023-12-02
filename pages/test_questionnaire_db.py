import streamlit as st
from st_supabase_connection import SupabaseConnection
import json

def check_existence(conn, username):
    if username == "":
        st.error("Please provide a username.")
        return

    # Check if the username already exists
    user_exists, count = conn.table("questionnaire") \
        .select("*") \
        .ilike('name', f'%{username}%') \
        .execute()

    return len(user_exists[1]) == 1

def insert_data(conn, username, response_data):
    # Insert the response_data into the PostgreSQL table
    api = conn.table("questionnaire")
    api.upsert([
        {"name": username, "response_data": response_data}
    ]).execute()
    st.write("Data stored in the table.")

def insert_or_update_data(conn, username, response_data):
    try:
        data = {
            'response_data': json.dumps(response_data)
        }
        st.write(data)
        user_exists = check_existence(conn, username)

        if user_exists:
            # Username exists, update the existing record
            update_query = conn.table("questionnaire").update(data).eq('name', username).execute()
            
            if update_query:
                st.success("Data updated successfully.")
            else:
                st.error("Failed to update data.")
        else:
            # Username does not exist, insert a new record
            data = {
                'name': username,
                'response_data': json.dumps(response_data)
            }
            insert_result = conn.table('questionnaire').upsert(data).execute()
            st.info("Username does not exist, yet. Accounted for preferences")
    except Exception as e:
        st.error(f"Error inserting or updating data in the database: {str(e)}")

# Initialize connection to Supabase.
conn = st.connection("supabase", type=SupabaseConnection)

st.markdown('## Check existence')
username = st.text_input("Check name", "", key="existence")

if st.button("Account for preferences", key="check"):
    try:
        check_existence(conn, username)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")

st.markdown('## Update data')
username = st.text_input("Name", "")
response_data = st.text_area("Update Data (JSON)", "{}", key="update_json")

if st.button("Account for preferences", key="update"):
    try:
        response_data_json = json.loads(response_data)
        insert_or_update_data(conn, username, response_data_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")

st.title("Add User Responses to the Database")

# User input fields
username = st.text_input("Username", "")
response_data = st.text_area("Response Data (JSON)", "{}")

st.json(response_data)

if st.button("Account for preferences"):
    try:
        response_data_json = json.loads(response_data)
        insert_or_update_data(conn, username, response_data_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")

    st.download_button(
        label="Download data JSON",
        data=response_data,
        file_name='survey.json',
        mime='text/json',
    )
    
def fetch_and_display_data():
    # Fetch all data from the "questionnaire" table
    response = conn.table("questionnaire").select("*").execute()
    st.write(response)
    # Check if there is any data in the response
    if response and response.data:
        data = response.data

        # Display each row of data
        for row in data:
            st.write(f"Username: {row['name']} Id: {row['id']} timestamp: {row['created_at']}")
            st.json(json.loads(row['response_data']))
            st.write("------------")
    else:
        st.write("No data found in the 'questionnaire' table.")

# Add a button to fetch data
if st.button("Fetch Data"):
    fetch_and_display_data()