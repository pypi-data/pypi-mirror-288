import unittest
from mw_python_sdk import upload_folder  # , upload_file


class TestUploadFolder(unittest.TestCase):
    def test_upload_folder(self):
        dataset_id_tmp = "64e6c644c60d2823b0a2e266"
        try:  # Example assertion
            upload_folder("tests", "", dataset_id_tmp)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
