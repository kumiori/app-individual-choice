import streamlit as st
import numpy as np
from streamlit_image_select import image_select

from PIL import Image

img = image_select(
    label="Select a cat",
    images=[
        "https://bagongkia.github.io/react-image-picker/0759b6e526e3c6d72569894e58329d89.jpg",
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/APC_3171.jpg")),
    ],
    # captions=["A cat"],
)