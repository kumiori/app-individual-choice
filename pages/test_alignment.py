import streamlit as st
import os
import random
from streamlit_extras.add_vertical_space import add_vertical_space 
from lib.survey import CustomStreamlitSurvey
from lib.io import create_dichotomy

# Initialize session state variables
if "removed_images" not in st.session_state:
    st.session_state["removed_images"] = []

if "current_index" not in st.session_state:
    st.session_state["current_index"] = []

if "choices" not in st.session_state:
    st.session_state["choices"] = {}

# Path to the directory containing the images
image_dir = "images/cards/clear"
# image_dir = "images/cards/contrast"

# Get a list of all files in the directory
image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
# Filter out non-image files (if needed)
image_files = [file for file in image_files if file.endswith((".png", ".jpg", ".jpeg"))]

# Construct the URLs for the images
image_urls = [f"{image_dir}/{file}" for file in image_files]

# Shuffle the list of image URLs
random.shuffle(image_urls)

# Initialize current image index
current_index = 0
st.markdown(
    """
    <style>
    .st-emotion-cache-13k62yr {
        background-color: #000 !important;
    }
   </style>
    """,
    unsafe_allow_html=True
)

def get_next_image():
    # st.write(st.session_state["removed_images"])
    remaining_images = [img for idx, img in enumerate(image_urls) if idx not in st.session_state["removed_images"]]
    random.shuffle(remaining_images)
    if remaining_images:
        idx = image_urls.index(remaining_images[0])
        return remaining_images[0], idx
    else:
        return None, None

# Function to handle button clicks
def handle_button_click(image_index, choice):
    st.session_state["removed_images"].append(image_index)
    st.session_state["choices"].update({st.session_state["current_index"][-2]: choice})

# Function to handle button clicks
def on_button_click(choice):
    global current_index, image_urls
    if choice == "Left":
        st.write("You chose Left")
    elif choice == "Right":
        st.write("You chose Right")
    
    # Remove the current image from the list
    del image_urls[current_index]
    
    # Shuffle the list
    random.shuffle(image_urls)

    # st.write(f"Images left: {len(image_urls)}")
    # st.write(f"Current index: {current_index}")
        
    # Update the current index
    current_index = 0 if current_index >= len(image_urls) else current_index
    

st.title("Do you resonate?")
# Display the current image
col1, col2, col3 = st.columns([1, 5, 1])
survey = CustomStreamlitSurvey()

next_image_url = None
wrapper = st.empty()

if next_image_url is None:
    wrapper.write("No more images to display.")
    # st.stop()
# 
# with col1:
#     add_vertical_space(13)
#     st.button("Yes",
#         key = f"yes_button_{current_index}",
#         on_click=handle_button_click,
#         args=(image_urls.index(next_image_url),))
# 
# with col3:
#     add_vertical_space(13)
#     st.button("No",
#         key = f"no_button_{current_index}",
#         on_click=handle_button_click,
#         args=(image_urls.index(next_image_url),))
# 
# col2.image(next_image_url,
#             width=500,
#             caption=f"Idea {current_index + 1}")
# 

st.divider()



def create_dichotomy(key, kwargs = {}):
    survey = kwargs.get('survey')
    label = kwargs.get('label', 'Confidence')
    name = kwargs.get('name', 'there')
    index = kwargs.get('index', -1)
    question = kwargs.get('question', 'Dychotomies, including time...')
    question += f' {index}'
    messages = kwargs.get('messages', ["🖤", "Meh. Balloons?", "... in between ..."])
    inverse_choice = kwargs.get('inverse_choice', lambda x: x)
    _response = kwargs.get('response', '## You can always change your mind. Now, to the next step.')
    col1, col2, col3 = st.columns([3, .1, 1])
    callable = kwargs.get('callback')
    
    with col1:    
        response = survey.dichotomy(name=name, 
                                label=label,
                                question=question,
                                gradientWidth = kwargs.get('gradientWidth', 30), 
                                key=key)
    # with col3:
    #     if response:
    #         st.markdown('\n')            
    #         st.markdown(f'## Your choice:', unsafe_allow_html=True)
    #         st.markdown(f'## {inverse_choice(float(response))}')
    #         st.markdown(f'{float(response)}', unsafe_allow_html=True)
    #         if float(response) < 0.1:
    #             st.success(messages[0])
    #         if float(response) > 0.9:
    #             st.info(messages[1])
    #         elif 0.1 < float(response) < 0.9:
    #             st.success(messages[2])
    #     else:
    #         st.markdown(f'## Take your time:', unsafe_allow_html=True)
    
    # st.write(*kwargs.get('args', []), response)
    
    if response:
        st.markdown(_response)
        
        if callable:
            callable(*kwargs.get('args', []), response)
            
    return response, index

next_image_url, current_index = get_next_image()

st.session_state["current_index"].append(current_index)

if next_image_url:
    response = create_dichotomy(key = "steering", kwargs={'survey': survey,
                                           'label': 'resonance', 
                                           'question': 'Do you resonate with',
                                           'gradientWidth': 1,
                                           'inverse_choice': lambda x: '',
                                           'index': current_index,
                                            'callback': handle_button_click,
                                            'args': (current_index,)}
                            )

    wrapper.image(next_image_url,
                width=500,
                caption=f"Idea {current_index}")

    st.write(st.session_state["removed_images"])
    st.write(f"response: {response}, current_index: {current_index}, last_image: {st.session_state['current_index']}")
    st.write(st.session_state["choices"])
    st.write(st.session_state["current_index"])