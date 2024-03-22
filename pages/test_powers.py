import streamlit as st
from streamlit.components.v1 import components as stc
from streamlit_extras.row import row
from pages.test_injection import CustomStreamlitSurvey
from streamlit_extras.mandatory_date_range import date_range_picker 
import hashlib
superpowers_dict = {
    'Time-Bending Vision': {
        'description': 'With the ability to see moments from the past, present, and future simultaneously, you navigate life with wisdom beyond your years. Embrace your time-bending vision to savor the present and make future choices with an extraordinary foresight.',
        'emoji': '🕰️'
    },
    'Quantum Resilience': {
        'description': 'Harness the power of quantum resilience, allowing you to bounce back from challenges stronger than ever. You\'re not just unbreakable; you\'re a force of nature, adapting and thriving in the face of adversity.',
        'emoji': '🌟'
    },
    'Mindful Teleportation': {
        'description': 'Imagine the world as your playground, and with mindful teleportation, you can transport your mind to any place, experiencing the wonders of diverse cultures and perspectives without leaving your chair.',
        'emoji': '🌍'
    },
    'Emotional Alchemy': {
        'description': 'Turn emotional challenges into golden opportunities with emotional alchemy. Your ability to transmute negative feelings into positive actions makes you a true emotional alchemist.',
        'emoji': '🌈'
    },
    'Tech-Intuitive Empathy': {
        'description': 'Connect with people on a profound level through your tech-intuitive empathy. Whether it\'s deciphering emojis or understanding digital vibes, your superpower lies in creating genuine connections in the digital age.',
        'emoji': '✨'
    },
    'Infinite Creativity Flow': {
        'description': 'Dive into the boundless river of creativity where ideas flow endlessly. With infinite creativity flow, you\'re a master at turning imagination into reality, making every project a masterpiece.',
        'emoji': '🎨'
    },
    'Empathic Harmony': {
        'description': 'Tune into the emotions of those around you and weave a tapestry of empathic harmony. Your ability to create unity and understanding makes you a beacon of emotional resonance.',
        'emoji': '🌟'
    },
    'Gravity-Defying Confidence': {
        'description': 'Soar through life with the weightless power of gravity-defying confidence. Your self-assuredness defies expectations, allowing you to reach new heights with each step.',
        'emoji': '💃'
    },
    'Fluent Multiverse Communication': {
        'description': 'Speak the language of the multiverse, effortlessly navigating diverse realities and perspectives. Fluent multiverse communication lets you connect with people from all walks of life, making you a bridge between worlds.',
        'emoji': '🌐'
    },
    'Harmonic Time Management': {
        'description': 'Command the symphony of time with harmonic time management. Juggling various aspects of life becomes an art form as you orchestrate priorities, creating a harmonious balance.',
        'emoji': '🎶'
    }
}

def show_powers():
    container = st.container()
    empty = st.empty()
    
    def callback(description, _container):
        # st.write(description)
        # empty.write('ad')
        _container.write(description)
        
    links_row = row(len(superpowers_dict)//2, vertical_align="center")

    with container:
        for power_name, details in superpowers_dict.items():
            emoji = details['emoji']
            description = details['description']

            # Create a button with emoji and show description on hover
            button_text = f"{emoji}"

            links_row.button(button_text, help=description, key=power_name, on_click = callback, args = (description, empty))
    
    st.write('''<style>
        [data-testid="stVerticalBlock"] [data-testid="baseButton-secondary"] p {
            font-size: 2rem;
            padding: 1rem;
        }
    </style>''', unsafe_allow_html=True)
    
    with container:
        st.write('asd')

# Example Usage:
def main():
    st.write(st.session_state)
    st.text_input('Access key', key='access key')
    survey = CustomStreamlitSurvey()
    col1, col2, col3 = st.columns(3)
    with col1:
        current_time = survey.timeinput("Is this the time?", key='time')
    with col2:
        current_date = survey.dateinput("Is this today?", key='dateasdasd')
    with col3:
        location = survey.text_input("Where are you, if not here...", help="Our location.")

    show_powers()

if __name__ == '__main__':
    main()

    st.write(
        """
        This is an example of a date range picker that *always* returns a start and
        end date, even if the user has only selected one of the dates. Until the
        user selects both dates, the app will not run.
        """
    )
    result = date_range_picker("Select a date range")
    st.write("Result:", result)