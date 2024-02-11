import streamlit as st

def display_dictionary(dictionary):
    """
    Function to display dictionary keys and content.
    """

    for key, content in dictionary.items():
        col1, _, col2 = st.columns([2, .1, 2])
        with col1:
            st.markdown(f"{key}")
        with col2:
            st.markdown(f"{list(content)[0]}", unsafe_allow_html=True)
        st.divider()

def display_dictionary_by_indices(dictionary, indices=None):
    """
    Function to display the data contained in dictionary for a specified subset using indices.
    """
    categories = list(dictionary.keys())
    if indices is None:
        indices = range(len(categories))
    else:
        indices = sorted(set(indices))  # Ensure uniqueness and sort the indices

    sliced_items = list(dictionary.items())[indices[0]:indices[1]]

    # Convert the sliced items back to a dictionary
    sliced_dict = dict(sliced_items)

    for category, content in sliced_dict.items():
        col1, _, col2 = st.columns([3, .3, 4])
    
        with col1:
            st.markdown(f"{category}")
        with col2:
            st.markdown(list(content)[0])
        st.divider()
            
def display_details_description(category, details):
    """
    Function to display category and its description.
    """
    col1, _, col2 = st.columns([2, .1, 2])
    with col1:
        st.markdown(f"{category}")
    # for sub_category, description in details.items():
    with col2:
        st.markdown(f" {details}")
    st.write("---")
