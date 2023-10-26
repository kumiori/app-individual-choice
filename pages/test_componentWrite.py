import streamlit as st
from st_supabase_connection import SupabaseConnection
import streamlit.components.v1 as components

# Initialize connection.
conn = st.experimental_connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="address_book", ttl="10m").execute()


    
st.text("Hello")

_my_component = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)


def my_component(name, greeting="Hello", key=None):
    return _my_component(name=name, greeting=greeting, default=0, key=key)



# Print results.
for row in rows.data:
    st.markdown(f"{row['name']} has a :{row['animal']}: id {row['id']}")

return_value = my_component(name = "Mai", key = "Ahoi")
st.write('You picked me:', return_value)

confirmation = st.button("Confirm and Store in Database")


if confirmation:
    # Insert the return_value into the PostgreSQL table
    insert_query = conn.table("address_book").insert([
        {"name": "Mai", "value": return_value}
    ]).execute()
    st.write("Data stored in the table.")
else:
    st.write(f"Data not stored in the table. ({return_value})")

