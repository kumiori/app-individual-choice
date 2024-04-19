import streamlit as st
import numpy as np
import plotly.express as px
import time
import matplotlib.pyplot as plt

def generate_random_matrix(N):
    return np.random.rand(N, N)

def plot_random_matrix(matrix, column):
    fig = px.imshow(matrix, color_continuous_scale='gray')
    fig.update_layout(coloraxis_showscale=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
    fig.update_traces(hovertemplate='trust: %{z}')
    column.plotly_chart(fig)

def plot_random_matrix(matrix, ax):
    ax.imshow(matrix, cmap='gray')
    ax.axis('off')
    
def plot_random_matrix(matrix):
    plt.rcParams.update({
        "figure.facecolor":  (1.0, 0.0, 0.0, 0.9),  # red   with alpha = 30%
        "axes.facecolor":    (1.0, 0.0, 0.0, 0.1),  # green with alpha = 50%
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

def main():
    st.title("Random Matrix Display")

    # User input for matrix size
    N = st.slider("Select matrix size:", min_value=2, max_value=10, step=1)

    # User input for refresh interval
    refresh_interval = st.slider("Select refresh interval (seconds):", min_value=1, max_value=10, step=1)

    col1, col2 = st.columns([1, 1])

    # Generate random matrix
    random_matrix = generate_random_matrix(N)

    # Plot random matrix
    fig = plot_random_matrix(random_matrix)
    col1.pyplot(fig)
    col2.pyplot(fig)

    # Refresh and reshuffle matrix every given interval

if __name__ == "__main__":
    main()
