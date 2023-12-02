import streamlit.components.v1 as components
import streamlit as st

st.text("Hello")

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)


def qualitative_selector(name, greeting="Hello", key=None):
    return _qualitative_selector(name=name, greeting=greeting, default=0, key=key)

return_value = qualitative_selector(name = "Spirit in passing", key = "Ahoi")
st.write('You picked me:', return_value)

