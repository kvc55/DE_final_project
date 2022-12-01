from fastapi import FastAPI, UploadFile
import os
import logging

# LOGGING CONFIG
logging.basicConfig(
    level= logging.INFO,
    filename='result.log',
    filemode= 'a',
    datefmt= '%d - %b-%y %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()


# API ROUTES #
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    '''create_upload_file: a file is uploaded and saved to the relative folder directory.

    Args:
        file (UploadFile): uploaded file to save.

    Returns:
        log: success or fail as a logger response.
    '''

    try:
        folder = './data'
        # Create folder if it doesn't exist.
        if not os.path.isdir(folder):
            os.mkdir(folder)

        file_location = f"../{folder}/{file.filename}" # Save to the 'data' folder.
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        logging.info({"info": f"file '{file.filename}' saved at '{file_location}'"})
        return True

    except Exception as e:
        logging.error({"info": f"file '{file.filename}' has not been saved at '{file_location}'. Full error: '{e}'"})