import os
from os import path
import logging
import logging.config
import pandas as pd
import io

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse


# Load logger config files.
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logs/log_config_file.cfg')
logging.config.fileConfig(log_file_path)

# Declare logger to be used in this context.
logger = logging.getLogger('backend')

app = FastAPI()

# UPLOAD FILE
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    '''create_upload_file: a file is uploaded and saved to the relative folder directory.

    Args:
        file (UploadFile): uploaded file to save.

    Returns:
        log: success or fail as a logger response.
    '''
    try:
        folder = '../../data'
        create_or_exists(folder)

        file_location = f"{folder}/{file.filename}" # Save to the 'data' folder.
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        logger.info({"info": f"file '{file.filename}' saved at '{file_location}'"})
        return True

    except Exception as e:
        logger.error({"Error:": f"file '{file.filename}' has not been saved at '{file_location}'. Full error: '{e}'"})
        return e

# READ FILE
@app.get("/data/{file_name}")
async def read_select_dataset(file_name: str):
    '''read_select_dataset: reads a selected file and converts it to data.
    Args:
        file_name (str): uploaded file to process.
    Returns:
        fileResponse: text file.
    '''

    try:
        folder = '../../data'
        folder_temp = '../../temp'
        # Create folders or check if they already exist..
        create_or_exists(folder)
        create_or_exists(folder_temp)

        file_path = f"{folder_temp}/info.txt"
        file_location = f"{folder}/{file_name}"
        
        df = pd.read_csv(file_location)
        
        buffer = io.StringIO()
        df.info(buf=buffer, verbose=True)
        buffer_value = buffer.getvalue()

        with open(file_path, "w",encoding="utf-8") as f:  
            f.write(buffer_value)

        return FileResponse(path=file_path, filename=file_path, media_type='text')
    
    except Exception as e:
        logger.error({"Error:": f"failed to read file. Full error: {e}"})

# SPECIFIC METHODS
def create_or_exists(folder):
    # Create folder if it doesn't exist.
    if not os.path.isdir(folder):
        os.mkdir(folder)