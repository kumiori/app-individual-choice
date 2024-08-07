import streamlit_survey as ss
import streamlit.components.v1 as components
import streamlit as st
from  streamlit_vertical_slider import vertical_slider 
import random

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


def main():

    # Usage example
    survey = CustomStreamlitSurvey()

    pages = survey.pages(2, on_submit=lambda: st.success("Your preferences are recorded. Thank you!"))

    with pages:
        if pages.current == 0:
            st.write("Experiments or Theory?")
            love_together = survey.radio(
                "love_together", options=["nan", "Experiments", "Theory"], index=0,
                label_visibility="collapsed", horizontal=True
            )

        elif pages.current == 1:
            st.write("How confident are you in Decentralised Science?")

            return_value = survey.dichotomy(name="Spirit", 
                                            label="Confidence",
                                            question="Dychotomies, including time...", 
                                            key="boundaries")
            st.write('You picked', return_value)

            return_value = survey.equaliser(label="Equaliser Dim 1",
                height=200,
                id="test_1",
                default_value=55,
                step=1,
                min_value=0,
                max_value=100,
                value_always_visible=True,)
            

            return_value = survey.equaliser(label="Equaliser Dim 2",
                height=200,
                key="test_2",
                default_value=55,
                step=1,
                min_value=0,
                max_value=100,
                value_always_visible=True,)
            


            bottom_cols = st.columns(3)
            
            for i, column in enumerate(bottom_cols):
                with column:
                    survey.equaliser(
                        label=f"Eq{i}",
                        height=200,
                        key=f"cat_{i}",
                        default_value=random.random() * 100,
                        step=1,
                        min_value=0,
                        max_value=100,
                        value_always_visible=True,
                    )
            
    # Retrieve survey data and display
    survey_data = survey.data
    st.write("Survey Data:", survey_data)

    from streamlit_survey.survey_component import (
        SelectSlider,
        SurveyComponent,
    )
    st.markdown("## AZIZ")
    st.write(survey._components)
    survey._add_component(SelectSlider)
    st.markdown("## after injection")
    st.write(survey._components)
    st.markdown("## after double injection")
    survey._add_component(_qualitative_selector)
    st.write(survey._components)
    st.write(survey.data)
if __name__ == "__main__":
    main()