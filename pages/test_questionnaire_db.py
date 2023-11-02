import streamlit as st
from st_supabase_connection import SupabaseConnection
import json

table_name = "questionnaire"

def check_existence(conn, username):
    if username == "":
        st.error("Please provide a username.")
        return
    # Check if the username already exists
    st.write(f'checking if {username} exists')
    # breakpoint()
    # user_exists = conn.table('questionnaire').select().execute()
    user_exists, count = conn.table("questionnaire")       \
        .select("*")                                \
        .ilike('name', f'%{username}%')             \
        .execute()

    st.write(user_exists, 'count len', len(user_exists[1]))
    return

def insert_data(conn, username, response_data):
    # Insert the return_value into the PostgreSQL table
    
    api = conn.table(table_name)
    
    # api.insert([
    #     {"name": username, "responses": response_data}
    # ]).execute()
    
    api.upsert([
        {"name": username, "response_data": response_data}
    ]).execute()
    
    st.write("Data stored in the table.")

def insert_or_update_data(conn, username, response_data):
    try:
        # Check if the username already exists
        st.write(f'checking if {username} exists')
        # breakpoint()
        # user_exists = conn.table('questionnaire').select().execute()
        user_exists, count = conn.table("questionnaire")       \
            .select("*")                                \
            .ilike('name', f'%{username}%')             \
            .execute()

        st.write(user_exists, 'count key', count)
        
        user_exists, count = conn.table("questionnaire")       \
            .select("*")                                \
            .eq('name', username)             \
            .execute()

        # .eq('name', username).execute()
        st.write(user_exists, 'count len', len(user_exists[1]))
        
        count = len(user_exists[1])
        # breakpoint()
        if count > 0:
            st.write('user_exists', len(user_exists[1]), ' records')
            # Username exists, update the existing record
            data = {
                'response_data': json.dumps(response_data)
            }
            # update_query = conn.table("questionnaire").select("*").eq('name', username).update(data).execute()
            update_query = conn.table("questionnaire").update(data).eq('name', username).execute()
            
            if update_query:
                st.success("Data updated successfully.")
            else:
                st.error("Failed to update data.")
        #     if update_result['status'] == 200:
        #         st.success("Data updated successfully in the database!")
        #     else:
        #         st.error("Failed to update data.")

        else:
            # Username does not exist, insert a new record
        #     data = {
        #         'username': username,
        #         'response_data': json.dumps(response_data)
        #     }
        #     insert_result = supabase.from_table('user_responses').upsert(data).execute()

        #     if insert_result['status'] == 201:
        #         st.success("Data inserted successfully in the database!")
        #     else:
            st.error("Username does not exist.")

    except Exception as e:
        st.error(f"Error inserting or updating data in the database: {str(e)}")

# Initialize connection to Supabase.
conn = st.connection("supabase", type=SupabaseConnection)

# Define the Supabase table name where you want to store questionnaire data.
table_name = "questionnaire"

# Load the JSON questionnaire data
json_data = '''
'''
# data = json.loads(json_data)
st.markdown('## Check existence')
username = st.text_input("Check name", "", key="existence")

if st.button("Submit", key="check"):
    try:
        check_existence(conn, username)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")

st.markdown('## Update data')
username = st.text_input("Name", "")
response_data = st.text_area("Update Data (JSON)", "{}", key="update_json")

if st.button("Submit", key="update"):
    try:
        response_data_json = json.loads(response_data)  # Convert the JSON string to a Python dictionary
        insert_or_update_data(conn, username, response_data_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")



st.title("Add User Responses to the Database")

# User input fields
username = st.text_input("Username", "")
response_data = st.text_area("Response Data (JSON)", "{}")

st.json(response_data)

# st.write(dir(conn.table(table_name)))


if st.button("Submit"):
    try:
        response_data_json = json.loads(response_data)  # Convert the JSON string to a Python dictionary
        insert_data(conn, username, response_data_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON string.")


st.download_button(
    label="Download data JSON",
    data=json_data,
    file_name='survey.json',
    mime='text/json',
)



# Check if the insert was successful and handle any errors.


# conn.close()