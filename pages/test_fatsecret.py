import streamlit as st
from fatsecret import Fatsecret
from streamlit import secrets

# Replace with your own API key and API secret
app_id = secrets['food']['FATSECRET_ID']
app_key = secrets['food']['FATSECRET_KEY']

# Create a FatSecret client
fs = Fatsecret(app_id, app_key)

# Streamlit app
st.title("Nutritional Information Lookup")

# Input for the food item
food_query = st.text_input("Enter a food item:", "banana")

# Button to trigger the search
if st.button("Search"):
    try:
        # Perform the food search
        search_results = fs.foods_search(food_query)
        generic_foods = [food for food in search_results if food.get("food_type") == "Generic"]

        # st.json(generic_foods)
        
        # Display the first result
        if generic_foods:
            food = search_results[0]
            
            food_name = food["food_name"]
            description_parts = food["food_description"].split("|")
            per_100g_part = description_parts[0].strip().split("-")
            quantitative_data = {part.split(":")[0].strip(): part.split(":")[1].strip() for part in description_parts[1:]}

            # Parse food_description to get quantitative data
            description_parts = food["food_description"].split("|")
            quantitative_data = {part.split(":")[0].strip(): part.split(":")[1].strip() for part in description_parts}

            # Display information in Streamlit
            st.write(f"Food Name: {food_name}")
            st.write(f"Per 100g: {per_100g_part}")
            st.write("Quantitative Data:")
            for nutrient, value in quantitative_data.items():
                st.write(f"- {nutrient}: {value}")
            st.write("---")  # Add a separator

            # st.image(food.get('image', ''), caption=food.get('food_name', ''), use_container_width=True)
            # st.header(food.get('food_name', ''))

            # # Display nutritional information
            # st.subheader("Nutritional Information:")
            # st.write(f"Calories: {food.get('calories', '')} kcal")
            # st.write(f"Protein: {food.get('protein', '')} g")
            # st.write(f"Fat: {food.get('fat', '')} g")
            # st.write(f"Carbohydrates: {food.get('carbohydrate', '')} g")
            # st.write(f"Fiber: {food.get('fiber', '')} g")

    except Exception as e:
        st.error(f"Error: {e}")
