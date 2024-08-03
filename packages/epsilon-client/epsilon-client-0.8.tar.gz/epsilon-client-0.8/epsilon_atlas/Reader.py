import os
import pandas as pd


class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        _, file_extension = os.path.splitext(self.file_path)
        if file_extension == '.csv':
            reader = CsvReader(self.file_path)
            return reader.read_data()
        elif file_extension in ['.xls', '.xlsx']:
            reader = XlsReader(self.file_path)
            return reader.read_data()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


class CsvReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        df = pd.read_csv(self.file_path)
        return self.extract_columns_and_types(df)

    def extract_columns_and_types(self, df):
        columns = df.columns.tolist()
        data = df.to_dict(orient='records')
        types = {col: self.infer_type(df[col]) for col in df.columns}
        return columns, data, types

    def infer_type(self, series):
        if pd.api.types.is_integer_dtype(series):
            return "int"
        elif pd.api.types.is_float_dtype(series):
            return "float"
        else:
            return "string"


class XlsReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        df = pd.read_excel(self.file_path)
        return self.extract_columns_and_types(df)

    def extract_columns_and_types(self, df):
        columns = df.columns.tolist()
        data = df.to_dict(orient='records')
        types = {col: self.infer_type(df[col]) for col in df.columns}
        return columns, data, types

    def infer_type(self, series):
        if pd.api.types.is_integer_dtype(series):
            return "int"
        elif pd.api.types.is_float_dtype(series):
            return "float"
        else:
            return "string"
