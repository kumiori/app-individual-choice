import streamlit as st
import numpy as np
from streamlit_image_select import image_select

from PIL import Image

image_paths = [
"images/cards/crop/share-24041611083.jpg",
"images/cards/crop/share-24021711083.jpg",
"images/cards/crop/share-24061711083.jpg",
"images/cards/crop/share-24081611083.jpg",
"images/cards/crop/share-24121711083.jpg",
"images/cards/crop/share-24131611083.jpg",
"images/cards/crop/share-24171611083.jpg",
"images/cards/crop/share-24191711083.jpg",
"images/cards/crop/share-24231611083.jpg",
"images/cards/crop/share-24271611083.jpg",
"images/cards/crop/share-24281711083.jpg",
"images/cards/crop/share-24331711083.jpg",
"images/cards/crop/share-24381611083.jpg",
"images/cards/crop/share-24391511083.jpg",
"images/cards/crop/share-24551611083.jpg",
"images/cards/crop/share-24561511083.jpg",
"images/cards/crop/share-24471311083.jpg"
]

# Shuffle the list of image paths
np.random.shuffle(image_paths)
print(image_paths)



# Initialize a list to store np.array(Image.open()) objects
image_arrays = []

for path in image_paths:
    image = Image.open(path)
    image_array = np.array(image)
    image_arrays.append(image_array)


img = image_select(
    label="Select a cat",
    images=[
        np.array(Image.open("images/APC_3171.jpg")),
        np.array(Image.open("images/cards/crop/share-24021711083.jpg")),
        np.array(Image.open("images/cards/crop/share-24041611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24061711083.jpg")),
        np.array(Image.open("images/cards/crop/share-24081611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24121711083.jpg")),
        np.array(Image.open("images/cards/crop/share-24131611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24171611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24191711083.jpg")),
        np.array(Image.open("images/cards/crop/share-24231611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24271611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24281711083.jpg")),
        np.array(Image.open("images/cards/crop/share-24331711083.jpg")),
        np.array(Image.open("images/cards/crop/share-24381611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24391511083.jpg")),
        np.array(Image.open("images/cards/crop/share-24551611083.jpg")),
        np.array(Image.open("images/cards/crop/share-24561511083.jpg")),
    ],
    # captions=["A cat"],
)



# img = image_select(
#     label="Select a cat",
#     images=image_arrays,
#     # captions=["A cat"],
# )