import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px
from matplotlib.patches import Polygon


def generate_random_matrix(N, a=0, b=1):
    """
    Generate a random matrix of size NxN with values between a and b.

    Parameters:
        N (int): Size of the matrix (number of rows and columns).
        a (float): Lower bound of the random values.
        b (float): Upper bound of the random values.

    Returns:
        numpy.ndarray: Random matrix of size NxN.
    """
    return np.random.uniform(a, b, (N, N))

def plot_random_matrix(matrix):
    fig, ax = plt.subplots()
    ax.scatter(*np.meshgrid(range(matrix.shape[0]), range(matrix.shape[1])),
               c=matrix, cmap='gray', edgecolors='none', s=100)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Random Matrix")
    st.pyplot(fig)

def plot_random_matrix(matrix, placeholder):
    with placeholder:
        fig = px.imshow(matrix, color_continuous_scale='gray')
        # fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(coloraxis_showscale=False, 
                          xaxis_showticklabels=False, 
                          yaxis_showticklabels=False)
        fig.update_layout(coloraxis_showscale=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
        fig.update_traces(hovertemplate='Trust: %{z:.2f}')

        st.plotly_chart(fig)

    
def plot_random_matrix_matplotlib(matrix):
    plt.rcParams.update({
        "figure.facecolor":  (1.0, 0.0, 0.0, 0.9),  # red   with alpha = 30%
        "axes.facecolor":    (1.0, 0.0, 0.0, 0.4),  # green with alpha = 50%
        # "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
    })
    fig, ax = plt.subplots()
    ax.scatter(*np.meshgrid(range(matrix.shape[0]), range(matrix.shape[1])),
               c=matrix, cmap='gray', edgecolors='none', s=500)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.patch.set_facecolor('red')

    # ax.set_title("Random Matrix")
    return fig

def plot_random_matrix_matplotlib2(matrix):
    fig, ax = plt.subplots()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = plt.cm.gray(matrix[i, j])  # Convert matrix value to grayscale color
            polygon = Polygon([[i, j], [i+1, j], [i+1, j+1], [i, j+1]], closed=True, facecolor=color, edgecolor='none')
            ax.add_patch(polygon)
    ax.set_xlim(0, matrix.shape[0])
    ax.set_ylim(0, matrix.shape[1])
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.set_title("Random Matrix")
    return fig

def generate_sparse_matrix(N, M):
    # Create an empty matrix filled with zeros
    matrix = np.zeros((N, N))
    
    # Generate random row and column indices for non-zero values
    row_indices = np.random.choice(range(N), M, replace=True)
    col_indices = np.random.choice(range(N), M, replace=True)
    
    # Assign random non-zero values to the specified indices
    for i in range(M):
        matrix[row_indices[i], col_indices[i]] = np.random.rand()
    
    return matrix

def main():
    st.title("Welcome to Game Trust")
    st.write("Game Trust is an experimental game designed to explore trust dynamics between investors and financial institutions.")
    """
We explore questions of trust, trustworthiness, and cooperation in social interactions. It's particularly interesting because it involves sequential decision-making, where one player's decision influences the other's subsequent decision. 

Trusting behavior often depends on factors such as perceived trustworthiness of the partner, perceived risks and rewards, and social norms regarding cooperation and reciprocity. This game allows us, researchers and players, to study how these factors influence decision-making and how trust and cooperation can emerge or break down in different situations.    
    """
    col1, col2 = st.columns(2)
    
    with col1:
        placeholder = col1.empty()
    
    placeholder2 = col2.empty()

    # User input for refresh interval
    refresh_interval = st.slider("Select refresh interval (seconds):", min_value=1, max_value=10, step=1)

        # User input for matrix size
    N = st.slider("Select number of players (or its root):", value=10, min_value=2, max_value=100, step=3)
        # User input for matrix size
    M = st.slider("Select number of nonzero in the sparse:", min_value=0, max_value=N, step=1)

    st.write("Players: ", N+1)
    
    while True:
        # Generate random matrix
        random_matrix = generate_random_matrix(N, a=.3)
        sparse_matrix = generate_sparse_matrix(N, M)
        
        if N == 2:
            random_matrix[1, 1] = 1.
        
        # Plot random matrix
        # plot_random_matrix(random_matrix, placeholder)
        fig = plot_random_matrix_matplotlib(random_matrix)
        fig = plot_random_matrix_matplotlib2(random_matrix)
        fig2 = plot_random_matrix_matplotlib2(sparse_matrix)

        placeholder.pyplot(fig)
        placeholder2.pyplot(fig2)
            
        # Refresh and reshuffle matrix every given interval
        time.sleep(refresh_interval)

        placeholder.empty()
        for _fig in [fig, fig2]:
            plt.close(_fig)  # Close the figure to release memory

    
    # technology outsmarting the humans
    # take a lot of people? how many people are there?
    
    st.header("Instructions:")
    st.write("In this game, you will act as an investor deciding how much trust to invest in the bank HSBC.")
    st.write("Your task is to choose a level of trust, represented by a value between 0 and 1.")
    st.write("You will also have an initial capital to allocate to the bank.")
    st.write("Based on your decision and the bank's response, both players will receive certain payoffs.")
    st.write("Remember, your level of trust can change over time.")
    
    st.header("Gameplay:")
    st.write("1. Choose a level of trust (α) between 0 and 1 using the slider.")
    st.write("2. Allocate an initial capital (C) to the bank.")
    st.write("3. The bank will decide whether to 'move' or 'betray'.")
    st.write("4. Based on the bank's decision and your trust level, both players will receive payoffs.")
    st.write("5. You can adjust your trust level at any time.")
    
    st.header("Trust Level:")
    trust_level = st.slider("Select your trust level:", min_value=0.0, max_value=1.0, step=0.01)
    st.write("Your current trust level: ", trust_level)
    
    st.header("Capital Allocation:")
    capital = st.number_input("Enter your initial capital:", min_value=0, step=1000)
    st.write("Your initial capital: ", capital)
    
    st.header("Bank's Decision:")
    # Implement bank's decision logic and display here
    
    st.header("Outcome:")
    # Display payoffs for both players based on the bank's decision and trust level
    
    
    st.header("Random Matrix:")
    matrix_placeholder = st.empty()

    # while True:
    #     # Generate and display random matrix
    #     random_matrix = generate_random_matrix(N)
    #     matrix_placeholder.dataframe(random_matrix)

    #     # Refresh and reshuffle matrix every given interval
    #     time.sleep(refresh_interval)

    # while True:
    #     # Generate random matrix
    #     random_matrix = generate_random_matrix(N)

    #     # Plot random matrix
    #     plot_random_matrix(random_matrix)

    #     # Refresh and reshuffle matrix every given interval
    #     st.text("Refreshing matrix in {} seconds...".format(refresh_interval))
    #     matrix_placeholder.empty()
        

if __name__ == "__main__":
    main()
