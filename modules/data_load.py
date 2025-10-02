import os
import pandas as pd
from modules.data_clean import clean


def load_data():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, "data", "swiftshop_sales_data.csv")
    df = pd.read_csv(data_path)
    return clean(df)
