import os
import pandas as pd
from constants import BASE_DIR
from config import CONFIG


spreadsheet_file_path = os.path.join(BASE_DIR, "data", CONFIG.get("input_file_name", ""))


def get_raw_data():
    result = "CSV FINANCIAL DATA:\n\n"

    xl = pd.ExcelFile(spreadsheet_file_path)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=None)
        df.index += 1       # this 1-indexes the rows, so that the LLM returns the correct cell
        result += f"Sheet Name: {sheet_name}\n{df.to_csv()}\n"

    return result
