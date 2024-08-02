import os
import pandas as pd

def load_dataset(name):
    # Define the path to the datasets
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    dataset_path = os.path.join(data_dir, f'{name}.csv')
    
    # Check if the dataset exists
    if not os.path.isfile(dataset_path):
        raise ValueError(f"Dataset {name} does not exist.")
    
    # Load and return the dataset as a DataFrame
    return pd.read_csv(dataset_path)
