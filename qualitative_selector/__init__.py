import streamlit.components.v1 as components
import streamlit as st

st.text("Hello")

_my_component = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)


def my_component(name, greeting="Hello", key=None):
    return _my_component(name=name, greeting=greeting, default=0, key=key)

return_value = my_component(name = "Spirit", key = "Ahoi")
st.write('You picked me:', return_value)

# return_value = my_component(name = "Mai-Brit", greeting='Ahoi', key="foo")
# st.write('You tricked me', return_value)
# _my_component(key="bar")