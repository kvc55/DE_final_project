from PIL import Image
import urllib.request

import streamlit as st

URL = 'https://res.cloudinary.com/dqgvfwvst/image/upload/v1670689699/empresa_e3yccb.jpg'

def put_image():    
    st.subheader('**Working team**')

    urllib.request.urlretrieve(
        URL,
        "empresa.jpg")

    image = Image.open('empresa.jpg')
    st.image(image)
    
 
