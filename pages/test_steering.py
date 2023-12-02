import streamlit as st
import time
import random
import emoji
import string
import numpy as np
# import matplotlib.pyplot as plt

markdown_text = """
# Description

This test conducts a dynamic matrix evolution experiment, starting with a random matrix of characters. The user can introduce fixed characters into the matrix, gradually transforming it over a specified number of iterations. The Frobenius norm, a measure of matrix magnitude, is calculated at each step. Additionally, the temporal differences between consecutive matrices are computed, and their Frobenius norm is displayed as an updating metric. Users can control the number of iterations and select between alphanumeric and emoji characters for evolution. The evolving matrix and its temporal differences are visually presented in a table, with the Frobenius norms tracked through interactive metrics. This experiment provides insights into the changing characteristics of the matrix and how temporal differences contribute to its evolving energy.
"""
_text = """
This example shows how to converge in decision making, starting from the favourable conditions: random initial data.
"""
if 'delta_norm_value' not in st.session_state:
    st.session_state = {'delta_norm_value': 0.0}
    
def update_session_state(delta_norm_value):
    st.session_state['delta_norm_value'] = delta_norm_value

def encode_matrix(matrix):
    return [[ord(char) for char in row] for row in matrix]

def frobenius_norm(matrix):
    return np.linalg.norm(matrix)

def one_norm(matrix):
    return np.linalg.norm(matrix, 1)

def infinity_norm(matrix):
    return np.linalg.norm(matrix, np.inf)

def two_norm(matrix):
    return np.linalg.norm(matrix, 2)

def schatten_norm(matrix, p):
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return np.linalg.norm(singular_values, p)

def nuclear_norm(matrix):
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return np.sum(singular_values)

def generate_random_matrix(size):
    # return [[random.choice(emoji.emojize(":smiley:")) for _ in range(size)] for _ in range(size)]
    return [[random.choice(string.ascii_letters) for _ in range(size)] for _ in range(size)]

def introduce_fixed_characters(matrix, fixed_chars):
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if random.random() < 0.1:
                matrix[i][j] = random.choice(fixed_chars)
    return matrix

def main():
    st.title("Energy Matrix Display aka")
    st.markdown("## 'The Matrix' or,")
    st.markdown("### Convergence of random processes")
    st.markdown("#### (or, how to make a decision)")
    st.markdown(_text)
    _players = st.slider("Select number of players (sqrt matrix size):", min_value=2, max_value=1000, value=300)
    size = int(_players**(1/2))
    # Create columns for a better visual layout
    col1, col2 = st.columns(2)

    with col1:
        choice = st.radio("Select fixed characters type:", ["Emojis", "Alphanumeric"])
        slowness = float(st.text_input("Slowness:", value='0.1'))

        if choice == "Emojis":
            fixed_emojis = st.text_input("Enter fixed emojis (e.g., 😀🌟🎉):", value='😀🌟🎉')
            fixed_characters = list(emoji.emojize(char) for char in fixed_emojis)
        else:
            fixed_characters = st.text_input("Enter fixed characters (e.g., ABC):", value=".")
            fixed_characters = ''.join(sorted(set(fixed_characters)))

        iterations = st.number_input("Number of iterations:", min_value=1, value=10)

        # Create an empty placeholder for the matrix table
        _col1, _col2 = st.columns(2)
        with _col1:
            start_evo = st.button("Start Evolution")
        with _col2:
            reset_evo = st.button("Reset Evolution", key="reset")

        chart_plot = st.empty()

        # Button to start the simulation
        # if st.button("Start Simulation"):

    with col2:
        # Display the st.metric element in the second column
        metric_value = len(fixed_characters) if fixed_characters else 0
        st.write(st.session_state.get('delta_norm_value'))
        st.markdown(f" ### Fixed Ideas: {metric_value}")
        st.markdown(markdown_text)
    norm_values = []
    normalised_norm_values = {
        'frobenius_norm': 0.0,
        'one_norm': 0.0,
        'infinity_norm': 0.0,
        'two_norm': 0.0,
        'schatten_norm': 0.0,
        'nuclear_norm': 0.0,
        '-2_norm': 0.0,
    }
    norm_functions = {
        'frobenius_norm': np.linalg.norm,
        'one_norm': lambda x: np.linalg.norm(x, ord=1),
        'infinity_norm': lambda x: np.linalg.norm(x, ord=np.inf),
        'two_norm': lambda x: np.linalg.norm(x, ord=2),
        'neginf_norm': lambda x: np.linalg.norm(x, ord=-np.inf),
        'nuclear_norm': lambda x: np.linalg.norm(x, ord='nuc'),
        '-2_norm': lambda x: np.linalg.norm(x, ord=-2),
    }    
    matrix_table_placeholder = st.empty()
    encoded_matrix_table_placeholder = st.empty()
    norm = st.empty()


    matrix = generate_random_matrix(size)
    matrix_table_placeholder.table(matrix)
    
    
    if start_evo:
        # matrix = generate_random_matrix(size)

        # Display the initial matrix in the first column
        matrix_table_placeholder.table(matrix)
        encoded_matrix_table_placeholder.table(matrix)

        # Gradually introduce fixed characters
        norm_old = 0
        _iterations = range(iterations)
        for iter in _iterations:
            time.sleep(slowness)
            matrix = introduce_fixed_characters(matrix, fixed_characters)
            encoded_matrix = encode_matrix(matrix)
            _scale = 500000
            norm_value = frobenius_norm(encoded_matrix)/_scale
            _delta = norm_value - norm_old
            
            with norm:
                
                st.markdown(f'Pseudo-energy: {normalised_norm_values["frobenius_norm"]}')
                st.metric("Pseudo-energy (Frobenius norm)", normalised_norm_values['frobenius_norm'],
                          delta=float(_delta))

            # Update the matrix table in the first column
            matrix_table_placeholder.table(matrix)
            encoded_matrix_table_placeholder.table(encoded_matrix)
            norm_old = norm_value

            if iter > 0:
                # Compute and display Frobenius norm of temporal differences
                # st.markdown(encoded_matrix)
                delta_matrix = np.array(encoded_matrix) - np.array(encode_matrix(prev_matrix))
                delta_norm_value = frobenius_norm(delta_matrix)
                # st.markdown(delta_matrix)
                update_session_state(delta_norm_value)

                # st.metric("Temporal Diff Norm", delta_norm_value, delta=0)

            prev_matrix = matrix.copy()
            _norm_values = {norm_name: norm_func(encode_matrix(matrix)) for norm_name, norm_func in norm_functions.items()}
            min_val = min(_norm_values.values())
            max_val = max(_norm_values.values())

            normalised_norm_values = {norm_name: (val - min_val) / (max_val - min_val) for norm_name, val in _norm_values.items()}

            # Plot normalized norms
            # st.line_chart(normalised_norm_values)
            norm_values.append(normalised_norm_values['frobenius_norm'])
            
            # Create a dictionary with data for the line chart
            # chart_data = {'Frobenius Norm': norm_values}

                # Create a line chart
            with chart_plot:
                st.line_chart(norm_values)
        st.write(norm_values)
if __name__ == "__main__":
    main()