import streamlit.components.v1 as components
import streamlit as st

st.text("Hello")

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)


def dichotomy(name, question, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    key=key,
    question = question)


def qualitative(name, question, data_values, key=None):
    return _qualitative_selector(component = "qualitative",
    name = name,
    key=key,
    data_values = data_values,
    question = question)

def qualitative_parametric(name, question, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    key=key,
    areas = areas,
    data_values  = [1, 2, 10],
    question = question)

return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "boundaries")
st.write('You picked me:', return_value)


return_value = qualitative(name = "Spirit", question = "How tricky is Quantity?", data_values = [1, 2, 10, 11, 25], key = "qualitative")
st.write('You picked me:', return_value)


return_value = qualitative_parametric(name = "Spirit",
     question = "Boundaries matter, see below...",
     areas = 3,
     key = "parametric")
st.write('You picked me:', return_value)

