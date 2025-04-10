import streamlit as st
from PIL import Image

image = Image.open("Storyboard.png")
st.image(image, caption="Storyboard von der App Trink_us!", use_column_width=True)
