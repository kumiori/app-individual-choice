import streamlit as st
import streamlit.components.v1 as components
from streamlit_vertical_slider import vertical_slider 
import streamlit_survey as ss
import os 

if st.secrets["runtime"]["STATUS"] == "Production":
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
        url='http://localhost:3001'
    )
    







def _dichotomy(name, question, label, rotationAngle = 0, gradientWidth = 40, invert = False, shift = 0, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    label = label,
    key=key,
    question = question,
    rotationAngle = rotationAngle,
    gradientWidth = gradientWidth,
    invert = invert,
    shift = shift
    )
    
def _qualitative(name, question, label, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    label = label,
    key=key,
    areas = areas,
    data_values  = [1, 2, 10],
    question = question)

Dichotomy = ss.SurveyComponent.from_st_input(_dichotomy)
VerticalSlider = ss.SurveyComponent.from_st_input(vertical_slider)
ParametricQualitative = ss.SurveyComponent.from_st_input(_qualitative)


class CustomStreamlitSurvey(ss.StreamlitSurvey):
    shape_types = ["circle", "square", "pill"]

    def dichotomy(self, label: str = "", id: str = None, **kwargs) -> str:
        return Dichotomy(self, label, id, **kwargs).display()
    
    def equaliser(self, label: str = "", id: str = None, **kwargs) -> str:
        return VerticalSlider(self, label, id, **kwargs).display()

    def qualitative_parametric(self, label: str = "", id: str = None, key=None, **kwargs):
        return ParametricQualitative(self, label, id, **kwargs).display()

