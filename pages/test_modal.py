import streamlit as st
from streamlit_modal import Modal

import streamlit.components.v1 as components


if "checked" not in st.session_state:
    st.session_state['checked'] = ''

value = False
modal = Modal(
    "Disclaimerrrrr", 
    key="demo-modal",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)


open_modal = st.button("Open Consent")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        """I experienced how analysis can be the fastest way to fuck\n
            with the mind."""
                 
        # st.write()

        st.markdown("## Some say this, some say that.")

        st.write("Can we show how to approximate division by zero? If not, it can be enforced: bottom up.")
        value = st.checkbox("Checked for consent", value=st.session_state['checked'],
                            on_change=lambda x: st.session_state.update({'checked': x}),
                            args=(True,))
        st.write(f"Checkbox checked: {value}")


        
st.write('value', st.session_state['checked'])
if st.session_state['checked']:
    st.write("Consent is granted.")