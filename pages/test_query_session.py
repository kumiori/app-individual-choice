import streamlit as st
import json
import streamlit_survey as ss
import streamlit.components.v1 as components

# Define a StreamlitSurvey class (simplified for this example)
# class StreamlitSurvey:
#     def __init__(self, name):
#         self.name = name

#     def pages(self, num_pages):
#         self.num_pages = num_pages
#         self.current = 0

# # Initialize the StreamlitSurvey
# survey = StreamlitSurvey("Survey")

_my_component = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)

# Initialize a session state object to store responses
if "session_state" not in st.session_state:
    st.session_state = {
        "pizza_response": None,
        "ice_cream_response": None,
        "component_response": None,
    }


def my_component(name, greeting="Hello", key=None):
    return _my_component(name=name, greeting=greeting, default=0, key=key)


st.title("Simple Survey")


with st.expander("Some questions:", expanded=True):
    survey = ss.StreamlitSurvey("Home")
    pages = survey.pages(3, on_submit=lambda: 
        st.success("Your responses have been recorded. Thank you!"))

    with pages:
        if pages.current == 0:
            st.write("Do you like pizza?")
            pizza_response = st.radio("Pizza?", options=["Yes", "No"])
            st.session_state["pizza_response"] = pizza_response

        elif pages.current == 1:
            st.write("How do you feel about ice cream?")
            ice_cream_response = st.select_slider(
                "Ice Cream?",
                options=["Love it!", "It's alright", "Not a fan"]
            )
            st.session_state["ice_cream_response"] = ice_cream_response

        elif pages.current == 2:
            st.write("How do you feel about numbers?")
            component_value = my_component(name = "Mai", key = "Ahoi")
            st.session_state["component_response"] = component_value

# Display the collected responses
responses = {
    "pizza_response": st.session_state.get("pizza_response"),
    "ice_cream_response": st.session_state.get("ice_cream_response"),
    "component_response": st.session_state.get("component_response")
}
st.write("Collected Responses:")
st.json(responses)