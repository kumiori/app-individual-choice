import streamlit as st
import requests
from streamlit_extras.let_it_rain import rain 

def main():
    st.title('FormSubmit.co Integration Example')

    # Use st.form to create a form in Streamlit
    with st.form(key='formsubmit_form'):
        st.header('Submit your information')
        name = st.text_input('Name', max_chars=50)
        email = st.text_input('Email', max_chars=50, type='default')

        submit_button = st.form_submit_button('Submit')

        if submit_button:
            # Check if name and email are provided
            if name and email:
                # Prepare the data to be sent
                form_data = {
                    'name': name,
                    'email': email
                }

                # Send POST request to FormSubmit.co endpoint
                response = requests.post('https://formsubmit.co/a.leon.baldelli@gmail.com', data=form_data)

                if response.status_code == 200:
                    st.success('Form submitted successfully!')
                    rain(
                            emoji="🎈",
                            font_size=54,
                            falling_speed=5,
                            animation_length="infinite",
                        )
                else:
                    st.error(f'Failed to submit form. Status code: {response.status_code}')
            else:
                st.warning('Please enter both name and email.')

if __name__ == '__main__':
    main()