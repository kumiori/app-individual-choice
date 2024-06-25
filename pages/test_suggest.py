import streamlit as st
import streamlit_tags as st_tags

# Function to retrieve autocomplete suggestions based on the query
def get_autocomplete_suggestions(query):
    # Replace this with your actual autocomplete logic
    suggestions = ["Apple", "Banana", "Orange", "Tomato", "Carrot"]
    return [suggestion for suggestion in suggestions if query.lower() in suggestion.lower()]

# Streamlit app
st.title("Ingredient Tags")

# Create a list to store selected ingredients
selected_ingredients = []

# Text input with autocomplete suggestions
query = st.text_input("Add Ingredient:", "")

# Retrieve autocomplete suggestions
autocomplete_suggestions = get_autocomplete_suggestions(query)

# Display autocomplete suggestions in a selectbox
selected_ingredient = st.selectbox("Select Ingredient:", autocomplete_suggestions, key="autocomplete_select")

# Add selected ingredient to the list on button click
if st.button("Add"):
    if selected_ingredient not in selected_ingredients:
        selected_ingredients.append(selected_ingredient)
        st.success(f"{selected_ingredient} added to the list!")

# Display the list of selected ingredients
st.write("Selected Ingredients:")
for ingredient in selected_ingredients:
    st.write(f"- {ingredient}")


tags = st_tags.st_tags(label = "## Food items",
    text="Food items",
    suggestions=autocomplete_suggestions,)
if tags:
    st.write(f"`{tags}`")