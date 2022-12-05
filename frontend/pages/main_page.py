import os
import pathlib
from os import listdir
from os.path import isfile, join

import requests
import pandas as pd
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

from logsetup import log_setup


logger = log_setup.logging.getLogger(__name__)
logger_r = log_setup.logging.getLogger('frontend')


# company's url logo
URL = 'https://res.cloudinary.com/dqgvfwvst/image/upload/v1669991725/tesseract_kwvpou.jpg'


def send_file(path: str):
    """Send .csv files interact with FastAPI endpoint.

    :param path: Path to csv folder directory
    :type path: str
    """

    url = "http://127.0.0.1:8000/uploadfile"
    files = {'file': open(path, 'rb')}
    try:
        requests.post(url, files=files)
    except requests.RequestException as e:
        logger.error("OOPS!! General Error")
        logger.error(str(e))
    finally:
        logger_r.info("Always executed complete")


def receive_csv_info(file_name: str) -> str:
    """Get dataset info from FastAPI endpoint.

    :param file_name: File name to get info
    :type file_name: str
    :return: Dataset information
    :rtype: str
    """

    url = f'http://localhost:8000/data/{file_name}'
    try:
        resp = requests.get(url)
        return resp.text
    except requests.RequestException as e:
        logger.error("OOPS!! General Error")
        logger.error(str(e))
    finally:
        logger_r.info("Always executed complete")


def add_logo(logo_url: str) -> None:
    """Add a logo (from logo_url) on the top of the sidebar.

    :param logo_url: URL of the logo
    :type logo_url: str
    """

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                background-image: url({logo_url});
                background-repeat: no-repeat;
                padding-top: 70px;
                background-position: 15px 40px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_file() -> str:
    """Saves the uploaded .csv file locally.

    :return: Path to data folder
    :rtype: str
    """

    parent_path = pathlib.Path(__file__).parent.parent.resolve()
    save_path = os.path.join(parent_path, "data")
    complete_name = os.path.join(save_path, uploaded_file.name)

    try:
        data = uploaded_file.getvalue().decode('utf-8')
        with open(complete_name, "w", encoding="utf-8") as destination_file:
            destination_file.write(data)
        send_file(complete_name)
        logger_r.info("Upload file locally and send .csv completed")
    except OSError as e:
        logger.error('Fail to save .csv file', e)
    except Exception as e:
        logger.error('Something went wrong', e)

    return save_path


def select_file(data_path: str) -> str:
    """Retrieves the path to specific file.

    :param data_path: Path to data folder
    :type data_path: str
    :return: Path to specific file
    :rtype: str
    """

    file_list = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    option = st.sidebar.selectbox('**Pick a dataset**', file_list)
    file_location = os.path.join(data_path, option)

    return file_location


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a UI on top of a dataframe to let viewers filter columns.

    :param df: Original dataframe
    :type df: pd.DataFrame
    :return: Filtered dataframe
    :rtype: pd.DataFrame
    """

    filter_container = st.sidebar.container()

    with filter_container:
        filtered_df = dataframe_explorer(df)

        want_drop_nulls = st.checkbox("**Drop null values**")

        if want_drop_nulls:
            to_drop_nulls = st.multiselect("Select columns", df.columns)

            drop_button = st.button('Apply')
            if drop_button:
                filtered_df.dropna(subset=to_drop_nulls, inplace=True)

    return filtered_df


@st.cache
def convert_df(df: pd.DataFrame) -> bytes:
    """Converts dataframe to .csv file.

    :param df: Filtered dataframe
    :type df: pd.DataFrame
    :return: .csv file
    :rtype: bytes
    """

    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


# MAIN PAGE STRUCTURE

st.title("TESSERACT")

st.markdown(
    """**Use this app to filter any dataframe you choose**
    """
)

add_logo(URL)

st.subheader('Choose a file')

uploaded_file = st.file_uploader((''))
# All tasks to be done when the user uploads a .csv file
if uploaded_file is not None:
    data_path = save_file()
    file_location = select_file(data_path)

    try:
        df = pd.read_csv(file_location)
    except FileNotFoundError as e:
        logger.error("File doesn't exist", e)
    except Exception as e:
        logger.error('Something went wrong', e)

    # Button display dataset info
    st.sidebar.markdown(
        """**Show dataset information**
    """
    )
    if st.sidebar.button('Request'):
        dataset_info = receive_csv_info(uploaded_file.name)
        st.text(dataset_info)
    else:
        st.sidebar.write('Received info complete')

    # Filters the user can apply
    modify = st.sidebar.checkbox("**Add filters**")
    if modify:
        filtered_df = filter_dataframe(df)
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

    # User can download filtered data
    save_filtered_df = st.sidebar.checkbox("Save results")

    if save_filtered_df:
        csv = convert_df(df)
        st.sidebar.download_button(
            label="Download",
            data=csv,
            file_name='filtered_df.csv',
            mime='text/csv',
        )
