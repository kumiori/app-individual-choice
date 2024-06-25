import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from local_components import card_container

# Sample data for illustration
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

# Define a dictionary of dietary preferences with example values
dietary_preferences = {
    'vegetarian': 'Prefers plant-based foods and avoids meat and fish.',
    'vegan': 'Follows a strict plant-based diet, avoiding all animal products.',
    'pescatarian': 'Includes fish and seafood in a vegetarian diet, but avoids other meats.',
    'flexitarian': 'Primarily follows a vegetarian diet but occasionally includes meat or fish.',
    'carnivore': 'Mainly consumes meat and animal products.',
    'omnivore': 'Eats a variety of foods, including both plant and animal-based options.',
    'gluten-free': 'Avoids gluten-containing grains like wheat, barley, and rye.',
    'keto': 'Follows a ketogenic diet, which is high in fat and very low in carbohydrates.',
    'paleo': 'Emulates the diet of prehistoric humans, focusing on whole foods and avoiding processed items.',
    'low-carb': 'Restricts carbohydrate intake to manage blood sugar levels or promote weight loss.',
}

df = pd.DataFrame(macro_splits).T

# Number of columns in the grid layout
num_columns = 2

# Calculate the number of rows needed
num_rows = -(-len(df) // num_columns)  # Round up the division

# Create a streamlit app
st.title('Dietary Preferences Polar Plots')
st.markdown("""## This app displays the macronutrient splits for different dietary preferences. \n

## The hidden label is `Carbohydrates`
            """)
# Create a grid layout
for row in range(num_rows):
    cols = st.columns(num_columns)

    for col_idx, col in enumerate(cols):
        preference_idx = row * num_columns + col_idx
        if preference_idx < len(df):
            preference = df.index[preference_idx]
            with col:
                col.markdown(f'### {preference}')
                col.write(dietary_preferences[preference])
                fig = go.Figure(data=go.Barpolar(
                    r=df.loc[preference],
                    # theta=[45, 135, 270],
                    theta=df.columns,
                    # thetaunit = "radians",
                ))
                fig.update_layout(template="plotly_dark")
                fig.update_layout(
                    showlegend = False,
                    polar = dict(# setting parameters for the second plot would be polar2=dict(...)
                    ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        ),
                        # sector = [150,210],
                        angularaxis = dict(
                                thetaunit = "radians",
                                dtick = 0.3141592653589793
                            )
                ))
                
                # Set the plot size (adjust the width and height as needed)
                col.plotly_chart(fig, use_container_width=True, width=100, height=100)
