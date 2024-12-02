import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import streamlit_tags as st_tags
from fatsecret import Fatsecret
from streamlit import secrets
from streamlit_scroll_navigation import scroll_navbar

app_id = secrets["food"]["FATSECRET_ID"]
app_key = secrets["food"]["FATSECRET_KEY"]

fs = Fatsecret(app_id, app_key)


# Anchor IDs and icons
anchor_ids = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"]
anchor_icons = ["info-circle", "lightbulb", "gear", "tag", "envelope"]


# 2. horizontal menu
st.subheader("Example 2", help="Horizontal menu")
scroll_navbar(
    anchor_ids, key="navbar2", anchor_icons=anchor_icons, orientation="horizontal"
)


if "weekly_intake" not in st.session_state:
    st.session_state.weekly_intake = None

if "food_data" not in st.session_state:
    # st.session_state.food_data = None
    st.session_state.food_data = []

if "food_info" not in st.session_state:
    st.session_state.food_info = pd.DataFrame(columns=["Food Item", "Quantity"])

if "food_ingredients" not in st.session_state:
    st.session_state.food_ingredients = []


# Placeholder functions for computation and data processing
def compute_rwi(data):
    # Placeholder for recommended weekly intake calculation
    return 2000  # Example value


def get_autocomplete_suggestions(query):
    # Placeholder for autocomplete suggestions
    return ["Bananas", "Apples", "Oranges", "Broccoli"]


def paginator(label, items, items_per_page=10, on_sidebar=False):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.

    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    page_number = location.selectbox(
        label, range(n_pages), format_func=page_format_func
    )

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    # import itertools

    # return itertools.islice(enumerate(items), min_index, max_index)

    # Return the chunk of items for the current page
    return list(enumerate(items[min_index:max_index]))


def fetch_food_data(food_query):
    alternatives = []
    search_results = fs.foods_search(food_query)
    if not search_results:
        return None
    generic_foods = [
        food for food in search_results if food.get("food_type") == "Generic"
    ]
    # st.info(f"Found {len(generic_foods)} generic foods")

    if not generic_foods:
        return None

    food = generic_foods[0]
    if len(generic_foods) > 1:
        alternatives.append(
            [generic_foods[i]["food_name"] for i in range(1, len(generic_foods))]
        )
    food_name = food["food_name"]
    print(food["food_description"])
    description_parts = food["food_description"].split("|")
    per_100g_part = description_parts[0].strip().split("-")
    quantitative_data = {
        part.split(":")[0].strip(): part.split(":")[1].strip()
        for part in description_parts[1:]
    }

    # Create a dictionary with all the relevant data
    food_data = {
        "Food Name": food_name,
        "Per 100g": per_100g_part[1].strip(),
        **quantitative_data,
    }

    return food_data, alternatives


def update_quantity(index):
    value = st.session_state.get(f"slider_{index}")
    st.session_state.food_info.at[index, "Quantity"] = value


