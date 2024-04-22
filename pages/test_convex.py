import streamlit as st

# Function to calculate the convex combination
def calculate_convex_combination(values):
    return sum(values)

# Function to check if the combination is valid
def is_valid_combination(values):
    return sum(values) <= 1

def rescale_values(values):
    total = sum(values)
    return [value / total for value in values]

# Main function to run the app
def main():
    st.title("Convex Combination Visualizer")


    # Initialize session state
    if "slider_values" not in st.session_state:
        st.session_state.slider_values = {"value1": 0.5, "value2": 0.3, "value3": 0.2}

    # Define three sliders for the convex combination
    with st.container():
        st.subheader("Adjust the Values")
        st.session_state.slider_values["value1"] = st.slider(
            "Value 1",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            value=st.session_state.slider_values["value1"]
        )
        st.session_state.slider_values["value2"] = st.slider(
            "Value 2",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            value=st.session_state.slider_values["value2"]
        )
        st.session_state.slider_values["value3"] = st.slider(
            "Value 3",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            value=st.session_state.slider_values["value3"]
        )

    # Retrieve slider values
    value1 = st.session_state.slider_values["value1"]
    value2 = st.session_state.slider_values["value2"]
    value3 = st.session_state.slider_values["value3"]

    # Calculate the convex combination
    convex_combination = calculate_convex_combination([value1, value2, value3])

    # Check if the combination is valid
    if not is_valid_combination([value1, value2, value3]):
        st.toast("Invalid combination! The sum of values cannot exceed 1. Values have been rescaled")
        # Rescale the values to fit the constraint
        st.session_state.slider_values["value1"], st.session_state.slider_values["value2"], st.session_state.slider_values["value3"] = rescale_values([value1, value2, value3])
        st.rerun()


    # Calculate uncertainty
    uncertainty = 1.0 - convex_combination

    # Display the combination
    st.subheader("Convex Combination")
    st.write(f"Value 1: {value1}")
    st.write(f"Value 2: {value2}")
    st.write(f"Value 3: {value3}")
    st.write(f"Convex Combination: {convex_combination}")
    st.write(f"Uncertainty: {uncertainty}")

if __name__ == "__main__":
    main()
