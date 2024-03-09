import streamlit as st
import requests
from streamlit import secrets
from local_components import card_container

def get_autocomplete_suggestions(query, app_id, app_key):
    base_url = "https://api.edamam.com/auto-complete"
    params = {
        "q": query,
        "limit": 5,  # Limit the number of suggestions
        "app_id": app_id,
        "app_key": app_key,
    }
    response = requests.get(base_url, params=params)
    st.write(response)

    data = response.json()
    return data
    
    
def recipe_search(ingredient, app_id, app_key):
    response = requests.get(
        f'https://api.edamam.com/apifood-database/v2/nutrients?q={ingredient}&app_id={app_id}&app_key={app_key}'
    )
    data = response.json()
    return data

def food_parser(ingredient, app_id, app_key):
    response = requests.get(
        f'https://api.edamam.com/api/food-database/v2/parser?app_id={app_id}&app_key={app_key}&ingr={ingredient}&nutrition-type=logging&category=generic-foods'
    )
    data = response.json()
    return data

def main():
    st.title('Recipe Search App')

    # Get user input for the ingredient
    ingredient = st.text_input('Enter an ingredient:', 'chicken')

    # Retrieve API credentials from Streamlit secrets
    app_id = secrets['food']['EDAMAM_ID']
    app_key = secrets['food']['EDAMAM_KEY']

    # Search for recipes when the user clicks the button
    if st.button('Parse Food'):
        food_data = food_parser(ingredient, app_id, app_key)

        # st.json(food_data)
        # Display the parsed food information
        if 'hints' in food_data and len(food_data['hints']) > 0:
            food_info = food_data['hints'][0]['food']
            st.subheader(f'Information for: {ingredient}')
            st.write('Food Label:', food_info['label'])
            st.write('Food Category:', food_info['category'])
            st.write('Nutrients:', food_info['nutrients'])
        else:
            st.error(f'No information found for: {ingredient}')

        st.subheader("Parsed Data:")
        for entry in food_data['parsed']:
            food_info = entry['food']
            quantity = entry['quantity']
            measure_info = entry['measure']

            st.write(f"Food Label: {food_info['label']}")
            st.image(food_info['image'], caption=food_info['label'], use_column_width=False)
            st.write(f"Quantity: {quantity}")
            # st.write(f"Measure Label: {measure_info['label']}")
            # st.write(f"Measure Weight: {measure_info['weight']} grams")
            st.write("Nutrients:")
            for nutrient, value in food_info['nutrients'].items():
                st.write(f"- {nutrient}: {value}")


        # Display hints data
        st.subheader("Hints Data:")
        for index, hint in enumerate(food_data['hints']):
            with card_container(key=f"hint-{index}"):
                food_info = hint['food']
                measures_info = hint['measures']

                st.write(f"## Food Spec: {food_info['label']}")
                # st.image(food_info['image'], caption=food_info['label'], use_column_width=False)
                st.write("Available Measures:")
                for measure_info in measures_info:
                    st.write(f"- {measure_info['label']}: {measure_info['weight']} grams")
                nutrients = food_info['nutrients']
                st.write(f"Calories: {nutrients['ENERC_KCAL']} kcal")
                st.write(f"Protein: {nutrients['PROCNT']} g")
                st.write(f"Fat: {nutrients['FAT']} g")
                st.write(f"Carbohydrates: {nutrients['CHOCDF']} g")
                st.write(f"Fiber: {nutrients['FIBTG']} g")
                

    query = st.text_input("Enter food name:", "")
    if st.button("Get Autocomplete Suggestions"):
        if query:
            api_key = "YOUR_API_KEY"  # Replace with your Edamam API Key
            suggestions = get_autocomplete_suggestions(query, app_id, api_key)
            st.write("Autocomplete Suggestions:", suggestions)
        else:
            st.warning("Please enter a food name.")

if __name__ == '__main__':
    main()
