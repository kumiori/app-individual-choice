import streamlit as st
import plotly.express as px
import numpy as np

# Generate random matrix data for demonstration
matrix_size = 5
matrix_data = np.random.rand(matrix_size, matrix_size)

# Create a scatter plot with circles
fig = px.scatter(x=np.arange(matrix_size).repeat(matrix_size),
                 y=np.tile(np.arange(matrix_size), matrix_size),
                 size=matrix_data.flatten(),
                 size_max=50,
                 color=matrix_data.flatten(),
                 color_continuous_scale="Blues",
                 title="Matrix Visualization")

# Set axis labels
fig.update_layout(xaxis_title="Column Index", yaxis_title="Row Index")

# Display the Plotly figure
st.plotly_chart(fig)

# Define custom tooltip content
custom_tooltip_data = [
    [f"({i + 1}, {j + 1})" for j in range(matrix_size)] for i in range(matrix_size)
]


matrix_size = 12
matrix_data = np.random.rand(matrix_size, matrix_size)

# st.write(np.array([[100 for j in range(matrix_size)] for i in range(matrix_size) ]))
# st.write(matrix_data.flatten())
# Create a scatter plot with circles and custom tooltips
fig = px.scatter(x=np.arange(matrix_size).repeat(matrix_size),
                 y=np.tile(np.arange(matrix_size), matrix_size),
                 size=np.array([[10. for j in range(matrix_size)] for i in range(matrix_size) ]).flatten(),
                #  size=matrix_data.flatten(),
                #  size=30,
                 size_max=30,
                 color=matrix_data.flatten(),
                 color_continuous_scale="blackbody",
                 title="Matrix Visualization",
                 hover_name=[f"({i + 1}, {j + 1})" for i in range(matrix_size) for j in range(matrix_size)])


# colorscales: ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges', 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd']

# Set axis labels
def _scatter_layout(fig):
    fig.update_layout(xaxis_title="Column", yaxis_title="Row")
    fig.update_xaxes(showgrid=False, showticklabels=False, showline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, showline=False)
# Set square aspect ratio
    fig.update_layout(
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1
    ),
    yaxis=dict(
        scaleanchor="x",
        scaleratio=1
    )
)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

_scatter_layout(fig)

# Adjust margin to fit the plot well within the Streamlit app
st.plotly_chart(fig)

def sort_matrix(matrix):
    # Step 1: Flatten the matrix into a vector
    vector = matrix.flatten()

    # Step 2: Sort the vector
    sorted_vector = np.sort(vector)

    # Step 3: Reshape the sorted vector into a new matrix
    num_rows, num_cols = matrix.shape
    sorted_matrix = sorted_vector.reshape((num_rows, num_cols))

    return sorted_matrix

sorted_matrix_data = sort_matrix(matrix_data)

fig = px.scatter(x=np.arange(matrix_size).repeat(matrix_size),
                 y=np.tile(np.arange(matrix_size), matrix_size),
                 size=np.array([[10. for j in range(matrix_size)] for i in range(matrix_size) ]).flatten(),
                #  size=matrix_data.flatten(),
                #  size=30,
                 size_max=30,
                 color=sorted_matrix_data.flatten(),
                 color_continuous_scale="blackbody",
                 title="Matrix Visualization",
                 hover_name=[f"({i + 1}, {j + 1})" for i in range(matrix_size) for j in range(matrix_size)])

_scatter_layout(fig)
st.plotly_chart(fig)
