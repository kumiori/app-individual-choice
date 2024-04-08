import streamlit as st
import time
from streamlit_extras.streaming_write import write as streamwrite 
import random
import string
import hashlib

# Initialize read_texts set in session state if not present
st.write(st.session_state)

if 'read_texts' not in st.session_state:
    st.session_state['read_texts'] = set()

def corrupt_string(input_str, damage_parameter):
    # Define the list of symbols
    symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~"

    # Calculate the number of characters to replace based on the damage parameter
    num_chars_to_replace = int(len(input_str) * damage_parameter)
    st.write(num_chars_to_replace)
    # Select random indices to replace
    indices_to_replace = random.sample(range(len(input_str)), num_chars_to_replace)

    # Corrupt the string
    corrupted_list = list(input_str)
    for index in indices_to_replace:
        corrupted_list[index] = random.choice(symbols)

    return ''.join(corrupted_list), num_chars_to_replace

def _stream_example(text, damage):
    # Define sleep lengths for different punctuation symbols
    sleep_lengths = {'.': 1., ',': 0.3, '!': 1.7, '?': 1.5, ';': 0.4, ':': 0.4}
    sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}
    # st.json(sleep_lengths)

    # st.write(sleep_lengths.values() * (1+damage))
    
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
    if text_hash not in st.session_state["read_texts"]:
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
            
        st.session_state["read_texts"].add(text_hash)  # Marking text as read

def create_streamed_columns(panel):
    num_panels = len(panel)
    
    for i in range(num_panels):
        width_pattern = [2, 1] if i % 2 == 0 else [1, 2]
        cols = st.columns(width_pattern)

        col_idx = 0  if i % 2 == 0 else 1
        with cols[col_idx]:
            streamwrite(_stream_once(panel[i], 0))

def match_input(input_text, translation_dict):
    if not input_text:
        return None
    
    matching_keys = [key for key, value in translation_dict.items() if value.lower() == input_text.lower()]

    if matching_keys:
        return matching_keys
    else:
        return False


def friendly_time(timestamp):
    from datetime import datetime

    human_readable_time = datetime.utcfromtimestamp(timestamp)

    hour = human_readable_time.strftime('%-I')
    minute = human_readable_time.strftime('%-M')
    _period = human_readable_time.strftime("%p")
    print(_period)
    # period = 'in the morning' if datetime.utcfromtimestamp(timestamp).strftime('%p').lower() == 'am' else 'in the afternoon'

    friendly_time = f"{minute} minutes past {hour}"

    return friendly_time