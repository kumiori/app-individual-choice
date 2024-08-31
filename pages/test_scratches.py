import streamlit as st

# Function to collect scratches
def collect_scratches():
    scratches = {}
    scratch_1 = st.text_input("Scratch 1", key="scratch_1")
    if scratch_1:
        scratches["Scratch 1"] = scratch_1
        scratch_2 = st.text_input("Scratch 2", key="scratch_2")
        if scratch_2:
            scratches["Scratch 2"] = scratch_2
            scratch_3 = st.text_input("Scratch 3", key="scratch_3")
            if scratch_3:
                scratches["Scratch 3"] = scratch_3
                scratch_4 = st.text_input("Scratch 4", key="scratch_4")
                if scratch_4:
                    scratches["Scratch 4"] = scratch_4
                    scratch_5 = st.text_input("Scratch 5", key="scratch_5")
                    if scratch_5:
                        scratches["Scratch 5"] = scratch_5
    return scratches

scratches = collect_scratches()

if scratches:
    st.write("Scratches collected:", scratches)