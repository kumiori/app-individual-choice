import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize an empty DataFrame
df = pd.DataFrame(columns=["Food Item", "Quantity", "Unit"])

if 'food_data' not in st.session_state:
    st.session_state.food_data = pd.DataFrame(columns=["Food Item", "Quantity", "Unit"])

if 'not_found' not in st.session_state:
    st.session_state.not_found = []

# Function to add a new food item to the DataFrame
def add_food_item(food_item, quantity, unit, multiplicity):
    new_row = pd.DataFrame({"Food Item": [food_item], "Quantity": [quantity], "Unit": [unit], "Multiplicity": [multiplicity]})
    st.session_state.food_data = pd.concat([st.session_state.food_data, new_row], ignore_index=True)

def get_current_date_string():
    return datetime.now().strftime("%Y-%m-%d")

# Title of the web app
st.title("Groceries App")

# File uploader to load a DataFrame from a CSV file
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:
    uploaded_data = pd.read_csv(uploaded_file)
    # st.session_state.food_data = pd.concat([st.session_state.food_data, uploaded_data], ignore_index=True)
    st.session_state.food_data = uploaded_data
    st.success("CSV file loaded successfully")

# Input fields
food_item = st.text_input("Enter food item:")
quantity = st.number_input("Enter quantity:", min_value=0.0, step=0.1)
multiplicity = st.number_input("Enter multiplicity:", min_value=0.0, step=0.1)
unit = st.radio("Select unit:", ("grams", "kilograms", "liters", "units"))

# Button to add the food item
if st.button("Add Food Item"):
    if food_item and quantity > 0:
        if unit == "units":
            quantity = int(quantity)
        add_food_item(food_item, quantity, unit, multiplicity)
        st.success(f"Added {quantity} {unit} of {food_item} to the list.")
    else:
        st.error("Please enter a valid food item and quantity.")

# Display the DataFrame
st.write("Current List of Food Items:")
st.dataframe(st.session_state.food_data)

# Option to download the DataFrame as CSV
current_date = get_current_date_string()

csv_filename = f"food_data_{current_date}.csv"
csv = st.session_state.food_data.to_csv(index=False)

if st.download_button(label="Download CSV", data=csv, file_name=csv_filename, mime='text/csv'):
    st.success(f"Downloaded {csv_filename}")
    # current_date = get_current_date_string()
    # csv_filename = f"groceries_{current_date}.csv"
    # csv = df.to_csv(index=False)
    
from fatsecret import Fatsecret
from streamlit import secrets

# Replace with your own API key and API secret
app_id = secrets['food']['FATSECRET_ID']
app_key = secrets['food']['FATSECRET_KEY']

# Create a FatSecret client
fs = Fatsecret(app_id, app_key)

def get_nutrient_info(food_item):
    # Perform food search to get food_id
    # st.write(f"Searching for {food_item}...")
    try:
        search_results = fs.foods_search(food_item)
        # st.write(search_results)
        generic_foods = [food for food in search_results if food.get("food_type") == "Generic"]
        if not generic_foods:
            return {"Error": "No generic food found"}
        # else:
            # st.write(f"Found {len(generic_foods)} generic foods")
        food_id = generic_foods[0]['food_id']
        
        # Get detailed nutritional info by food_id
        food_details = fs.food_get(food_id)
        if 'servings' in food_details:
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
        
        
        else:
            st.session_state.not_found.append(food_item)
            return {"Error": "No detailed nutritional info found"}

    except Exception as e:
        st.session_state.not_found.append(food_item)
        return {"Error": str(e)}
    
