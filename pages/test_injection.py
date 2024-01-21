import streamlit_survey as ss
import streamlit.components.v1 as components
import streamlit as st

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3000'
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

Dichotomy = ss.SurveyComponent.from_st_input(_dichotomy)


class CustomStreamlitSurvey(ss.StreamlitSurvey):
    # def dichotomy(self, label: str = "", id: str = None, **kwargs) -> str:
    #     return _qualitative_selector(
    #         component="dichotomy",
    #         name=kwargs["name"],
    #         key=kwargs["key"],
    #         question=kwargs["question"],
    #         rotationAngle=kwargs.get("rotationAngle", 0),
    #         gradientWidth=kwargs.get("gradientWidth", 40),
    #         invert=kwargs.get("invert", False),
    #         shift=kwargs.get("shift", 0)
    #     )

    def dichotomy(self, label: str = "", id: str = None, **kwargs) -> str:
        return Dichotomy(self, label, id, **kwargs).display()
    
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
                                        
                                        question="Dychotomies, including time...", 
                                        key="boundaries")
        st.write('You picked', return_value)

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
