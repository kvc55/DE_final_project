import os
import pathlib
import requests
from os import listdir
from os.path import isfile, join
import base64


import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

#from logsetup import log_setup

#logger = log_setup.logging.getLogger(__name__)
#logger_r = log_setup.logging.getLogger('result')

def send_file(path: str) -> str :
    """Send csv files interact with FastAPI endpoint.

    Args:
        path (str): Path to csv folder directory
    """
    url = "http://127.0.0.1:8000/uploadfile"
    files = {'file': open(path, 'rb')}
    try:
        res = requests.post(url, files=files)
    except requests.RequestException as e:
        #logger.error("OOPS!! General Error")
        #logger.error(str(e))
        pass
    finally:
        #logger_r.info("Always executed complete")
        pass
        
def save_file():
    data = uploaded_file.getvalue().decode('utf-8')
    parent_path = pathlib.Path(__file__).parent.parent.resolve()           
    save_path = os.path.join(parent_path, "data")
    complete_name = os.path.join(save_path, uploaded_file.name)

    with open(complete_name, "w", encoding="utf-8") as destination_file:
        destination_file.write(data)
        
    #Send file to server
    send_file(complete_name)
    #logger_r.info("Upload data and send csv file completed")
    return save_path


def select_file(data_path):
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    option = st.sidebar.selectbox('Pick a dataset', onlyfiles)
    file_location = os.path.join(data_path, option)

    return file_location


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    
    st.write(file_location)

    modify = st.sidebar.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.sidebar.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        
        for column in to_filter_columns:
            left, right = st.columns((1, 20)) # needs review
            left.write("↳")
            # Treat columns with < 10 unique values as categorical ---> review cities
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100 # ------> review
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]
        


        want_drop_nulls = st.checkbox("Drop null values")

        if want_drop_nulls:
            to_drop_nulls = st.multiselect("Select columns", df.columns)

            drop_button = st.button('Apply')
            if drop_button:
                df.dropna(subset=to_drop_nulls, inplace=True)

    return df



def drop_nulls(df: pd.DataFrame) -> pd.DataFrame:
    want_drop_nulls = st.sidebar.checkbox("Drop null values")
    
    if want_drop_nulls:
        to_drop_nulls = st.sidebar.multiselect("Select columns", df.columns)

        drop_button = st.sidebar.button('Apply')
        if drop_button:
            df.dropna(subset=to_drop_nulls, inplace=True)

    return df
            
#@st.cache(hash_funcs={st.delta_generator.DeltaGenerator: hash})
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def save_filtered_df(df: pd.DataFrame) -> None:
    save_filtered_df = st.sidebar.checkbox("Save results")
    
    if save_filtered_df:
        csv = convert_df(df)
        st.sidebar.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='large_df.csv',
            mime='text/csv',
        )




def download_link(object_to_download, download_filename, download_link_text):

    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=True)

    # some strings <-> bytes conversions necessary here
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def save_df(df):
    if st.button('Download Dataframe as CSV'):
        tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)





st.title("TESSERACT")

st.markdown(
    """**Use this app to filter any dataframe you choose**
    """
)


st.subheader('Choose a file')
uploaded_file = st.file_uploader((''))
if uploaded_file is not None:
  data_path = save_file()
  file_location = select_file(data_path)
  
  df = pd.read_csv(file_location)
  
  
  filtered_dataframe = st.dataframe(filter_dataframe(df))
  #st.write(type(filtered_dataframe))
  #st.dataframe(drop_nulls(filtered_dataframe))

  #save_filtered_df(filtered_dataframe)

  #convert_df(filtered_dataframe)

#save_df(df)