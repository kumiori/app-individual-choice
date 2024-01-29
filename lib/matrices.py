
import streamlit as st
import numpy as np
import time
import string
import emoji
import plotly.graph_objs as go

def encode_matrix(matrix):
    encoded_matrix = []
    for row in matrix:
        encoded_row = []
        for char in row:
            # Check if the character is an emoji
            if len(char) > 1:
                # Use the Unicode code points of emojis directly
                encoded_row.extend([ord(emoji_char) for emoji_char in char])
            else:
                # Use the Unicode code point of regular characters
                encoded_row.append(ord(char))
        encoded_matrix.append(encoded_row)

    # Convert the matrix to a NumPy array with a consistent data type (int)

    encoded_matrix = np.array(encoded_matrix, dtype=int)
    return encoded_matrix

# Function to generate a random NxN matrix of characters
def generate_random_matrix(size):
    characters = list(string.ascii_letters + string.digits + string.punctuation)
    emojis = [emoji.emojize(":cold_face:"),
        emoji.emojize("🗯"),
        emoji.emojize(":skull:"),
        emoji.emojize(":star:"),
        emoji.emojize(":sparkles:"),
        emoji.emojize(":face_with_peeking_eye:"),
        emoji.emojize(":rocket:")]

    all_characters = characters + emojis
    # all_characters = emojis
    # all_characters = characters

    return np.random.choice(all_characters, size=(size, size))
    # # return matrix
    return [[np.random.choice(characters) for _ in range(size)] for _ in range(size)]


# Function to display the matrix in a fixed-size container
def display_matrix(matrix):
    num_cols = len(matrix)

    # Create st.columns to display each matrix element in a column
    cols = st.columns(num_cols)

    for i in range(num_cols):
        for j in range(num_cols):
            cols[i].write(matrix[i][j])
