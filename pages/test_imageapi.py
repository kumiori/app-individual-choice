import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def fetch_image(image_name, size, quality):
    # Assuming the images are stored locally, replace the URL with your image server URL
    image_url = f"http://your_image_server_url/{image_name}.jpg"
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    
    # Open the image using PIL
    image = Image.open(BytesIO(response.content))
    
    # Resize the image
    width, height = size.split('x')
    width, height = int(width), int(height)
    image = image.resize((width, height))
    
    # Convert the image to bytes with the specified quality
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=quality)
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def main():
    st.title("Image as a Service")

    # Get query parameters from URL
    image_name = st.query_params.get("image_name", "example_image")
    size = st.query_params.get("size", "300x300")
    quality = int(st.query_params.get("quality", 85))

    # Sidebar inputs for optional overriding of parameters
    image_name_input = st.sidebar.text_input("Image Name", value=image_name)
    size_input = st.sidebar.text_input("Size (format: widthxheight)", value=size)
    quality_input = st.sidebar.slider("Quality", min_value=1, max_value=100, value=quality)

    _params = {'image_name': image_name_input, 'size': size_input, 'quality': str(quality_input)}
    # Update query parameters based on sidebar inputs
    st.query_params.update(_params)

    if st.sidebar.button("Generate Image"):
        try:
            image_bytes = fetch_image(image_name_input, size_input, quality_input)
            st.image(image_bytes, use_column_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
