import datetime
import sys
import os
import unittest
import asyncio
import tempfile

from fastapi import UploadFile
from fastapi.responses import FileResponse

# Import ENV variables.
from dotenv import load_dotenv, find_dotenv
load_dotenv (find_dotenv('../config/.env'))

# Read backend directory and import API.
sys.path.append(f'{os.getenv("ROOT_PATH")}/apps/back/')
import api 

class MyTests(unittest.TestCase):
    def test_file_upload_and_read(self):
        # Test file upload initializing the class, adding content and file name.
        test_file = UploadFile
        test_file.file = tempfile.TemporaryFile()
        test_file.filename = "olist_customers_dataset.csv"
        test_file.file.write(b'hello,world')
        test_file.file.seek(0)

        # Write File
        self.assertEqual(asyncio.run(api.create_upload_file(test_file)), True)
        # Read file
        self.assertIsInstance(asyncio.run(api.read_select_dataset(test_file.filename)), FileResponse)


# Header to be written at the top of the testing.txt file
def insert_header(f):
    f.write('\n')
    f.write('****************** API INTEGRATION TESTS ******************')
    f.write('\n')
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(date_time)
    f.write('\n')
    return f

def main(out = sys.stderr, verbosity = 2):
    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite)
    print (f'Results logged to {os.getenv("ROOT_PATH")}/docs/txt/api-integration-tests.txt')

if __name__ == '__main__':
    with open(f'{os.getenv("ROOT_PATH")}/docs/txt/api-integration-tests.txt', 'w') as f:
        f = insert_header(f)
        main(f)