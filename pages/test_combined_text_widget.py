import streamlit as st

# Example data
panel = ["Text 0", "Text 1", "Text 2", "Text 3"]
widget_info = [
    {"type": "button", "key": "button_0"},
    {"type": "dichotomy", "key": "dichotomy_1"},
    {"type": "qualitative", "key": "qualitative_2"},
    {"type": "button", "key": "button_3"},
]

# Dictionary for text strings
text_dict = {f"text_{i}": panel[i] for i in range(len(panel))}

# Dictionary for streamlit widgets
widget_dict = {}

# Function to create button widget
def create_button(key):
    return st.button(label=key)

# Function to create dichotomy widget
def create_dichotomy(key):
    return st.checkbox("Choose one:", key=key)

# Function to create qualitative widget
def create_qualitative(key):
    return st.radio("Select one:", ["Option 1", "Option 2", "Option 3"], key=key)

# Dictionary mapping widget types to creation functions
widget_creators = {
    "button": create_button,
    "dichotomy": create_dichotomy,
    "qualitative": create_qualitative,
}

# Create widgets based on widget_info
for i, info in enumerate(widget_info):
    widget_key = info["key"]
    widget_type = info["type"]

    st.write(text_dict[f"text_{i}"])
    if widget_type in widget_creators:
        widget_dict[widget_key] = widget_creators[widget_type](widget_key)

# Example usage

st.divider()
for i in range(len(panel)):
    st.write(text_dict[f"text_{i}"])
    if widget_info[i]["key"] in widget_dict:
        widget_dict[widget_info[i]["key"]]

