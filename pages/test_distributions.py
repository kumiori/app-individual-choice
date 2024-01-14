import streamlit as st
import numpy as np
import plotly.express as px

# Set a common random seed for reproducibility
np.random.seed(42)

# Function to plot histograms
def plot_distribution(data, title, distribution_formula):
    fig = px.histogram(data, nbins=50, title=title)
    st.plotly_chart(fig)
    st.markdown(f"$$f(x) = {distribution_formula}$$")

# Streamlit App
st.title("Distribution Plots")

# Number of distributions
num_distributions = 5

# Loop through distributions
for i in range(num_distributions):
    col1, col2 = st.columns(2)  # Create two columns

    # 1. Normal Distribution
    if i == 0:
        st.header("Normal Distribution")
        mu, sigma = st.slider("Select parameters for Normal Distribution", 0.1, 10.0, (0.0, 1.0))
        normal_data = np.random.normal(mu, sigma, 1000)
        plot_distribution(normal_data, "Normal Distribution", f"\\frac{1}{{\sqrt{{2\pi \sigma^2}}}} e^{{-\\frac{{(x - \mu)^2}}{{2\sigma^2}}}}")

    # 2. Exponential Distribution
    elif i == 1:
        st.header("Exponential Distribution")
        scale = st.slider("Select scale for Exponential Distribution", 0.1, 10.0, 1.0)
        exponential_data = np.random.exponential(scale, 1000)
        plot_distribution(exponential_data, "Exponential Distribution", "\\lambda e^{-\lambda x}")

    # 3. Uniform Distribution
    elif i == 2:
        st.header("Uniform Distribution")
        a, b = st.slider("Select parameters for Uniform Distribution", 0.0, 5.0, (0.0, 1.0))
        uniform_data = np.random.uniform(a, b, 1000)
        plot_distribution(uniform_data, "Uniform Distribution", "\\frac{1}{{b-a}}")

    # 4. Poisson Distribution
    elif i == 3:
        st.header("Poisson Distribution")
        lam = st.slider("Select lambda for Poisson Distribution", 1, 10, 3)
        poisson_data = np.random.poisson(lam, 1000)
        plot_distribution(poisson_data, "Poisson Distribution", "\\frac{e^{-\lambda} \lambda^x}{x!}")

    # 5. Beta Distribution
    elif i == 4:
        st.header("Beta Distribution")
        alpha, beta = st.slider("Select parameters for Beta Distribution", 0.1, 10.0, (2.0, 5.0))
        beta_data = np.random.beta(alpha, beta, 1000)
        plot_distribution(beta_data, "Beta Distribution", "\\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha, \beta)}")
