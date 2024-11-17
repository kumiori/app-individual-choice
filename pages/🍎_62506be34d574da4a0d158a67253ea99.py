import streamlit as st
import streamlit_survey as ss
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit_tags as st_tags

# Initialize session state for food items if not already set
if "food_items" not in st.session_state:
    st.session_state["food_items"] = []


def compute_nutrient_contributions(food_data):
    # Compute the overall nutrient contributions based on quantities
    overall_energy = sum(
        food_data["Quantity"][i] * food_data["calories"][i] / 100
        for i in range(len(food_data))
    )
    overall_carbs = sum(
        food_data["Quantity"][i] * food_data["carbohydrate"][i] / 100
        for i in range(len(food_data))
    )
    overall_protein = sum(
        food_data["Quantity"][i] * food_data["protein"][i] / 100
        for i in range(len(food_data))
    )
    overall_fat = sum(
        food_data["Quantity"][i] * food_data["fat"][i] / 100
        for i in range(len(food_data))
    )

    return overall_energy, overall_carbs, overall_protein, overall_fat


def compute_protein_intake(
    weight,
    activity_level,
    age=None,
    is_pregnant=False,
    is_lactating=False,
    fasting_window=None,
):
    activity_factors = {
        "sedentary": 0.8,
        "lightly active": 1.0,
        "moderately active": 1.4,
        "very active": 1.6,
        "strength training": 2.0,
    }

    # Adjustments for age or special conditions
    if age and age >= 65:
        base_factor = 1.0  # Sarcopenia prevention
    elif is_pregnant:
        base_factor = 1.1
    elif is_lactating:
        base_factor = 1.3
    else:
        base_factor = activity_factors.get(activity_level.lower(), 0.8)
    # st.info(f"Base Factor: {base_factor}")
    # Compute minimum protein intake
    protein_intake = weight * base_factor

    return protein_intake


def calculate_bmr(
    gender, age, weight, height, lean_body_mass=None, formula="Mifflin-St Jeor"
):
    """
    Calculate the Basal Metabolic Rate (BMR) using one of five popular formulas.

    Parameters:
    - gender: str ("male" or "female")
    - age: int (years)
    - weight: float (kg)
    - height: float (cm)
    - lean_body_mass: float (kg, optional for Katch-McArdle)
    - formula: str (choose from "Mifflin-St Jeor", "Harris-Benedict", "Revised Harris-Benedict", "Katch-McArdle", "Schofield")

    Returns:
    - bmr: float (cal/day)
    """
    gender = gender.lower()
    if gender not in ["male", "female"]:
        raise ValueError("Invalid value for 'gender'. Choose 'male' or 'female'.")

    if formula == "Mifflin-St Jeor":
        if gender == "male":
            return 10 * weight + 6.25 * height - 5 * age + 5
        else:  # female
            return 10 * weight + 6.25 * height - 5 * age - 161

    elif formula == "Harris-Benedict":
        if gender == "male":
            return 66.47 + 13.75 * weight + 5.003 * height - 6.755 * age
        else:  # female
            return 655.1 + 9.563 * weight + 1.85 * height - 4.676 * age

    elif formula == "Revised Harris-Benedict":
        if gender == "male":
            return 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
        else:  # female
            return 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age

    elif formula == "Katch-McArdle":
        if lean_body_mass is None:
            raise ValueError(
                "Lean body mass is required for the Katch-McArdle formula."
            )
        return 370 + 21.6 * lean_body_mass

    elif formula == "Schofield":
        if gender == "male":
            if 18 <= age <= 30:
                return 15.057 * weight + 692.2
            elif 30 < age <= 60:
                return 11.472 * weight + 873.1
            else:  # age > 60
                return 11.711 * weight + 587.7
        else:  # female
            if 18 <= age <= 30:
                return 14.818 * weight + 486.6
            elif 30 < age <= 60:
                return 8.126 * weight + 845.6
            else:  # age > 60
                return 9.082 * weight + 658.5
    else:
        raise ValueError(
            "Invalid formula name. Choose from 'Mifflin-St Jeor', 'Harris-Benedict', 'Revised Harris-Benedict', 'Katch-McArdle', 'Schofield'."
        )


def mifflin_st_jeor(weight, height, age, gender):
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == "female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender must be either 'male' or 'female'")


def harris_benedict(weight, height, age, gender):
    if gender.lower() == "male":
        return 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
    elif gender.lower() == "female":
        return 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    else:
        raise ValueError("Gender must be either 'male' or 'female'")


def revised_harris_benedict(weight, height, age, gender):
    if gender.lower() == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == "female":
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender must be either 'male' or 'female'")


