import os
import pandas as pd
from constants import BASE_DIR


spreadsheet_file_path = os.path.join(BASE_DIR, "data", "sample_input.xlsx")


class XlsxToCsv:
    def __init__(self):
        pass

    @staticmethod
    def _csv_output_directory_path(directory_path):
        return directory_path + '/csv_data'

    def is_initialized(self):
        csv_folder_path = self._csv_output_directory_path(os.path.join(BASE_DIR, "data"))
        return os.path.exists(csv_folder_path) and os.listdir(csv_folder_path)

    def convert(self, excel_file_path):
        # Extract the directory from the excel file path to save the CSVs in the same location
        directory = os.path.dirname(excel_file_path)

        # create a new folder called csv_data to save the csv files
        to_save_dir = self._csv_output_directory_path(directory)
        if not os.path.exists(to_save_dir):
            os.makedirs(to_save_dir)
        else:
            # check if data in the directory
            if os.listdir(to_save_dir):
                print("csv_data directory is not empty")
                return

        xls = pd.ExcelFile(excel_file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

            # Generate a CSV file name based on the Excel sheet name
            csv_file_name = f"{sheet_name}.csv"
            # If needed, adjust the path where CSV files will be saved (e.g., specific directory)
            csv_file_path = os.path.join(to_save_dir, csv_file_name)

            # Save the DataFrame to a CSV file
            df.to_csv(csv_file_path, index=False)
            print(f"Exported {sheet_name} to {csv_file_path}")


def get_csv_data():
    # for each file in csv_data folder
    # load the data into a pandas dataframe
    # get the dataframe
    result = "CSV FINANCIAL DATA:\n\n"

    folder_path = os.path.join(os.path.dirname(__file__), "../data", "csv_data")
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path, header=None)
            df.index += 1
            result += f"Sheet Name: {file}\n{df.to_csv()}\n"

    return result
