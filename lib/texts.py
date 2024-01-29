import streamlit as st
import time
from streamlit_extras.streaming_write import write as streamwrite 
import random
import string

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
 