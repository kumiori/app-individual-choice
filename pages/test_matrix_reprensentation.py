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




matrix_size = 15  # Adjust the matrix size as needed

# Define the probabilities for each outcome
probabilities = [0.6, 0.3, 0.1]

# Generate a random matrix using the specified probabilities
matrix_data = np.random.choice([0, 1, np.random.uniform(0, 1)], size=(matrix_size, matrix_size), p=probabilities)

# Flatten the matrix for plotting
flatten_matrix_data = matrix_data.flatten()

# Plot the scatter plot
fig = px.scatter(
    x=np.arange(matrix_size).repeat(matrix_size),
    y=np.tile(np.arange(matrix_size), matrix_size),
    size=np.full_like(flatten_matrix_data, 10),
    size_max=30,
    color=flatten_matrix_data,
    color_continuous_scale="blackbody",
    title="Matrix Visualization",
    hover_name=[f"({i + 1}, {j + 1})" for i in range(matrix_size) for j in range(matrix_size)]
)

# Show the plot
# fig.show()

_scatter_layout(fig)
st.plotly_chart(fig)


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



# Set a common random seed for reproducibility
np.random.seed(42)

# Function to plot histograms
# def plot_distribution(data, title):
#     plt.figure(figsize=(8, 6))
#     sns.histplot(data, kde=True)
#     plt.title(title)
#     plt.xlabel("Value")
#     plt.ylabel("Probability Density")
#     st.pyplot(plt)







import pandas as pd

# Title for the Streamlit app
st.title("Scatter Plot with NaN Values")

# Example matrix with NaN values
matrix = np.array([
    [1.0, 2.0, np.nan],
    [4.0, np.nan, 6.0],
    [7.0, 8.0, 9.0]
])

# Convert matrix to a DataFrame for plotting
df = pd.DataFrame(matrix, columns=['A', 'B', 'C'])

# Melt the DataFrame to a long format
df_long = df.reset_index().melt(id_vars='index', var_name='Category', value_name='Value')

# Create a new column to indicate NaN values
df_long['IsNaN'] = df_long['Value'].isna()

# Replace NaN values with a specific value for plotting (e.g., -1)
df_long['Value'] = df_long['Value'].fillna(-1)

# Create a scatter plot
fig = px.scatter(
    df_long,
    x='index',
    y='Value',
    color='IsNaN',
    symbol='IsNaN',
    labels={'index': 'Index', 'Value': 'Value', 'IsNaN': 'NaN Status'},
    title='Scatter Plot with NaN Values'
)

# Customize markers: differentiate NaN points
fig.update_traces(marker=dict(size=12), selector=dict(marker_symbol='circle'))
fig.update_traces(marker=dict(size=12, color='red'), selector=dict(marker_symbol='cross'))

# Display the plot in Streamlit
_scatter_layout(fig)
st.plotly_chart(fig)



# Function to plot histograms
def plot_distribution(data, title, distribution_formula):
    fig = px.histogram(data, nbins=50, title=title)
    st.plotly_chart(fig)
    st.latex(f'''f(x) = {distribution_formula}''')






# Streamlit App
st.title("Distribution Plots")

# Number of distributions
num_distributions = 5
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')

# Loop through distributions
for i in range(num_distributions):
    col1, col2 = st.columns(2)  # Create two columns

    # 1. Normal Distribution
    if i == 0:
        st.header("Normal Distribution")
        mu, sigma = st.slider("Select parameters for Normal Distribution", 0.1, 10.0, (0.0, 1.0))
        st.write("mu =", mu, "sigma =", sigma)
        normal_data = np.random.normal(mu, sigma, 1000)
        plot_distribution(normal_data, "Normal Distribution", f"\\frac{1}{{\sqrt{{2\pi \sigma^2}}}} e^{{-\\frac{{(x - \mu)^2}}{{2\sigma^2}}}}")

    # 2. Exponential Distribution
    elif i == 1:
        st.header("Exponential Distribution")
        scale = st.slider("Select scale for Exponential Distribution", 0.1, 10.0, 1.0)
        st.write("scale =", scale)
        exponential_data = np.random.exponential(scale, 1000)
        plot_distribution(exponential_data, "Exponential Distribution", "\\lambda e^{-\lambda x}")

    # 3. Uniform Distribution
    elif i == 2:
        st.header("Uniform Distribution")
        a, b = st.slider("Select parameters for Uniform Distribution", 0.0, 5.0, (0.0, 1.0))
        st.write("a =", a, "b =", b)
        uniform_data = np.random.uniform(a, b, 1000)
        plot_distribution(uniform_data, "Uniform Distribution", "\\frac{1}{{b-a}}")

    # 4. Poisson Distribution
    elif i == 3:
        st.header("Poisson Distribution")
        lam = st.slider("Select lambda for Poisson Distribution", 1, 10, 3)
        st.write("lambda =", lam)
        poisson_data = np.random.poisson(lam, 1000)
        plot_distribution(poisson_data, "Poisson Distribution", "\\frac{e^{-\lambda} \lambda^x}{x!}")

    # 5. Beta Distribution
    elif i == 4:
        st.header("Beta Distribution")
        alpha, beta = st.slider("Select parameters for Beta Distribution", 0.1, 10.0, (2.0, 5.0))
        st.write("alpha =", alpha, "beta =", beta)
        beta_data = np.random.beta(alpha, beta, 1000)
        plot_distribution(beta_data, "Beta Distribution", "\\frac{x^{\\alpha-1}(1-x)^{\\beta-1}}{B(\\alpha, \\beta)}")