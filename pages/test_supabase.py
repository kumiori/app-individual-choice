import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
conn = st.experimental_connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="address_book", ttl="10m").execute()

# Print results.
for row in rows.data:
    st.markdown(f"{row['name']} has a :{row['animal']}: id {row['id']}")