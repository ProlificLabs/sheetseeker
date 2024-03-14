import os
import pandas as pd
from constants import BASE_DIR
from config import CONFIG

spreadsheet_file_path = os.path.join(BASE_DIR, "data", CONFIG.get("input_file_name", ""))


def get_raw_data() -> str:
    """
    Read the Excel file, get all the data from all the sheets,
    and then concatenate the raw data into a single string in preparation for the LLM
    - need to ensure that the stringified data is indexed correctly so that the LLM can identify cells correctly
    - also need to label each sheet's data with the sheet name when we concatenate

    Strategy is to turn the cells into a CSV format: the LLM can understand stringified CSV data

    :return: stringified raw data from the Excel spreadsheet
    """
    result = "RAW FINANCIAL DATA:\n\n"

    xl = pd.ExcelFile(spreadsheet_file_path)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=None)
        df.index += 1       # this 1-indexes the rows, so that the LLM returns the correct cell

        # outputting CSV data: we found a LLM prompt that works with CSV data
        result += f"Sheet Name: {sheet_name}\n{df.to_csv()}\n"

    return result
