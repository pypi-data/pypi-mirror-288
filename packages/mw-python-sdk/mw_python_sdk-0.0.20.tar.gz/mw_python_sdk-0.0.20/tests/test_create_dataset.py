import unittest
from mw_python_sdk import create_dataset, delete_dataset, upload_file


class TestCreateDataset(unittest.TestCase):
    def test_dataset_create(self):
        try:
            dataset = create_dataset("llama3chinese")
            print(dataset.title)
            assert dataset.title == "llama3chinese"
            upload_file("README.md", "test/README.md", dataset)
            delete_dataset(dataset)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
