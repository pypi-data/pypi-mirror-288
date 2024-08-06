import unittest
from mw_python_sdk import list_datasets


class TestListDatasets(unittest.TestCase):
    def test_dataset_create(self):
        try:
            datasets_list = list_datasets("llama3chinese")
            print(datasets_list.datasets)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
