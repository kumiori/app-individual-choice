import streamlit as st

# nested buttons and session state


# init state

if "button_pressed" not in st.session_state:
    st.session_state["button_pressed"] = False
    # st.write(f"{st.session_state['button_pressed']}")
    
    
def callback():
    st.session_state["button_pressed"] = True
    st.write("Button pressed!")


st.slider(label='Slide me')
st.button(label='Press me', on_click=callback)
st.write(f"button_pressed: {st.session_state['button_pressed']}")

st.write(st.session_state)
