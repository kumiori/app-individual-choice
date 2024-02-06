import streamlit as st
import hashlib
from pages.test_1d import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from streamlit_extras.streaming_write import write as streamwrite 
import time
import string


# Initialize read_texts set in session state if not present
if 'read_texts' not in st.session_state:
    st.session_state.read_texts = set()

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def _stream_once(text, damage):
    text_hash = hash_text(text)


    # Define sleep lengths for different punctuation symbols
    sleep_lengths = {'.': 1., ',': 0.3, '!': 1.7, '?': 1.5, ';': 0.4, ':': 0.4}
    sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}
    # st.json(sleep_lengths)

    # st.write(sleep_lengths.values() * (1+damage))

    # Check if the text has already been read
    if text_hash not in st.session_state.read_texts:
        # st.write(text)
    
        for i, word in enumerate(text.split()):
            # Check if the last character is a punctuation symbol
            last_char = word[-1] if word[-1] in string.punctuation else None

            # Yield the word with appropriate sleep length
            if last_char == '.' or last_char == '?' or last_char == '^':
                yield word + " \n "
            else:
                yield word + " "
            
            if last_char and last_char in sleep_lengths:
                time.sleep(sleep_lengths[last_char])
            else:
                time.sleep(0.3)
            
        st.session_state.read_texts.add(text_hash)  # Marking text as read

def main():
    # once usage:
    st.write(st.session_state.read_texts)
    streamwrite(_stream_once("This is some initial text that should only be displayed once.", 0))
    st.write(st.session_state.read_texts)
    streamwrite(_stream_once("Additional text that should only be displayed once.", 0))
    st.write(st.session_state.read_texts)
    st.text_input("Text Input")


if __name__ == "__main__":
    main()