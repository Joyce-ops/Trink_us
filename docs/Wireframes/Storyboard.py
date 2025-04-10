import streamlit as st
from PIL import Image

image = Image.open("bild.png")
st.image(image, caption="Ein tolles Bild!", use_column_width=True)
