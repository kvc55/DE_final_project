import os
import pathlib
import requests
from os import listdir
from os.path import isfile, join

import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def send_file(path:str) -> str :
    url = "http://127.0.0.1:8000/uploadfile"
    files = {'file': open(path, 'rb')}
    try:
        res = requests.post(url, files=files)
    except requests.RequestException as e:
         print("OOPS!! General Error")
         print(str(e))
    finally:
        return "Send file csv"

def save_file():
    data = uploaded_file.getvalue().decode('utf-8')
    parent_path = pathlib.Path(__file__).parent.parent.resolve()           
    save_path = os.path.join(parent_path, "data")
    complete_name = os.path.join(save_path, uploaded_file.name)
    destination_file = open(complete_name, "w")
    destination_file.write(data)
    destination_file.close()
    print(complete_name)
    #send file to server
    send_file(complete_name)
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
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        #print(to_filter_columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20)) #no entiendo
            left.write("↳")
            # Treat columns with < 10 unique values as categorical ---> reveer el tema de las ciudades
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
                step = (_max - _min) / 100 # ------> mmmm reveer, no sera porque tenia 100 filas??
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
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df






st.title("PRISMA")

st.write(
    """Use this app to filter any dataframe you choose
    """
)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  data_path = save_file()
  file_location = select_file(data_path)


  df = pd.read_csv(file_location)

  st.dataframe(filter_dataframe(df))


