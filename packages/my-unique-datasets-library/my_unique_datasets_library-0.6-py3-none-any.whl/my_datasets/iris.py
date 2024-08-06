# my_datasets/iris.py

import os
import pandas as pd
from pkg_resources import resource_filename

def list_available_datasets():
    """
    List all available datasets in the library's data folder.
    :return: List of dataset filenames.
    """
    data_dir = resource_filename(__name__, 'data')
    
    if not os.path.exists(data_dir):
        return []
    
    return [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

def load_dataset(dataset_name):
    """
    Load a specified dataset from the library's data folder.
    :param dataset_name: Name of the dataset file (e.g., 'walmart.csv').
    :return: DataFrame containing the specified dataset.
    """
    data_path = resource_filename(__name__, f'data/{dataset_name}')
    
    if not os.path.exists(data_path):
        available_datasets = list_available_datasets()
        print(f"Dataset '{dataset_name}' was not found.")
        print("Available datasets:")
        for dataset in available_datasets:
            print(f" - {dataset}")
        return None  # Or raise an exception if preferred
    
    df = pd.read_csv(data_path)
    return df