def get_nutrient_info(food_item):
    # Perform food search to get food_id
    # st.write(f"Searching for {food_item}...")
    try:
        search_results = fs.foods_search(food_item)
        # st.write(search_results)
        generic_foods = [
            food for food in search_results if food.get("food_type") == "Generic"
        ]
        if not generic_foods:
            return {"Error": "No generic food found"}
        # else:
        # st.write(f"Found {len(generic_foods)} generic foods")
        food_id = generic_foods[0]["food_id"]

        # Get detailed nutritional info by food_id
        food_details = fs.food_get(food_id)
        if "servings" in food_details:
            servings = food_details["servings"]["serving"]
            if isinstance(
                servings, dict
            ):  # If there's only one serving, it's returned as a dict
                servings = [servings]
            # Find the serving with metric_serving_amount of 100 and metric_serving_unit of 'g'
            target_serving = next(
                (
                    serving
                    for serving in servings
                    if serving.get("metric_serving_amount") == "100.000"
                    and serving.get("metric_serving_unit") == "g"
                ),
                None,
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


# Initialize session state for selected ingredients
if "selected_staples2" not in st.session_state:
    st.session_state["selected_staples2"] = set()


# Define the callback to handle removal of ingredients
def remove_ingredients():
    print(st.session_state["selected_to_remove"])
    print("original", st.session_state["selected_staples2"])
    st.session_state["selected_staples2"] = [
        item
        for item in st.session_state["selected_staples2"]
        if item not in st.session_state["selected_to_remove"]
    ]
    print("changed", st.session_state["selected_staples2"])
    print(f"new len {len(st.session_state['selected_staples2'])}")
    st.session_state["selected_to_remove"] = []  # Reset selection after removal


# Sample data for dietary preferences polar plots
macro_splits = {
    "vegetarian": {"Carbohydrates": 60, "Proteins": 20, "Fats": 20},
    "vegan": {"Carbohydrates": 65, "Proteins": 15, "Fats": 20},
    "pescatarian": {"Carbohydrates": 55, "Proteins": 25, "Fats": 20},
    "flexitarian": {"Carbohydrates": 50, "Proteins": 25, "Fats": 25},
    "carnivore": {"Carbohydrates": 10, "Proteins": 70, "Fats": 20},
    "omnivore": {"Carbohydrates": 50, "Proteins": 25, "Fats": 25},
    "gluten-free": {"Carbohydrates": 40, "Proteins": 30, "Fats": 30},
    "keto": {"Carbohydrates": 5, "Proteins": 20, "Fats": 75},
    "paleo": {"Carbohydrates": 25, "Proteins": 30, "Fats": 45},
    "low-carb": {"Carbohydrates": 20, "Proteins": 40, "Fats": 40},
}
df = pd.DataFrame(macro_splits).T

# Streamlit application
st.title("Food Nutritional Application")

option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
}
selection = st.segmented_control(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "Your selected option: " f"{None if selection is None else option_map[selection]}"
)

# Stage 1: Determination of weekly necessary nutrients
st.header("Stage 1: Determination of Weekly Necessary Nutrients", anchor="Stage 1")
with st.form(key="rwi_form"):
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    height = st.number_input("Height (cm)", min_value=0, max_value=250, value=175)
    weight = st.number_input("Weight (kg)", min_value=0, max_value=300, value=70)
    gender = st.selectbox("Gender", ["Male", "Female"])
    activity = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Lightly active",
            "Moderately active",
            "Very active",
            "Extra active",
        ],
    )
    submit_button = st.form_submit_button(label="Compute")

    if submit_button:
        data = {
            "age": age,
            "height": height,
            "weight": weight,
            "gender": gender,
            "activity": activity,
        }
        weekly_intake = compute_rwi(data) * 7
        st.session_state.weekly_intake = weekly_intake
        st.success(
            f"Recommended Weekly Intake: {weekly_intake} kcal, {weekly_intake * 4.184} kJ"
        )

