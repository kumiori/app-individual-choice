import streamlit as st

# Set page configuration
st.set_page_config(page_title="Cool CSS/JS Effect", page_icon="✨")

# Title of the app
st.title("Cool CSS/JS Effect in Streamlit")

# Description
st.write("This is a simple Streamlit app demonstrating a cool CSS/JavaScript effect.")

# Embed custom CSS and JavaScript using st.markdown
st.markdown("""
    <style>
        body {
            background: #2e2e2e;
            color: #f1f1f1;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }

        .cool-effect {
            margin: 50px auto;
            width: 300px;
            height: 300px;
            background-color: #1a1a1a;
            border-radius: 50%;
            position: relative;
            overflow: hidden;
        }

        .cool-effect:before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, #ff0040, #ffcc00, #00ff40, #00ccff, #ff00ff, #ff0040);
            animation: rotate 10s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    <div class="cool-effect"></div>
""", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Enjoy the cool CSS/JS effect!")
