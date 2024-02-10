import streamlit as st
import streamlit.components.v1 as components
import os
import sys

_RELEASE = True

if _RELEASE:
    st.write(os.path.basename(__file__))
    root_dir = os.path.dirname(__file__)

    # Print the root directory
    st.write("Root directory:", root_dir)
    build_dir = os.path.join(os.path.split(root_dir)[0], "qualitative_selector/frontend/build")
    st.write("Build directory:", build_dir)
    _qualitative_selector = components.declare_component("qualitiative", path=build_dir)
else:
    _qualitative_selector = components.declare_component(
        "qualitative",
        url='http://localhost:3000'
    )
    

def dichotomy(name, question, rotationAngle = 0, gradientWidth = 40, invert = False, shift = 0, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    key=key,
    question = question,
    rotationAngle = rotationAngle,
    gradientWidth = gradientWidth,
    invert = invert,
    shift = shift
    )


def main():

    return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "boundaries")
    st.write('You picked', return_value)

if __name__ == "__main__":
    main()
