import streamlit as st

from streamlit_extras.stylable_container import stylable_container 
from streamlit_extras.streaming_write import write 
from streamlit_extras.let_it_rain import rain 
from streamlit_extras.keyboard_url import keyboard_to_url 
from streamlit_image_coordinates import streamlit_image_coordinates

def example():
    with stylable_container(
        key="green_button",
        css_styles="""
            button {
                background-color: green;
                color: white;
                border-radius: 20px;
            }
            """,
    ):
        st.button("Green button")

    st.button("Normal button")

    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 13px solid rgba(49, 51, 63, 0.9);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
        st.markdown("This is a container with a border.")


example()




value = streamlit_image_coordinates("https://placekitten.com/200/200")

st.write(value)


# def example():
#     # Main function
#     keyboard_to_url(key="S", url="https://www.github.com/streamlit/streamlit")

#     load_key_css()
#     st.write(
#         f"""Now hit {key("S", False)} on your keyboard...!""",
#         unsafe_allow_html=True,
#     )


def example():
    rain(
        emoji="🎈",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )
    
example()
    