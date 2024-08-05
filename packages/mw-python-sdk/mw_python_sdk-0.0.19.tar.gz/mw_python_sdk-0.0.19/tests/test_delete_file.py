import unittest
import os
import json
from dataclasses import asdict
from mw_python_sdk import download_file, get_dataset,delete_file


class TestDownloadFile(unittest.TestCase):
    def test_download(self):
        dataset_id_tmp = "64e6c644c60d2823b0a2e266"
        try:  # Example assertion
            dataset = get_dataset(dataset_id_tmp)
            print(dataset.files)
            delete_file(dataset_id_tmp, "README.md")
        except Exception as err:
            print(f"An error occurred: {err}")

if __name__ == "__main__":
    unittest.main()
