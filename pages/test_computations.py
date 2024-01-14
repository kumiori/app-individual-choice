import streamlit as st

# Define the computation function, including the sanity check
def perform_computation(selected_option, session_data):
    if selected_option == 'current_0':
        data = session_data.get('data_current_0')
        if data is None:
            return "Data for 'current_0' is missing. Please set the data and try again."
        result = f"Computation for 'current_0' with data: {data}"
    elif selected_option == 'quadratic_1':
        data = session_data.get('data_quadratic_1')
        if data is None:
            return "Data for 'quadratic_1' is missing. Please set the data and try again."
        result = f"Computation for 'quadratic_1' with data: {data}"
    elif selected_option == 'quadratic_with_choice_2':
        result = "Computation for 'quadratic_with_choice_2'"
    elif selected_option == 'capital_constrained_3':
        result = "Computation for 'capital_constrained_3'"
    else:
        result = "Select an option and click 'Run'."
    return result

# Create the Streamlit app
st.title("Computation App")

# Create radio buttons to select options
selected_option = st.radio("Select an option:", ('current_0', 'quadratic_1', 'quadratic_with_choice_2', 'capital_constrained_3'))

# Get the data from the user
data_current_0 = st.text_input("Data for 'current_0'")
data_quadratic_1 = st.text_input("Data for 'quadratic_1'")

# Create a button to set data in the session state
if st.button("Set Data"):
    if selected_option == 'current_0':
        st.session_state.data_current_0 = data_current_0
    elif selected_option == 'quadratic_1':
        st.session_state.data_quadratic_1 = data_quadratic_1

# Create a button to trigger the computation
if st.button("Run"):
    session_data = st.session_state
    result = perform_computation(selected_option, session_data)
    st.write("Result:")
    st.write(result)
