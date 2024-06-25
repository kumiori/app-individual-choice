import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data for illustration
data = {
    'Food Item': ['Apple', 'Banana', 'Chicken Breast', 'Broccoli', 'Almonds'],
    'Quantity': [2, 3, 1, 2, 0.5],
    'Unit': ['units', 'units', 'units', 'units', 'kg'],
    'Multiplicity': [1, 1, 1, 1, 1000],
    'calcium': [6, 5, 16, 47, 269],
    'calories': [52, 89, 165, 55, 575],
    'carbohydrate': [14, 23, 0, 11, 21],
    'cholesterol': [0, 0, 85, 0, 0],
    'fat': [0.2, 0.3, 3.6, 0.6, 49],
    'fiber': [2.4, 2.6, 0, 3.7, 12.5],
    'iron': [0.1, 0.3, 0.9, 0.7, 3.7],
    'measurement_description': ['medium', 'medium', 'medium', 'cup', 'kg'],
    'monounsaturated_fat': [0, 0, 1.2, 0, 31],
    'number_of_units': [1, 1, 1, 1, 1],
    'polyunsaturated_fat': [0.1, 0.1, 0.7, 0, 12],
    'potassium': [107, 358, 256, 316, 705],
    'protein': [0.3, 1.1, 31, 3.7, 21],
    'saturated_fat': [0, 0.1, 1, 0.1, 3.7],
    'sodium': [1, 1, 74, 33, 1],
    'sugar': [10, 12, 0, 2.4, 4.2],
    'trans_fat': [0, 0, 0, 0, 0],
    'vitamin_a': [54, 64, 13, 567, 1],
    'vitamin_c': [5, 8.7, 0, 89.2, 0]
}

# Load the data into a DataFrame
df = pd.DataFrame(data)

# Create a Streamlit app
st.title('Nutritional Data Visualization')

# Display the DataFrame
st.write("## Nutritional Data")
st.dataframe(df)

# 1. Total Nutrients Overview
st.write("## Total Nutrients Overview")
total_nutrients = df.drop(columns=['Food Item', 'Quantity', 'Unit', 'Multiplicity', 'measurement_description', 'number_of_units']).sum()
fig1 = px.bar(total_nutrients, title='Total Amount of Each Nutrient')
st.plotly_chart(fig1)

# 2. Nutrient Distribution
st.write("## Nutrient Distribution")
nutrients = ['calcium', 'calories', 'carbohydrate', 'cholesterol', 'fat', 'fiber', 'iron', 'potassium', 'protein', 'saturated_fat', 'sodium', 'sugar']
fig2 = px.box(df, y=nutrients, title='Distribution of Key Nutrients')
st.plotly_chart(fig2)

# 3. Caloric Contribution
st.write("## Caloric Contribution")
fig3 = px.pie(df, values='calories', names='Food Item', title='Caloric Contribution by Food Item')
st.plotly_chart(fig3)

# 4. Correlation Heatmap
st.write("## Nutrient Correlation Heatmap")
corr = df.drop(columns=['Food Item', 'Quantity', 'Unit', 'Multiplicity', 'measurement_description', 'number_of_units']).corr()
fig4, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig4)

# Add a button to save the dataframe to a CSV file
if st.button("Save Data to CSV"):
    filename = f"nutritional_data_{pd.Timestamp.today().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    st.success(f"Data saved to {filename}")
