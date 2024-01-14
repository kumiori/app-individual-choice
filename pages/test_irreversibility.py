import streamlit as st
import random
import string

# Function to corrupt a string
def corrupt_string(input_str, damage_parameter):
    symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~"
    num_chars_to_replace = int(len(input_str) * damage_parameter)
    indices_to_replace = random.sample(range(len(input_str)), num_chars_to_replace)
    corrupted_list = list(input_str)
    for index in indices_to_replace:
        corrupted_list[index] = random.choice(symbols)
    return ''.join(corrupted_list)

# Sample texts
texts = ["Text 1", "Text 2", "Text 3"]

# Initialization
if 'page_number' not in st.session_state:
    st.session_state.page_number = 0

if 'damage_parameter' not in st.session_state:
    st.session_state.damage_parameter = 0.1  # Initial damage parameter

last_page = len(texts) - 1
prev, _, next = st.columns([1, 10, 1])

if next.button("\>"):
    if st.session_state.page_number + 1 > last_page:
        st.session_state.page_number = 0
    else:
        st.session_state.page_number += 1

if prev.button("<"):
    if st.session_state.page_number - 1 < 0:
        st.session_state.page_number = last_page
    else:
        st.session_state.page_number -= 1
        # Increase damage parameter when < button is clicked
        st.session_state.damage_parameter += 0.05  # You can adjust the increment

# Display the current page number and damage parameter
st.write(f"Page Number: {st.session_state.page_number}")
st.write(f"Damage Parameter: {st.session_state.damage_parameter:.2f}")

# Display the corrupted text
corrupted_text = corrupt_string(texts[st.session_state.page_number], st.session_state.damage_parameter)
st.write(f"Corrupted Text: {corrupted_text}")
