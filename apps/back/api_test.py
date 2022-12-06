import datetime
import sys
import unittest
import asyncio
import tempfile


from fastapi import UploadFile
from fastapi.responses import FileResponse

sys.path.append('./')
import api


class MyTests(unittest.TestCase):
    def test_file_upload(self):
        # Simulate a file upload initializing the class, adding content and file name.
        test_file = UploadFile
        test_file.file = tempfile.SpooledTemporaryFile("Testing")
        test_file.filename = "testfile.txt"
        
        self.assertEqual(asyncio.run(api.create_upload_file(test_file)), True)
    
    def test_file_read(self):
        file = 'test_file_to_read.txt'

        self.assertIsInstance(asyncio.run(api.read_select_dataset(file)), FileResponse)


# Header to be written at the top of the testing.txt file
def insert_header(f):
    f.write('\n')
    f.write('******************TESTING******************')
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
    print ('Results logged to root/docs/txt/api-testing.txt')

if __name__ == '__main__':
    with open('../../docs/txt/api-testing.txt', 'a') as f:
        f = insert_header(f)
        main(f)