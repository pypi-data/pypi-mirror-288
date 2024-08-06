import os
import pandas as pd
from pkg_resources import resource_filename

def load_iris_dataset():
    """
    Load the Iris dataset from the library's data folder.
    :return: DataFrame containing the Iris dataset.
    """
    # Get the path to the data file in the installed package
    data_path = resource_filename(__name__, 'data/Iris.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The dataset file at {data_path} was not found.")
    
    df = pd.read_csv(data_path)
    return df

