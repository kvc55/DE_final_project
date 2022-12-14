from PIL import Image
import urllib.request

import streamlit as st
import hydralit_components as hc

from page_one import put_image
from page_two import create_page_two
from page_three import show_graphs

URL = 'https://res.cloudinary.com/dqgvfwvst/image/upload/v1670789306/TESSERACT_z7lwzh.png'

#make it look nice from the start
st.set_page_config(layout='wide')

#_, col2, _ = st.columns([1, 30, 1])

# specify the primary menu definition
menu_data = [
    {'icon': "🏠", 'label':"Home"},
    {'icon': "📚",'label':"Project"},
    {'icon': "📊", 'label':"Charts"},
]

over_theme = {
    'txc_inactive': '#FFFFFF',
    'menu_background':'#334354'
    }

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=True, # will show the st hamburger as well as the navbar now!
    sticky_nav=True, # at the top or not
    sticky_mode='sticky', # jumpy or not-jumpy, but sticky or pinned
)

st.write('\n')
st.write('\n')

urllib.request.urlretrieve(
    URL,
    "logo.png")

image = Image.open('logo.png')
st.image(image, width=300)

change_footer = """
    <style>

    footer{
        visibility: hidden;
        }
    footer:after{
            visibility: visible;
            content: '© 2022 TESSERACT. All Rights Reserved.'; 
            display: block;         
        }
    <style>
    """

st.markdown(change_footer, unsafe_allow_html=True)


if menu_id == 'Home':
    put_image()
elif menu_id == 'Project':
    create_page_two()
elif menu_id == 'Charts':
    show_graphs()