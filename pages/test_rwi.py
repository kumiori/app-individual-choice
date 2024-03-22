import streamlit as st

def compute_rwi(data):
    # Coefficients for the formula
    coefficients_male = {'c_0': 10, 'c_1': 0.5, 'c_2': 1.0, 'c_3': -2.0, 'c_4': 1.2}
    coefficients_female = {'c_0': 5, 'c_1': 0.4, 'c_2': 0.9, 'c_3': -1.5, 'c_4': 1.2}

    # Activity level coefficients
    activity_coefficients = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }

    # Check for missing data
    required_keys = ['age', 'height', 'weight', 'gender', 'activity']
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        raise ValueError(f'Missing data keys: {missing_keys}')

    # Extract data from the input dictionary
    age = data['age']
    height = data['height']
    weight = data['weight']
    gender = data['gender'].lower()  # Normalize to lowercase
    activity_level = data['activity'].lower()  # Normalize to lowercase

    # Validate activity level
    if activity_level not in activity_coefficients:
        raise ValueError(f'Invalid activity level: {activity_level}')

    # Select coefficients based on gender
    coefficients = coefficients_male if gender == 'male' else coefficients_female

    # Compute the weekly energetic intake
    x = (coefficients['c_0'] + coefficients['c_1'] * weight +
         coefficients['c_2'] * height + coefficients['c_3'] * age) * coefficients['c_4']

    # Adjust for daily intake (assuming 7 days in a week)
    weekly_intake = x * 7

    # Adjust for activity level
    adjusted_intake = weekly_intake * activity_coefficients[activity_level]

    return adjusted_intake

def main():
    st.title("Recommended Weekly Intake (RWI) Calculator")

    # Collect user input
    age = st.number_input("Enter your age:", min_value=1, max_value=150, step=1, key="age")
    height = st.number_input("Enter your height (in cm):", min_value=1, max_value=300, step=1, key="height")
    weight = st.number_input("Enter your weight (in kg):", min_value=1, max_value=500, step=1, key="weight")
    gender = st.selectbox("Select your gender:", ["Male", "Female"], key="gender").lower()
    activity_level = st.selectbox(
        "Select your activity level:",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
        key="activity"
    ).lower()

    # Calculate RWI on button click
    if st.button("Calculate Recommended Weekly Intake"):
        nutrition_data = {'age': age, 'height': height, 'weight': weight, 'gender': gender, 'activity': activity_level}
        try:
            result = compute_rwi(nutrition_data)
            st.success(f'Weekly Energetic Intake: {result:.2f} kcal')
        except ValueError as e:
            st.error(f'Error: {e}')

if __name__ == "__main__":
    main()
