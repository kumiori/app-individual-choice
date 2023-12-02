import streamlit as st
import json
from supabase import create_client
# TO TEST
# Initialize Supabase client
supabase_url = 'YOUR_SUPABASE_URL'
supabase_key = 'YOUR_SUPABASE_API_KEY'
supabase = create_client(supabase_url, supabase_key)

# Streamlit app
st.title("Supabase Realtime Example")

# Function to display real-time changes
def display_realtime_changes(payload):
    st.write(f"Change received: {json.dumps(payload)}")

# Subscribe to changes in the 'test_table' table
subscription = supabase \
    .table('test_table') \
    .on('*', display_realtime_changes) \
    .subscribe()

# Streamlit UI
st.write("Listening for changes in the 'test_table' table. Make updates in your Supabase dashboard.")

# Add any other Streamlit components or UI elements as needed

# Remember to unsubscribe when the app is closed
if st.button("Unsubscribe"):
    subscription.unsubscribe()
    st.success("Unsubscribed from real-time updates.")

# Note: Replace 'YOUR_SUPABASE_URL' and 'YOUR_SUPABASE_API_KEY' with your actual Supabase credentials.