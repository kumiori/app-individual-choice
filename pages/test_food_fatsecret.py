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
        
        # if search_results is empty, raise an exception
        if not search_results:
            raise Exception("No results found")
        
        generic_foods = [food for food in search_results if food.get("food_type") == "Generic"]

        st.json(generic_foods)
        
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

def get_nutrient_info(food_item):
    # Perform food search to get food_id
    search_results = fs.foods_search(food_item)
    generic_foods = [food for food in search_results if food.get("food_type") == "Generic"]
    if not generic_foods:
        return {"Error": "No generic food found"}

    food_id = generic_foods[0]['food_id']
    
    # Get detailed nutritional info by food_id
    food_details = fs.food_get(food_id)
    servings = food_details['servings']['serving']
    if isinstance(servings, dict):  # If there's only one serving, it's returned as a dict
        servings = [servings]
    # Find the serving with metric_serving_amount of 100 and metric_serving_unit of 'g'
    target_serving = next(
        (serving for serving in servings 
            if serving.get('metric_serving_amount') == "100.000" and serving.get('metric_serving_unit') == 'g'), 
        None
    )
    
    if target_serving:
        return target_serving
    else:
        return {"Error": "No serving size of 100g found"}


food_item = food_query

# Button to perform nutrient lookup for all food items
if st.button("Get Nutrient Info"):
    with st.spinner("Fetching nutrient information..."):
        nutrient_info = get_nutrient_info(food_item)
        # st.write(nutrient_info)