if st.button(f"Get Groceries Info {len(st.session_state.food_data)}"):
    progress_bar = st.progress(0)
    nutrient_data = []
    total_items = len(st.session_state.food_data)
    
    with st.spinner("Fetching nutrient information..."):
        for idx, row in st.session_state.food_data.iterrows():
            food_item = row["Food Item"]
            nutrient_info = get_nutrient_info(food_item)
            for nutrient, value in nutrient_info.items():
                st.session_state.food_data.at[idx, nutrient] = value
            progress_bar.progress((idx + 1) / total_items)

        st.success("Market information fetched successfully")
        st.write("Updated List of Food Items:")
        # data = 
        st.session_state.food_data.drop(columns=["metric_serving_amount", "metric_serving_unit",
                                                          "serving_description", "serving_id", "serving_url", "serving_url"], inplace=True)
        st.dataframe(st.session_state.food_data)
        
csv_filename = f"food_info_{current_date}.csv"
csv = st.session_state.food_data.to_csv(index=False)

if st.download_button(label="Save CSV", data=csv, file_name=csv_filename, mime='text/csv'):
    st.success(f"Saved {csv_filename}")

# load nutritional info

# File uploader to load a DataFrame from a CSV file
uploaded_file = st.file_uploader("Upload CSV", type="csv", key="upload_nutritional")

if uploaded_file is not None:
    uploaded_data = pd.read_csv(uploaded_file)
    # st.session_state.food_data = pd.concat([st.session_state.food_data, uploaded_data], ignore_index=True)
    st.session_state.food_data = uploaded_data
    st.success("CSV file loaded successfully")
    st.session_state.food_data = uploaded_data

st.write(uploaded_data)



df = st.session_state.food_data
st.session_state.food_data['energy'] = st.session_state.food_data['calories'] * 4184

import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

nutrient_columns = [
    'calcium', 'calories', 'carbohydrate', 'cholesterol', 'fat', 'fiber', 'iron',
    'monounsaturated_fat', 'polyunsaturated_fat', 'potassium', 'protein',
    'saturated_fat', 'sodium', 'sugar', 'vitamin_a', 'vitamin_c', 'energy'
]

df[nutrient_columns] = df[nutrient_columns].mul(df['Quantity']/100, axis=0)


# st.dataframe(st.session_state.food_data[nutrient_columns].mul(df['Quantity'], axis=0))
st.dataframe(df)
# 2. Relative Nutrient Distribution
st.write("## Relative Nutrient Distribution")
nutrients = ['calcium', 'carbohydrate', 'cholesterol', 'fat', 'fiber', 'iron', 'potassium', 'protein', 'saturated_fat', 'sodium', 'sugar']
macro = ['carbohydrate', 'fat', 'protein']
relative_df = df[nutrients].div(df[nutrients].sum(axis=1), axis=0)
macro_relative_df = df[macro].sum(axis=0)
macro_total_df = macro_relative_df.sum()
st.write(f'`{macro_total_df}` grams of nutrients out of {df["Quantity"].sum()/1000:.1f} kgs of mass means {1-macro_total_df/df["Quantity"].sum():.1%} of fiber and water.')

fig2 = px.bar(df[macro], y=macro, 
              x = df['Food Item'],
              labels = {'x': 'Food Item', 'value': 'Nutrients'},
              title='Relative Distribution of Key Nutrients')
# fig2 = px.box(macro_relative_df, y=macro, title='Relative Distribution of Key Nutrients')
st.plotly_chart(fig2)
st.data_editor(macro_relative_df)

fig2 = px.bar(macro_relative_df, title='Relative Distribution of Key Nutrients')
st.plotly_chart(fig2)


# 2. Relative Nutrient Distribution
st.write("## Relative Nutrient Distribution")
relative_df = df[macro].div(df[macro].sum(axis=0), axis=1)
relative_df['Food Item'] = df['Food Item']
relative_df_melted = relative_df.melt(id_vars=['Food Item'], var_name='Nutrient', value_name='Proportion')
st.dataframe(df[macro].sum(axis=0))
st.dataframe(relative_df_melted)
st.dataframe(relative_df)

fig2 = px.scatter(
    relative_df_melted,
    x='Food Item',
    y='Proportion',
    color='Nutrient',
    title='Relative Distribution of Key Nutrients',
    labels={'Proportion': 'Proportion', 'Food Item': 'Food Item'}
)

st.plotly_chart(fig2)
