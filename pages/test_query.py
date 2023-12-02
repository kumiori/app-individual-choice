import streamlit as st
import json
import streamlit_survey as ss

# Define a StreamlitSurvey class (simplified for this example)
# class StreamlitSurvey:
#     def __init__(self, name):
#         self.name = name

#     def pages(self, num_pages):
#         self.num_pages = num_pages
#         self.current = 0

# # Initialize the StreamlitSurvey
# survey = StreamlitSurvey("Survey")

st.title("Simple Survey")


with st.expander("Some questions:", expanded=True):
    survey = ss.StreamlitSurvey("Home")
    pages = survey.pages(2, on_submit=lambda: 
        st.success("Your responses have been recorded. Thank you!"))

    with pages:
        if pages.current == 0:
            st.write("Do you like pizza?")
            pizza_response = st.radio("Pizza?", options=["Yes", "No"])
            st.experimental_set_query_params(pizza_response=pizza_response)

        elif pages.current == 1:
            st.write("How do you feel about ice cream?")
            ice_cream_response = st.select_slider(
                "Ice Cream?",
                options=["Love it!", "It's alright", "Not a fan"]
            )
            st.experimental_set_query_params(ice_cream_response=ice_cream_response)

# Display the collected responses
responses = {
    "pizza_response": st.experimental_get_query_params().get("pizza_response"),
    "ice_cream_response": st.experimental_get_query_params().get("ice_cream_response")
}
st.write("Collected Responses:")
st.write(json.dumps(responses, indent=2))