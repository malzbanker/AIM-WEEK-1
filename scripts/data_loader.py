import pandas as pd

def load_stock_data(file_path):
    """
    Load stock market data from csv file

    args:
    file_path(str) path to the csv file

    return:
    pd.datafram: loaded  data
    """
    return pd.read_csv(file_path,parse_dates=["Date"])