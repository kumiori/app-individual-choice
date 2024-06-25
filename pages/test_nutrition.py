import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import streamlit_tags as st_tags
from fatsecret import Fatsecret
from streamlit import secrets

app_id = secrets['food']['FATSECRET_ID']
app_key = secrets['food']['FATSECRET_KEY']

fs = Fatsecret(app_id, app_key)

# Placeholder functions for computation and data processing
def compute_rwi(data):
    # Placeholder for recommended weekly intake calculation
    return 2000  # Example value

def get_autocomplete_suggestions(query):
    # Placeholder for autocomplete suggestions
    return ["Bananas", "Apples", "Oranges", "Broccoli"]

def fetch_food_data(food_query):
    alternatives = []
    search_results = fs.foods_search(food_query)
    if not search_results:
        return None
    generic_foods = [food for food in search_results if food.get("food_type") == "Generic"]

    if not generic_foods:
        return None

    food = generic_foods[0]
    if len(generic_foods) > 1:
        alternatives.append([generic_foods[i]["food_name"] for i in range(1, len(generic_foods))])
    food_name = food["food_name"]
    description_parts = food["food_description"].split("|")
    per_100g_part = description_parts[0].strip().split("-")
    quantitative_data = {part.split(":")[0].strip(): part.split(":")[1].strip() for part in description_parts[1:]}

    # Create a dictionary with all the relevant data
    food_data = {
        "Food Name": food_name,
        "Per 100g": per_100g_part[1].strip(),
        **quantitative_data
    }

    return food_data, alternatives
# Sample data for dietary preferences polar plots
macro_splits = {
    'vegetarian': {'Carbohydrates': 60, 'Proteins': 20, 'Fats': 20},
    'vegan': {'Carbohydrates': 65, 'Proteins': 15, 'Fats': 20},
    'pescatarian': {'Carbohydrates': 55, 'Proteins': 25, 'Fats': 20},
    'flexitarian': {'Carbohydrates': 50, 'Proteins': 25, 'Fats': 25},
    'carnivore': {'Carbohydrates': 10, 'Proteins': 70, 'Fats': 20},
    'omnivore': {'Carbohydrates': 50, 'Proteins': 25, 'Fats': 25},
    'gluten-free': {'Carbohydrates': 40, 'Proteins': 30, 'Fats': 30},
    'keto': {'Carbohydrates': 5, 'Proteins': 20, 'Fats': 75},
    'paleo': {'Carbohydrates': 25, 'Proteins': 30, 'Fats': 45},
    'low-carb': {'Carbohydrates': 20, 'Proteins': 40, 'Fats': 40}
}
df = pd.DataFrame(macro_splits).T

# Streamlit application
st.title('Food Nutritional Application')

# Stage 1: Determination of weekly necessary nutrients
st.header('Stage 1: Determination of Weekly Necessary Nutrients')
with st.form(key='rwi_form'):
    age = st.number_input('Age', min_value=0, max_value=120, value=25)
    height = st.number_input('Height (cm)', min_value=0, max_value=250, value=175)
    weight = st.number_input('Weight (kg)', min_value=0, max_value=300, value=70)
    gender = st.selectbox('Gender', ['Male', 'Female'])
    activity = st.selectbox('Activity Level', ['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Extra active'])
    submit_button = st.form_submit_button(label='Compute')

    if submit_button:
        data = {'age': age, 'height': height, 'weight': weight, 'gender': gender, 'activity': activity}
        weekly_intake = compute_rwi(data)
        st.success(f'Recommended Weekly Intake: {weekly_intake} kcal')

# Stage 2: Selection of dietary preferences
st.header('Stage 2: Selection of Dietary Preferences')
selected_preference = st.selectbox('Select Your Dietary Preference', df.index)
st.markdown(f'### {selected_preference}')
st.write(df.loc[selected_preference])
fig = go.Figure(data=go.Barpolar(
    r=df.loc[selected_preference],
    theta=['Carbohydrates', 'Proteins', 'Fats'],
))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Stage 3: Identification of set of preferred food items
st.header('Stage 3: Identification of Preferred Food Items')
food_query = st.text_input('Enter a food item:')
if food_query:
    suggestions = get_autocomplete_suggestions(food_query)
    st.write('Autocomplete Suggestions:')
    for suggestion in suggestions:
        st.write(suggestion)

food_items = st_tags.st_tags(label = "## Food items",
    text="Food items",
    suggestions=[],)
if food_items:
    st.write(f"`{food_items}`")
    
if st.button("Search"):
    try:
        # Fetch data for all food items and store in a list of dictionaries
        all_food_data = []
        all_alternatives = []
        for food_query in food_items:
            food_data, alternatives = fetch_food_data(food_query)
            if food_data:
                all_food_data.append(food_data)
                all_alternatives.append(alternatives)
            else:
                st.warning(f"No generic food data found for {food_query}")

        if not all_food_data:
            raise Exception("No results found")

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(all_food_data)

        # Display the DataFrame in Streamlit
        st.dataframe(df)
        st.write(all_alternatives)
    except Exception as e:
        st.error(f"Error: {e}")

# Stage 4: Equalisation of the quantities
st.header('Stage 4: Equalisation of Quantities')
st.write('This stage will involve adjusting the quantities of selected food items to match the nutritional needs.')

# Stage 5: Possible refinement of food items
st.header('Stage 5: Refinement of Food Items')
st.write('This stage will involve refining the selection of food items based on user feedback or additional criteria.')