# Stage 2: Selection of dietary preferences
st.header("Stage 2: Selection of Dietary Preferences", anchor="Stage 2")
selected_preference = st.selectbox("Select Your Dietary Preference", df.index)
st.markdown(f"### {selected_preference}")
st.write(df.loc[selected_preference])
fig = go.Figure(
    data=go.Barpolar(
        r=df.loc[selected_preference],
        theta=["Carbohydrates", "Proteins", "Fats"],
    )
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Stage 3: Identification of set of preferred food items
st.header("Stage 3: Identification of Preferred Food Items", anchor="Stage 3")
food_items = st_tags.st_tags(
    label="## Food items",
    text="Food items",
    suggestions=[],
)

if food_items not in st.session_state:
    st.session_state.food_items = []
    print("food_items not in session state, initialised")

if food_items:
    st.write(f"`{[str(s).title() for s in food_items]}`")
    st.session_state.food_items = [str(s).title() for s in food_items]
elif food_items == [] and st.session_state.food_items:
    st.write(f"`{[str(s).title() for s in st.session_state.food_items]}`")

# if st.button("Search"):
#     try:
#         # Fetch data for all food items and store in a list of dictionaries
#         all_food_data = []
#         all_alternatives = []

#         for food_query in food_items:
#             food_data, alternatives = fetch_food_data(food_query)
#             if food_data:
#                 all_food_data.append(food_data)
#                 all_alternatives.append(alternatives)
#             else:
#                 st.warning(f"No generic food data found for {food_query}")

#         if not all_food_data:
#             raise Exception("No results found")

#         # Convert the list of dictionaries to a pandas DataFrame
#         df = pd.DataFrame(all_food_data)

#         # Display the DataFrame in Streamlit
#         st.dataframe(df)
#         st.write(all_alternatives)
#     except Exception as e:
#         st.error(f"Error: {e}")

# Stage 4: Equalisation of the quantities
st.header("Stage 4: Equalisation of Quantities", anchor="Stage 4")
import numpy as np


st.write(
    "### ",
    selected_preference,
    macro_splits[selected_preference],
    " is the selected dietary preference. The recommended weekly intake is ",
    st.session_state.weekly_intake,
    " kcal, ",
    "in Joule",
    st.session_state.weekly_intake * 4.184,
)


# Conversion factors
calories_per_gram = {"Carbohydrates": 4, "Proteins": 4, "Fats": 9}
print(macro_splits[selected_preference])

# Compute grams for each macro
necessary_grams = {
    macro: (percentage / 100 * st.session_state.weekly_intake)
    / calories_per_gram[macro]
    for macro, percentage in macro_splits[selected_preference].items()
}

# Display results
st.markdown("### Necessary grams for each macro per week:")
for macro, grams in necessary_grams.items():
    st.write(f"{macro}: {grams:.2f} g")

st.write(
    "This stage will involve adjusting the quantities of selected food items to match the nutritional needs."
)

# Stage 5: Possible refinement of food items
st.header("Stage 5: Refinement of Food Items", anchor="Stage 5")
st.write(
    "This stage will involve refining the selection of food items based on user feedback or additional criteria."
)


cuisine_options = [
    "Middle European Cuisine",
    "Mediterranean",
    "Asian",
    "Latin-American",
    "Middle-Eastern",
]

staple_ingredients = {
    "Middle European Cuisine": [
        "Potatoes",
        "Onions",
        "Carrots",
        "Butter",
        "Flour",
        "Cabbage",
        "Sausages",
    ],
    "Mediterranean": [
        "Olive Oil",
        "Tomatoes",
        "Garlic",
        "Herbs (Thyme, Oregano)",
        "Lemons",
        "Feta Cheese",
        "Pasta",
    ],
    "Asian": [
        "Soy Sauce",
        "Rice",
        "Ginger",
        "Garlic",
        "Chili Paste",
        "Tofu",
        "Noodles",
    ],
    "Latin-American": [
        "Corn Tortillas",
        "Black Beans",
        "Avocado",
        "Lime",
        "Cilantro",
        "Chili Peppers",
        "Rice",
    ],
    "Middle-Eastern": [
        "Chickpeas",
        "Tahini",
        "Olive Oil",
        "Cumin",
        "Pita Bread",
        "Yogurt",
        "Lentils",
    ],
}


# Initialize session state for selected ingredients
if "selected_staples" not in st.session_state:
    st.session_state["selected_staples"] = {cuisine: [] for cuisine in cuisine_options}


# User Selection for Cuisine Type

st.write("### Choose Your Basic Cuisine Setup")
selected_cuisine = st.pills(
    "Cuisine Types", options=cuisine_options, selection_mode="single", format_func=str
)

"""### Add vegetables"""

"""### Protein versus energy, heatmap"""

"""### Add custom ingredient (from label)
    how much a standard portion is worth? 
    
    Recipe: Kama
"""

"""
Go to the market
add nutritional yeast
"""

if selected_cuisine:
    # Display the corresponding staple ingredients
    st.write(f"### Staple Ingredients for {selected_cuisine}:")
    selected_ingredients = st.pills(
        "Staple Ingredients",
        options=staple_ingredients[selected_cuisine],
        selection_mode="multi",
        format_func=str,
    )

    # Show selected staple ingredients
    if selected_ingredients:
        st.markdown(f'Selected: {", ".join(selected_ingredients)}')
        st.session_state["selected_staples"][selected_cuisine] = selected_ingredients

    all_selected_ingredients = [
        f"{', '.join(ingredients)}"
        for cuisine, ingredients in st.session_state["selected_staples"].items()
        if ingredients
    ]
    # st.markdown("\n ### ".join(all_selected_ingredients))
    _all_ingredients = [
        ingredients
        for cuisine, ingredients in st.session_state["selected_staples"].items()
    ]
    # st.json(st.session_state["selected_staples"])
    flat_ingredients = set(item for sublist in _all_ingredients for item in sublist)
    st.session_state["food_ingredients"] = flat_ingredients

    f"""### Selected {len(flat_ingredients)} Staple Ingredients"""
    # st.pills("Remove Ingredients", options=flat_ingredients, selection_mode="multi")
    st.markdown("### " + ", ".join(sorted(st.session_state["food_ingredients"])))

    # st.write("### Select Ingredients to Remove")
    # st.session_state["selected_to_remove"] = st.pills(
    #     "Ingredients to Remove",
    #     options=st.session_state["selected_staples2"],
    #     selection_mode="multi",
    #     format_func=str,
    #     on_change=remove_ingredients,
    #     key="remove_ingredients",
    # )

    # if st.session_state["selected_staples2"]:
    #     st.write(", ".join(sorted(st.session_state["selected_staples2"])))


# create a long list of elements to showcase the paginator
elements = list(range(100))

# for i, fruit in paginator("Select a fruit page", elements):
#     st.write("%s. **%s**" % (i, fruit))

# Example list of food items
food_items = [
    "Kiwifruit",
    "Honeydew",
    "Cherry",
    "Honeyberry",
    "Pear",
    "Apple",
    "Nectarine",
    "Soursop",
    "Pineapple",
    "Satsuma",
    "Fig",
    "Huckleberry",
    "Coconut",
    "Plantain",
    "Jujube",
    "Guava",
    "Clementine",
    "Grape",
    "Tayberry",
    "Salak",
    "Raspberry",
    "Loquat",
    "Nance",
    "Peach",
    "Akee",
]

st.divider()
st.title("Food Item Selector with Pagination")

# Paginate the food items
paginated_items = paginator(
    "Select a page of food items", food_items, items_per_page=15
)
# Display the items on the current page using st.pills
if paginated_items:
    st.write("### Choose from the following items:")
    _, current_page_items = zip(*paginated_items)
    selected_items = st.pills(
        label="Select your items", options=current_page_items, selection_mode="multi"
    )

    st.write("### Selected Items:")
    st.write(selected_items)

st.divider()

if st.session_state.food_items and st.session_state.food_ingredients:
    st.write("### List of Items:")
    all_food_items = set(st.session_state.food_items).union(
        st.session_state.food_ingredients
    )
    st.write(all_food_items)
    # now search food data
    # Fetch data for all food items and store in a list of dictionaries

    if st.button("Basic search", key="search"):
        try:
            # Fetch data for all food items and store in a list of dictionaries
            all_food_data = []
            all_alternatives = []

            for food_query in all_food_items:
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
            st.session_state.food_data = df
            # st.write(all_alternatives)
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button(f"Get detailed info ({len(all_food_items)} ingredients)"):
        progress_bar = st.progress(0)
        nutrient_data = []
        total_items = len(all_food_items)

        with st.spinner("Fetching nutrient information..."):
            # for idx, row in st.session_state.food_data.iterrows():
            for idx, food_item in enumerate(all_food_items):
                # food_item = row["Food Item"]
                st.session_state.food_info.at[idx, "Food Item"] = food_item
                nutrient_info = get_nutrient_info(food_item)
                for nutrient, value in nutrient_info.items():
                    print(nutrient, value)
                    st.session_state.food_info.at[idx, nutrient] = value
                progress_bar.progress((idx + 1) / total_items)

            st.success("Market information fetched successfully")
            st.write("Updated List of Food Items:")

            st.session_state.food_info.drop(
                columns=[
                    "metric_serving_amount",
                    "metric_serving_unit",
                    "serving_description",
                    "measurement_description",
                    "serving_id",
                    "serving_url",
                    "serving_url",
                ],
                inplace=True,
            )
            st.dataframe(st.session_state.food_info)

    current_date = pd.Timestamp.now().strftime("%Y-%m-%d")

    csv_filename = f"food_info_{current_date}.csv"
    csv = st.session_state.food_data.to_csv(index=False)

    if st.download_button(
        label="Save CSV", data=csv, file_name=csv_filename, mime="text/csv"
    ):
        st.success(f"Saved {csv_filename}")

if st.session_state.food_data is not None:
    st.info("Market information fetched successfully")
    df = st.session_state.food_data
    st.dataframe(df.head(), use_container_width=True)

    for col in st.session_state.food_info.columns:
        if col != "Food Item":  # Skip 'Food Item' column
            st.session_state.food_info[col] = pd.to_numeric(
                st.session_state.food_info[col], errors="coerce"
            )

    df = st.session_state.food_info
    st.dataframe(df.head(), use_container_width=True)
    # st.write(st.session_state.food_items)
    # st.write(st.session_state.selected_staples2)

if st.session_state.food_info is not None:
    st.session_state.food_info["calories"] = pd.to_numeric(
        st.session_state.food_info["calories"], errors="coerce"
    )
    # st.write(df.columns)
    st.session_state.food_info["energy"] = st.session_state.food_info["calories"] * 4184

    st.info("Market information fetched successfully")
    df = st.session_state.food_info

    st.write("### Quantify Ingredients for Weekly Diet")
for index, row in st.session_state.food_info.iterrows():
    slider_value = st.slider(
        f"{row['Food Item']} (grams)",
        min_value=0,
        max_value=500,
        value=int(row["Quantity"]) if not np.isnan(row["Quantity"]) else 0,
        step=1,
        key=f"slider_{index}",
        on_change=update_quantity,
        args=(index,),
    )

st.table(st.session_state.food_info)
# Check if at least one quantity is not NaN
if st.session_state.food_info["Quantity"].notna().any():
    # Compute total macro nutrients based on quantities
    food_info = st.session_state.food_info
    food_info["Total Energy"] = food_info["Quantity"] * food_info["energy"] / 100
    food_info["Total Carbs"] = food_info["Quantity"] * food_info["carbohydrate"] / 100
    food_info["Total Protein"] = food_info["Quantity"] * food_info["protein"] / 100
    food_info["Total Fat"] = food_info["Quantity"] * food_info["fat"] / 100

    # Compute global totals
    total_energy = food_info["Total Energy"].sum()
    total_carbs = food_info["Total Carbs"].sum()
    total_protein = food_info["Total Protein"].sum()
    total_fat = food_info["Total Fat"].sum()
    total_mass = food_info["Quantity"].sum()

    # Display summary
    st.write("### Summary of Global Macro Nutrients")
    st.write(f"**Total energy:** {total_energy:.2f}")
    st.write(f"**Total Carbohydrates:** {total_carbs:.2f}")
    st.write(f"**Total Protein:** {total_protein:.2f}")
    st.write(f"**Total Fat:** {total_fat:.2f}")
    st.write(f"**Total Mass (kg):** {total_mass/1000:.1f}")
    st.write(
        f"**Total Water (kg):** {(total_mass - (total_carbs + total_protein+ total_fat))/1000:.1f}?"
    )

    # Display detailed table
    st.write("### Nutritional Table")
    st.dataframe(
        food_info[
            [
                "Food Item",
                "Quantity",
                "Total Energy",
                "Total Carbs",
                "Total Protein",
                "Total Fat",
            ]
        ],
        use_container_width=True,
    )
    computed_grams = {
        "Carbohydrates": total_carbs,
        "Proteins": total_protein,
        "Fats": total_fat,
    }
else:
    st.warning(
        "No quantities selected yet! Please adjust sliders to calculate nutritional information."
    )

if computed_grams and necessary_grams:
    st.write("### Comparison of Necessary and Computed Nutrients")
    st.write("#### Necessary Nutrients:")
    st.write(necessary_grams)
    st.write("#### Computed Nutrients:")
    st.write(computed_grams)

from scipy.optimize import linprog


# Selection of ingredients to optimize against
st.write("### Select 3 Ingredients to Optimize:")
selected_ingredients = st.multiselect(
    "Choose ingredients for optimization:",
    options=st.session_state.food_info["Food Item"],
    max_selections=3,
)


# Optimization button
necessary_nutrients = necessary_grams
computed_nutrients = computed_grams

if st.button("Compute Optimal Quantities") and len(selected_ingredients) == 3:
    # Extract the nutrient values for the selected ingredients
    selected_data = st.session_state.food_info[
        st.session_state.food_info["Food Item"].isin(selected_ingredients)
    ]
    st.write(selected_data)
    # Nutrient matrix (rows: nutrients, cols: ingredients)
    A = selected_data[["carbohydrate", "protein", "fat"]].values.T

    # Target vector (necessary nutrients)
    b = np.array(
        [
            necessary_nutrients["Carbohydrates"],
            necessary_nutrients["Proteins"],
            necessary_nutrients["Fats"],
        ]
    )
    st.write(A)
    # Solve for the quantities (linear system: A*x = b)
    try:
        quantities = np.linalg.solve(A, b)
        result = dict(zip(selected_ingredients, quantities))
        st.write("### Optimal Quantities:")
        st.json(result)

        # Update quantities in the DataFrame
        for ingredient, quantity in result.items():
            st.session_state.food_info.loc[
                st.session_state.food_info["Food Item"] == ingredient, "Quantity"
            ] = quantity

        st.write("### Updated Food Information:")
        st.dataframe(st.session_state.food_info)

    except np.linalg.LinAlgError as e:
        st.error(
            "Optimization failed: The selected ingredients might be linearly dependent."
        )
else:
    st.info("Select exactly 3 ingredients to optimise against and hit the button.")


def compute_macros(df):
    """
    Recomputes the overall macro nutrients for a given dataset.

    Args:
        df (pd.DataFrame): DataFrame containing the food data.
                           It must have columns 'Quantity', 'Carbohydrates', 'Proteins', 'Fats'.

    Returns:
        dict: A dictionary with the total amounts of Carbohydrates, Proteins, and Fats.
    """
    # Ensure all necessary columns are present
    required_columns = ["Quantity", "carbohydrate", "protein", "fat"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Replace NaN quantities with 0 (assuming those items are not included)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)

    # Compute total macros
    total_carbs = (df["Quantity"] * df["carbohydrate"]).sum()
    total_proteins = (df["Quantity"] * df["protein"]).sum()
    total_fats = (df["Quantity"] * df["fat"]).sum()

    return {
        "carbohydrate": total_carbs,
        "protein": total_proteins,
        "fat": total_fats,
    }


st.write(compute_macros(st.session_state.food_info))

df = st.session_state.food_info
st.write("## Nutrient Distribution")
nutrients = [
    "calcium",
    "calories",
    "carbohydrate",
    "cholesterol",
    "fat",
    "fiber",
    "iron",
    "potassium",
    "protein",
    "saturated_fat",
    "sodium",
    "sugar",
]
fig2 = px.box(df, y=nutrients, title="Distribution of Key Nutrients")
st.plotly_chart(fig2)

# 3. Caloric Contribution
st.write("## Energy Contribution")
fig3 = px.pie(
    df, values="calories", names="Food Item", title="Energy Contribution by Food Item"
)
st.plotly_chart(fig3)

st.write("## Carbs Contribution")
fig3 = px.pie(
    df,
    values="carbohydrate",
    names="Food Item",
    title="Carbs Contribution by Food Item",
)
st.plotly_chart(fig3)

st.write("## Protein Contribution")
fig3 = px.pie(
    df,
    values="protein",
    names="Food Item",
    title="Protein Contribution by Food Item",
)
st.plotly_chart(fig3)

st.write("## Fat Contribution")
fig3 = px.pie(
    df,
    values="fat",
    names="Food Item",
    title="Fat Contribution by Food Item",
)
st.plotly_chart(fig3)
