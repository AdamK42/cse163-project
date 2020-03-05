import pandas as pd

def read_in_dataset(file_name):
    """
    Takes a dataset name. Returns the dataset as a pandas dataframe
    """
    return pd.read_excel(file_name)

df = read_in_dataset("datasets/total_applicants.xlsx")
df