import streamlit as st
import lib.survey as sv
import streamlit_shadcn_ui as ui
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
from local_components import card_container

survey = sv.CustomStreamlitSurvey()

# Page configuration
st.set_page_config(
    page_title="Quantitative Exchange Platform",
    page_icon="📊",
    layout="centered",
)

# Title

cols = st.columns(3)
with cols[1]:

    st.markdown("# • Portal •")

# Subtitle
st.subheader("One Way to Communicate and Exchange")

# Introduction
st.markdown(
    """
    The system is not designed nor is trained, but achieves a _systematic_ target.
    
    Click to execute. 
    
    Here • and • Now.
    
    ** 🚀 **
    """
)

switch_value = switch(default_checked=True, label="Toggle Switch", key="switch1")

ui.badges(badge_list=[("applications", "default"), ("theory", "destructive")], class_name="flex gap-2", key="main_badges")

location = survey.text_input("I connect my location", help="Our location will appear shortly...", value=st.session_state.get('location', 'Venegono Superiore, Varese, Italy'))

cols = st.columns(3)

with cols[1]:
    button = survey.button("`------ Here • Now -------`", key="submit_location")
    
    ui.card(title="Inside", content="+1", description="+∞ from last checkpoint", key="card").render()



def generate_sales_data():
    import pandas as pd
    import numpy as np
    
    np.random.seed(0)  # For reproducible results
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sales = np.random.randint(0, 10, size=len(months))
    return pd.DataFrame({'Month': months, 'Energy': sales})

# with card_container(key="chart1"):
#     st.vega_lite_chart(generate_sales_data(), {
#         'mark': {'type': 'bar', 'tooltip': True, 'fill': 'rgb(173, 250, 29)', 'cornerRadiusEnd': 4 },
#         'encoding': {
#             'x': {'field': 'Month', 'type': 'ordinal'},
#             'y': {'field': 'Energy', 'type': 'quantitative', 'axis': {'grid': False}},
#         },
#     }, use_container_width=True)

# Switch Component
st.write("Switch is On:", switch_value)