def katch_mcardle(lean_body_mass):
    return 370 + (21.6 * lean_body_mass)


def schofield(weight, age, gender):
    if gender.lower() == "male":
        if age <= 18:
            return 17.6 * weight + 656
        else:
            return 15.0 * weight + 692
    elif gender.lower() == "female":
        if age <= 18:
            return 13.3 * weight + 692
        else:
            return 14.8 * weight + 486
    else:
        raise ValueError("Gender must be either 'male' or 'female'")


# Example usage

if __name__ == "__main__":
    survey = ss.StreamlitSurvey()

    # Title of the app
    st.title("Dietary Plan Personalization")

    # Basic Information Section
    st.header("1. Basic Information")
    age = survey.number_input(
        "Age (years)", min_value=1, max_value=120, value=30, step=1
    )
    gender = survey.selectbox("Gender", options=["Male", "Female", "Other/Non-Binary"])
    height = survey.number_input(
        "Height (cm)", min_value=50, max_value=250, value=170, step=1
    )
    weight = survey.number_input(
        "Weight (kg)", min_value=10, max_value=200, value=70, step=1
    )

    # Activity Level Section
    st.header("2. Activity Level")
    activity_level = survey.selectbox(
        "Select your activity level",
        options=[
            "Sedentary (little or no exercise)",
            "Lightly Active (light exercise/sports 1-3 days/week)",
            "Moderately Active (moderate exercise/sports 3-5 days/week)",
            "Very Active (hard exercise/sports 6-7 days/week)",
            "Extra Active (very hard exercise/physical job)",
        ],
    )

    # Dietary Goals Section
    st.header("3. Dietary Goals")
    dietary_goal = survey.radio(
        "What is your dietary goal?",
        options=["Weight Loss", "Weight Maintenance", "Weight Gain", "Other"],
    )

    # Dietary Preferences Section
    st.header("4. Dietary Preferences")
    dietary_restrictions = st.multiselect(
        "Do you follow any specific dietary restrictions?",
        options=[
            "Vegetarian",
            "Vegan",
            "Pescatarian",
            "Gluten-Free",
            "Lactose-Free",
            "Keto",
            "Paleo",
            "None",
            "Other",
        ],
    )
    allergies = survey.text_input(
        "Do you have any allergies? (e.g., nuts, dairy, shellfish)"
    )
    preferred_foods = survey.text_area("What are your favorite foods?")
    disliked_foods = survey.text_area("Are there any foods you'd like to avoid?")

    # Macronutrient Preferences Section
    st.header("5. Macronutrient Preferences")
    custom_split = survey.checkbox(
        "Would you like to customize your macronutrient split?"
    )
    if custom_split:
        carbs_split = survey.slider("Carbohydrates (%)", 0, 100, 50, step=1)
        proteins_split = survey.slider("Proteins (%)", 0, 100, 25, step=1)
        fats_split = survey.slider("Fats (%)", 0, 100, 25, step=1)
        total_split = carbs_split + proteins_split + fats_split
        if total_split != 100:
            st.warning(
                "The total macronutrient split must sum to 100%. Please adjust your values."
            )
    else:
        st.write("Default split will be used based on your goal.")

    # Intermittent Fasting
    st.header("2. Intermittent Fasting Preferences")
    enable_fasting = survey.checkbox("Do you practice intermittent fasting?")
    fasting_window = None

    if enable_fasting:
        fasting_schedule = survey.radio(
            "Select your fasting schedule",
            options=[
                "16/8 (16 hrs fasting, 8 hrs eating)",
                "18/6 (18 hrs fasting, 6 hrs eating)",
                "20/4 (20 hrs fasting, 4 hrs eating)",
            ],
        )
        meals = survey.number_input(
            "Number of meals/snacks in eating window",
            min_value=1,
            max_value=6,
            value=3,
            step=1,
        )

        # Parse the eating hours based on the selection
        eating_hours = int(fasting_schedule.split("/")[1].split(" ")[0])
        fasting_window = {"eating_hours": eating_hours}

    # Compute protein intake
    activity = activity_level.split("(")[0].strip().lower()
    st.info(f"Activity Level: {activity}")
    # Meal Preferences Section
    st.header("6. Meal Preferences")
    num_meals = survey.select_slider(
        "How many meals do you prefer to eat per day?",
        options=[1, 2, 3, 4, 5, 6],
        value=3,
    )
    snacks = survey.radio(
        "Would you like snacks included in your plan?", options=["Yes", "No"]
    )
    cooking_time = survey.selectbox(
        "How much time can you spend cooking daily?",
        options=["Less than 15 minutes", "15–30 minutes", "30–60 minutes", "No limit"],
    )
    cuisine_preferences = survey.text_area("Do you have any favorite cuisines?")

    # Special Requirements Section
    st.header("7. Special Requirements")
    medical_conditions = survey.text_area(
        "Do you have any medical conditions or dietary needs we should consider?"
    )
    supplements = survey.text_area(
        "Do you take any supplements? (e.g., multivitamins, protein powder)"
    )

    # Flexibility Feedback Section
    st.header("8. Plan Flexibility")
    plan_flexibility = survey.radio(
        "How flexible do you want your dietary plan to be?",
        options=[
            "Strict (Stick to the plan exactly)",
            "Moderate (Occasional substitutions allowed)",
            "Flexible (General guidelines)",
        ],
    )

    # Summary Section
    if st.button("Submit"):
        st.subheader("Your Input Summary:")
        st.write(f"**Age:** {age} years")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Height:** {height} cm")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Activity Level:** {activity_level}")
        st.write(f"**Dietary Goal:** {dietary_goal}")
        st.write(
            f"**Dietary Restrictions:** {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}"
        )
        st.write(f"**Allergies:** {allergies or 'None'}")
        st.write(f"**Preferred Foods:** {preferred_foods or 'None'}")
        st.write(f"**Disliked Foods:** {disliked_foods or 'None'}")
        if custom_split:
            st.write(
                f"**Macronutrient Split:** Carbs: {carbs_split}%, Proteins: {proteins_split}%, Fats: {fats_split}%"
            )
        st.write(f"**Number of Meals:** {num_meals}")
        st.write(f"**Snacks Included:** {snacks}")
        st.write(f"**Cooking Time:** {cooking_time}")
        st.write(f"**Cuisine Preferences:** {cuisine_preferences or 'None'}")
        st.write(f"**Medical Conditions:** {medical_conditions or 'None'}")
        st.write(f"**Supplements:** {supplements or 'None'}")
        st.write(f"**Plan Flexibility:** {plan_flexibility}")

        # Example Usage
        # user_weight = 70  # kg
        # user_activity = "moderately active"
        # user_age = 30

        protein_intake = compute_protein_intake(
            weight, activity, age, fasting_window=fasting_window
        )
        protein_needed = compute_protein_intake(
            weight, activity, age=age, fasting_window=fasting_window
        )
        st.info(f"Protein Intake: {protein_intake:.1f} g/day")
        st.info(f"Minimum Protein Intake: {protein_needed:.1f} g/day")

        if enable_fasting:
            st.write(f"**Fasting Schedule:** {fasting_schedule}")
            st.write(f"**Eating Window:** {fasting_window['eating_hours']} hours")
            st.write(
                f"**Adjusted Protein Intake:** {protein_intake:.2f} g spread across {fasting_window['eating_hours']} hours"
            )
            protein_per_meal = protein_intake / meals
            st.write(f"**Total Daily Protein Intake:** {protein_intake:.2f} g")
            st.write(f"**Protein per Meal/Snack:** {protein_per_meal:.2f} g")
        else:
            st.write(f"**Recommended Daily Protein Intake:** {protein_intake:.2f} g")

        st.success(
            "Thank you for providing your details! We will use this information to tailor your dietary plan."
        )

        with st.expander("Learn more about protein intake", expanded=False):
            """
                References

            1.	WHO/FAO/UNU Expert Consultation on Protein and Amino Acid Requirements (2007):
            •	WHO Technical Report Series 935. Available here.
            https://iris.who.int/bitstream/handle/10665/43411/WHO_TRS_935_eng.pdf
            2.	Academy of Nutrition and Dietetics, Dietitians of Canada, and the American College of Sports Medicine:
            •	Position Stand: Nutrition and Athletic Performance. PubMed Reference.
            https://pubmed.ncbi.nlm.nih.gov/26891166/
            3.	Institute of Medicine (IOM):
            •	Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Protein, and Amino Acids. Available here.
            https://nap.nationalacademies.org/catalog/10490/dietary-reference-intakes-for-energy-carbohydrate-fiber-fat-fatty-acids-cholesterol-protein-and-amino-acids
            """

    #     text = f"""
    # I am a {st.session_state.get('age', 'N/A')}-year-old {st.session_state.get('gender', 'N/A').lower()}, standing tall at {st.session_state.get('height', 'N/A')} cm and weighing {st.session_state.get('weight', 'N/A')} kg. My lifestyle is {st.session_state.get('activity_level', 'N/A').lower()}, involving regular moderate exercise or sports around three to five days a week. My current dietary goal is {st.session_state.get('dietary_goal', 'N/A').lower()}, and fortunately, I don't have any dietary restrictions, allergies, or medical conditions to consider.
    # When it comes to food, I have a particular preference for {st.session_state.get('preferred_foods', 'N/A')}, and while I don't strongly dislike any specific foods, I lean towards a balanced diet with a macronutrient split of {st.session_state.get('carb_split', 'N/A')}% carbohydrates, {st.session_state.get('protein_split', 'N/A')}% proteins, and {st.session_state.get('fat_split', 'N/A')}% fats.
    # I like to keep things simple and efficient in the kitchen, so my cooking time usually ranges between {st.session_state.get('cooking_time', 'N/A')}. I'm flexible with cuisines, happy to explore various flavors and styles. For my meals, I prefer {st.session_state.get('meals_per_day', 'N/A')} main meals a day, and I don't mind including snacks as part of my routine.
    # Recently, I've started practicing intermittent fasting, following a {st.session_state.get('fasting_schedule', 'N/A')} schedule. This means I fast for {st.session_state.get('fasting_hours', 'N/A')} hours and eat during a {st.session_state.get('eating_hours', 'N/A')}-hour window. Within this window, I plan my meals to meet my nutritional needs. Based on my profile, my total daily protein intake is calculated to be around {st.session_state.get('total_protein', 'N/A'):.2f} grams, which I distribute across my eating hours. With {st.session_state.get('meals_per_day', 'N/A')} meals a day, this means approximately {st.session_state.get('protein_per_meal', 'N/A'):.2f} grams of protein per meal or snack.
    # My approach to nutrition is flexible and adaptable. I'm open to general guidelines rather than rigid plans, aiming for a sustainable and enjoyable eating routine that aligns with my health and fitness goals.
    # """

    st.write(f"""{st.session_state.get('age', 'N/A')}""")

    # Test data
    # gender = "male"
    # age = 25
    # weight = 70  # in kg
    # height = 175  # in cm
    lean_body_mass = 60  # in kg

    # Calculate BMR using each formula
    formulas = [
        "Mifflin-St Jeor",
        "Harris-Benedict",
        "Revised Harris-Benedict",
        "Katch-McArdle",
        "Schofield",
    ]
    for formula in formulas:
        try:
            bmr = calculate_bmr(gender, age, weight, height, lean_body_mass, formula)
            st.write(f"{formula}: {bmr:.2f} kcal/day")
        except ValueError as e:
            st.write(f"{formula}: Error - {e}")

    ages = np.linspace(15, 80, 60)
    weight = 70  # kg
    height = 175  # cm
    gender = "male"

    # Collecting data for different models
    data = {
        "Age": ages,
        "Mifflin-St Jeor": [
            mifflin_st_jeor(weight, height, age, gender) for age in ages
        ],
        "Harris-Benedict": [
            harris_benedict(weight, height, age, gender) for age in ages
        ],
        "Revised Harris-Benedict": [
            revised_harris_benedict(weight, height, age, gender) for age in ages
        ],
        "Schofield": [schofield(weight, age, gender) for age in ages],
    }

    # Create a DataFrame for plotting
    df = pd.DataFrame(data)
    # st.table(df)
    # Plot using Plotly
    fig = px.line(
        df,
        x="Age",
        y=[
            "Mifflin-St Jeor",
            "Harris-Benedict",
            "Revised Harris-Benedict",
            "Schofield",
        ],
        labels={"value": "BMR (kcal/day)", "variable": "Model"},
        title="BMR Comparison Across Models",
    )
    fig.update_layout(template="plotly_dark")

    # Display plot in Streamlit
    st.plotly_chart(fig)

    st.json(survey.data)

    st.markdown(
        """
        ### Add Food Items to Your Diet
        Specify the food items you want to include in your diet. 
        Their quantities will remain as variables to be determined in the dietary plan.
        """
    )

    food_items = st_tags.st_tags(
        label="## Free Food items",
        text="Food items, unknown quantities",
        suggestions=[],
    )
    # Save food items to session state
    if food_items:
        st.session_state["food_items"] = food_items

    if st.button("Clear Food Items"):
        st.session_state["food_items"] = []

    # Display added food items
    if st.session_state["food_items"]:
        st.markdown("### Current Food Items")
        st.write(st.session_state["food_items"])

    "## Given Food items"
    uploaded_file = st.file_uploader("Given food data", type="csv")

    if uploaded_file is not None:
        uploaded_data = pd.read_csv(uploaded_file)
        # st.session_state.food_data = pd.concat([st.session_state.food_data, uploaded_data], ignore_index=True)
        st.session_state.food_data = uploaded_data
        st.success("CSV file loaded successfully")

        st.table(uploaded_data)

    st.session_state.food_data["energy"] = st.session_state.food_data["calories"] * 4184
    df = st.session_state.food_data

    overall_energy, overall_carbs, overall_protein, overall_fat = (
        compute_nutrient_contributions(df)
    )
    # st.write(res)

    # Macronutrient energy densities
    CARB_CALORIES_PER_GRAM = 4
    PROTEIN_CALORIES_PER_GRAM = 4
    FAT_CALORIES_PER_GRAM = 9

    st.header("Nutrient Contributions:")
    st.write(f"Overall Energy Content: {overall_energy:.2f} kcal")
    st.write(f"Overall Carbohydrates: {overall_carbs:.2f} grams")
    st.write(f"Overall Protein: {overall_protein:.2f} grams")
    st.write(f"Overall Fat: {overall_fat:.2f} grams")

    st.divider()
    cols = st.columns(3)

    with cols[0]:
        # Target energy requirement and nutrient split
        target_energy = st.number_input(
            "Target Energy Requirement (kcal/day)", value=1500
        )
        target_carbs = st.number_input(
            "Target Carbohydrates (%)", min_value=0, max_value=100, value=40
        )
        target_protein = st.number_input(
            "Target Protein (%)", min_value=0, max_value=100, value=30
        )
        target_fat = st.number_input(
            "Target Fat (%)", min_value=0, max_value=100, value=30
        )

        _target_carbs = target_carbs / 100 * target_energy
        _target_protein = target_protein / 100 * target_energy
        _target_fat = target_fat / 100 * target_energy

        # Convert to grams
        _target_carbs_grams = _target_carbs / CARB_CALORIES_PER_GRAM
        _target_protein_grams = _target_protein / PROTEIN_CALORIES_PER_GRAM
        _target_fat_grams = _target_fat / FAT_CALORIES_PER_GRAM

        # Display target energy and macronutrient breakdown
        st.write(f"### Target Energy and Macronutrient Breakdown per Day")
        st.write(f"Target Energy: {target_energy} kcal")
        st.write(
            f"Target Carbs: {_target_carbs:.2f} kcal ({_target_carbs_grams:.2f} g)"
        )
        st.write(
            f"Target Protein: {_target_protein:.2f} kcal ({_target_protein_grams:.2f} g)"
        )
        st.write(f"Target Fat: {_target_fat:.2f} kcal ({_target_fat_grams:.2f} g)")

    with cols[1]:

        # Calculate distance from target split
        distance_carbs = overall_carbs - _target_carbs_grams
        distance_protein = overall_protein - _target_protein_grams
        distance_fat = overall_fat - _target_fat_grams
        # Display results
        st.header("Nutrient Target:")
        st.write(f"Current Carbohydrates: {overall_carbs:.2f} grams")
        st.write(f"Current Protein: {overall_protein:.2f} grams")
        st.write(f"Current Fat: {overall_fat:.2f} grams")

        st.header("Weekly Target:")

        st.write(f"Target Carbs: ({7*_target_carbs_grams:.2f} g)")
        st.write(f"Target Protein: ({7*_target_protein_grams:.2f} g)")
        st.write(f"Target Fat: ({7*_target_fat_grams:.2f} g)")

    with cols[2]:
        # Display distance from target split
        st.header("Distance from Target Split:")
        st.write(f"Carbohydrates: {distance_carbs:.2f} grams")
        st.write(f"Protein: {distance_protein:.2f} grams")
        st.write(f"Fat: {distance_fat:.2f} grams")

    # Slider to adjust the protein coefficient
    protein_coefficient = st.slider(
        "Protein Coefficient (g/kg body weight)",
        min_value=0.8,
        max_value=2.0,
        value=1.5,
        step=0.1,
    )

    # Calculate minimum protein requirement
    min_protein_grams = weight * protein_coefficient

    # Add the constraint to the target protein
    if _target_protein_grams < min_protein_grams:
        st.warning(
            f"The computed target protein ({_target_protein_grams:.2f} g) is below the minimum recommended protein intake ({min_protein_grams:.2f} g)."
        )
    else:
        st.success(
            f"The computed target protein ({_target_protein_grams:.2f} g) meets the minimum recommended protein intake ({min_protein_grams:.2f} g)."
        )

    # Display the minimum protein constraint
    st.write(f"### Minimum Protein Constraint")
    st.write(f"Minimum Protein Requirement: {min_protein_grams:.2f} g")
