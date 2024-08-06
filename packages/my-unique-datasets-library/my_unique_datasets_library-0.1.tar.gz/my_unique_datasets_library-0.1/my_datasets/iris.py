# my_datasets/iris.py

import os
import pandas as pd

def load_iris_dataset():
    """
    Load the Iris dataset from the library's data folder.
    :return: DataFrame containing the Iris dataset.
    """
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, 'data', 'iris.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The dataset file at {data_path} was not found.")
    
    df = pd.read_csv(data_path)
    return df

