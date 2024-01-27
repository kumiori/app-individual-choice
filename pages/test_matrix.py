import streamlit as st
import numpy as np
import time
import string
import emoji
import plotly.graph_objs as go

from pages.test_steering import frobenius_norm

def plot_norm_values(norm_values):
    fig = go.Figure(data=go.Scatter(x=np.arange(len(norm_values)), y=norm_values, mode='lines+markers'))
    fig.update_layout(title='Everything starts from zero...',
        xaxis_title='Real Time flows',
        yaxis_title='Energy')
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 0
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, theme="streamlit")


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

# Streamlit app
def main():
    st.title("Data is Encoded in the Matrix")


    # Set the size of the matrix (e.g., 5x5)
    col1, col2, col3 = st.columns(3)
    with col1:
        """### `We have accepted explosion of information, are you willing to accept explosion of undertsanding?`"""

    with col2:
        # matrix_size = st.slider("Select Matrix Size", min_value=1, max_value=10, value=5)
        matrix_size = 5
        matrix_placeholder = st.empty()
    with col3:
        st.button("Reload")
        st.button("Continue")
        st.button("Exit")
        st.button("Play")
    
    chart_plot = st.empty()
        
    # Set the update frequency
    update_frequency = 500  # in milliseconds

    # Create a placeholder to display the matrix

    # Generate and display the initial matrix
    # matrix = generate_random_matrix(matrix_size)
    # display_matrix(matrix)

    _scale = 500000
    
    # Update the matrix every 500 milliseconds
    norm_values = []
    while True:
        time.sleep(update_frequency / 1000.0)  # Convert to seconds
        matrix = generate_random_matrix(matrix_size)
        encoded_matrix = encode_matrix(matrix)
        norm_value = frobenius_norm(encoded_matrix)/_scale
        norm_values.append(norm_value)
        
        # with col1:
        #     st.write(norm_value)
        
        with col2:
            matrix_placeholder.empty()
            with matrix_placeholder:
                display_matrix(matrix)
        # matrix_placeholder.table(matrix)

        with chart_plot:
            # st.line_chart(norm_values)
            plot_norm_values(norm_values)

# Run the app
if __name__ == "__main__":
    main()
