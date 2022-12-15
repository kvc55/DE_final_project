
import datetime
import os
import sys
import unittest
import asyncio
import tempfile

from fastapi import UploadFile
from fastapi.responses import FileResponse

# Import ENV variables.
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('../config/.env'))

# Read backend directory and import API.
sys.path.append(f'{os.getenv("ROOT_PATH")}/apps/back/')
import api 


class ApiTests(unittest.TestCase):
    def test_correct_file_upload(self):
        # Test file upload initializing the class, adding content and file name.
        test_file = UploadFile
        test_file.file = tempfile.TemporaryFile()
        test_file.filename = "testfile.csv"
        test_file.file.write(b'hello,world')
        test_file.file.seek(0)
        
        self.assertEqual(asyncio.run(api.create_upload_file(test_file)), True)

    def test_incorrect_type_file_upload(self):
        # Test file upload initializing the class, adding content and file name.
        test_file = UploadFile
        test_file.file = tempfile.TemporaryFile()
        test_file.filename = "testfile.txt"
        test_file.file.write(b'hello,world')
        test_file.file.seek(0)
        
        with self.assertRaises(AssertionError):
            asyncio.run(api.create_upload_file(test_file))
    
    def test_file_read(self):
        file = 'test_file_to_read.txt'
        self.assertIsInstance(asyncio.run(api.read_select_dataset(file)), FileResponse)


# Header to be written at the top of the testing.txt file
def insert_header(f):
    f.write('\n')
    f.write('****************** API TESTS ******************')
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
    print (f'Results logged to {os.getenv("ROOT_PATH")}/docs/txt/api-testing.txt')

if __name__ == '__main__':
    with open(f'{os.getenv("ROOT_PATH")}/docs/txt/api-testing.txt', 'a') as f:
        f = insert_header(f)
        main(f)