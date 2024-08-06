import streamlit as st
import numpy as np
import streamlit_survey as ss
from lib.survey import CustomStreamlitSurvey
from lib.io import (
    create_button, create_checkbox, create_dichotomy, create_equaliser, create_equaliser,
    create_globe, create_next, create_qualitative, create_textinput,
    create_yesno, create_yesno_row, fetch_and_display_data, conn
)
from lib.texts import stream_text
import os
import random

# from pages.test_alignment import get_next_image


@st.dialog('Cast your preferences')
def _submit():
    st.write('Thanks, expand below to see your data')    
    st.json(survey.data, expanded=False)
    # st.rerun()

# =============================================================================
# Image classification

# Initialize session state variables
if "removed_images" not in st.session_state:
    st.session_state["removed_images"] = []

if "current_index" not in st.session_state:
    st.session_state["current_index"] = []

if "choices" not in st.session_state:
    st.session_state["choices"] = {}

image_dir = "images/cards/clear"

# Get a list of all files in the directory
image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
# Filter out non-image files (if needed)
image_files = [file for file in image_files if file.endswith((".png", ".jpg", ".jpeg"))]
# Construct the URLs for the images
image_urls = [f"{image_dir}/{file}" for file in image_files][0:3]

# Shuffle the list of image URLs
# random.shuffle(image_urls)
# Initialize current image index
current_index = 0
displayed_image_url = None

def handle_button_click(image_index, choice):
    st.toast(f"Idea {image_index} classified as {choice}")
    st.session_state["removed_images"].append(image_index)
    st.session_state["choices"][image_index] = choice

def get_next_image(image_urls):
    remaining_images = [img for idx, img in enumerate(image_urls) if idx not in st.session_state["removed_images"]]
    if remaining_images:
        idx = image_urls.index(remaining_images[0])
        return remaining_images[0], idx
    else:
        return None, None

def display_images_in_grid(image_urls):
    # Create an expander
    with st.expander("Image Gallery"):
        # Number of columns in the grid
        cols = st.columns(3)  # Adjust the number of columns as needed

        # Iterate through image URLs and display them in the grid
        for index, url in enumerate(image_urls):
            # Determine the column to place the image
            col = cols[index % len(cols)]
            # Display the image with caption
            col.image(url, caption=f"Image {index}", use_column_width=True)
# =============================================================================

# survey = ss.StreamlitSurvey()
survey = CustomStreamlitSurvey('Question map')

with st.expander("Questions, expanded", expanded=True):
    pages_total = 10
    pages = survey.pages(pages_total, 
            # on_submit=lambda: st.success("Thank you!")
            on_submit=lambda: _submit
            )

    st.markdown("### Welcome to the Question Map")
    st.progress(float((pages.current + 1) / pages_total))
    with pages:
        if pages.current == 0:
            st.write("Are you happy to dine?")

            dine_together = survey.radio(
                "dine_together", options=["Neither Yes nor No", "Yes", "No"], index=0,
                label_visibility="collapsed", horizontal=True
            )
        elif pages.current == 1:
            st.write('Share something about your preferences tonight...')
            experience = create_dichotomy(key = "steering", kwargs={'survey': survey,
                                            'label': 'resonance', 
                                            'question': 'White, go forward; black, go back.',
                                            'gradientWidth': 50,
                                            'height': 300,
                                            'inverse_choice': lambda x: '',
                                            'callback': lambda x: st.write(x),}
                            )
        elif pages.current == 2:
            st.markdown("### Can we align?")
            col1, col2, col3 = st.columns([1, 1, 1])
            wrapper = col2.empty()
            current_image_url, current_index = get_next_image(image_urls)

            if current_image_url is None:
                wrapper.write("No more images to display.")
            else:
                st.session_state["current_index"] = current_index
                alignment = create_dichotomy(key = "alignment", kwargs={'survey': survey,
                                            'label': 'resonance', 
                                            'question': 'Like it or not, 🤔 hit White or Black, if resonates - or not.',
                                            'gradientWidth': 10,
                                            'height': 100,
                                            'inverse_choice': lambda x: '',
                                            'callback': handle_button_click,
                                            'args': (current_index,)}
                            )
                wrapper.image(current_image_url, width=300, caption=f"Idea {current_index}")

            st.write(image_urls)
            st.write(f'removed {st.session_state["removed_images"]}')
            st.write(f'choices {st.session_state["choices"]}')
        elif pages.current == 3:
            st.markdown("### Can we mix?")
            equaliser_data = [
                ("Sensual Exploration", ""),
                ("Emotional Connection", ""),
                ("Intellectual Stimulation", ""),
                ("Spiritual Connection", ""),
                ("Power Dynamics", ""),
                ("Personal Growth", ""),
            ]

            # st.write(survey)
            st.markdown("Let's think _energetically..._")
            st.markdown("### Using an _energy_ mixer, where energy _comes from_?")
            create_equaliser(key = "equaliser", kwargs={"survey": survey, "data": equaliser_data})
        elif pages.current == 4:
            st.markdown("## How are you feeling today?")
            st.write('hi / low : positive \ negative')
        elif pages.current == 5:
            st.markdown('## $\mathcal{Q}$uestion:')
            stream_text('### context: EID, suggestion of ..., upsert results ina plenary session')
            stream_text('### solution: R.~P., panelist, title and background')
            stream_text('### ask: good idea or not?')
            experience = create_dichotomy(key = "plenary", kwargs={'survey': survey,
                                            'label': 'plenary', 
                                            'question': 'White, go forward; black, go back.',
                                            'gradientWidth': 25,
                                            'height': 300,
                                            'inverse_choice': lambda x: '',
                                            'callback': lambda x: st.write(x),}
                            )
display_images_in_grid(image_urls)
