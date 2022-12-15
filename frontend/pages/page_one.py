
from PIL import Image
import urllib.request

import streamlit as st

URL = 'https://res.cloudinary.com/dqgvfwvst/image/upload/v1670689699/empresa_e3yccb.jpg'

def put_image():    
    
    urllib.request.urlretrieve(
        URL,
        "empresa.jpg")
    st.write(' ')
    st.markdown("<h2 style='text-align: center; color: black;'>TESSERACT - ONLINE DATA BROWSER </h2>", unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')
        
        
        

    with col2:
        image = Image.open('empresa.jpg')
        st.image("empresa.jpg")
        st.write(' ')
        st.subheader(' 📚 Project to upload csv files and work with them')
        st.subheader(' 📊 Charts to view quick graphs of the csv files')

    with col3:
        st.write(' ')



 
