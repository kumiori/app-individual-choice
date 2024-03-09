import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from local_components import card_container
import streamlit_shadcn_ui as ui

# Sample food data (replace this with your actual food data)
food_data = {
    'Food Item': ['Broccoli', 'Chicken Breast', 'Brown Rice', 'Extra Virgin Olive Oil', 'Eggs'],
    'Energy (kcal per 100g)': [55, 165, 111, 884, 155],
    'Carbohydrate (g per 100g)': [11.2, 0, 23.5, 0, 1.1],
    'Protein (g per 100g)': [3.7, 31, 2.6, 0, 12.6],
    'Fat (g per 100g)': [0.6, 3.6, 0.9, 100, 11]
}


food_df = pd.DataFrame(food_data)

def compute_nutrient_contributions(quantities):
    # Compute the overall nutrient contributions based on quantities
    overall_energy = sum(quantities[i] * food_df['Energy (kcal per 100g)'][i] / 100 for i in range(len(quantities)))
    overall_carbs = sum(quantities[i] * food_df['Carbohydrate (g per 100g)'][i] / 100 for i in range(len(quantities)))
    overall_protein = sum(quantities[i] * food_df['Protein (g per 100g)'][i] / 100 for i in range(len(quantities)))
    overall_fat = sum(quantities[i] * food_df['Fat (g per 100g)'][i] / 100 for i in range(len(quantities)))
    
    return overall_energy, overall_carbs, overall_protein, overall_fat

def main():
    st.title('Nutrient Calculator')

    # Display food items and sliders
    quantities = []
    for i, food_item in enumerate(food_df['Food Item']):
        if food_item == 'Eggs':
            quantity = st.slider(f'Quantity of {food_item}', 0, 10, 2, step=1)
        else:
            quantity = st.slider(f'Quantity of {food_item} (grams)', 0, 500, 100)
        quantities.append(quantity)

    cols = st.columns(3)
    with cols[0]:
        # Target energy requirement and nutrient split
        target_energy = st.number_input('Target Energy Requirement (kcal)', value=1500)
        target_carbs = st.number_input('Target Carbohydrates (%)', min_value=0, max_value=100, value=40)
        target_protein = st.number_input('Target Protein (%)', min_value=0, max_value=100, value=30)
        target_fat = st.number_input('Target Fat (%)', min_value=0, max_value=100, value=30)

    # Compute nutrient contributions
        overall_energy, overall_carbs, overall_protein, overall_fat = compute_nutrient_contributions(quantities)

    with cols[1]:

        # Calculate distance from target split
        distance_carbs = abs(overall_carbs - (target_carbs / 100 * target_energy))
        distance_protein = abs(overall_protein - (target_protein / 100 * target_energy))
        distance_fat = abs(overall_fat - (target_fat / 100 * target_energy))

        # Display results
        st.header('Nutrient Contributions:')
        st.write(f'Overall Energy Content: {overall_energy:.2f} kcal')
        st.write(f'Overall Carbohydrates: {overall_carbs:.2f} grams')
        st.write(f'Overall Protein: {overall_protein:.2f} grams')
        st.write(f'Overall Fat: {overall_fat:.2f} grams')

    with cols[2]:
        # Display distance from target split
        st.header('Distance from Target Split:')
        st.write(f'Carbohydrates: {distance_carbs:.2f} grams')
        st.write(f'Protein: {distance_protein:.2f} grams')
        st.write(f'Fat: {distance_fat:.2f} grams')

    # Bar chart visualizing the distance from the target split
    distances = [distance_carbs, distance_protein, distance_fat]
    nutrients = ['Carbohydrates', 'Protein', 'Fat']

    dataf = pd.DataFrame({'Month': nutrients, 'Distance': distances})

    with card_container(key="chart1"):
        st.vega_lite_chart(dataf, {
            'mark': {'type': 'bar', 'tooltip': True, 
                     'fill': 'rgb(173, 250, 29)', 'cornerRadiusEnd': 4 },
            'encoding': {
                'x': {'field': 'Month', 'type': 'ordinal'},
                'y': {'field': 'Distance',
                      'scale': {'domain': [0, 1000]},
                      'type': 'quantitative',
                      'axis': {'grid': False}},
            },
        }, use_container_width=True, theme=None)


if __name__ == "__main__":
    main()