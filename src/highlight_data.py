from datatypes import MetricAnswer
import os
from constants import BASE_DIR


def create_highlighted_excel_file(metric_answer: MetricAnswer):
    if not metric_answer:
        print("Error: LLM unable to answer query, no Excel file created")
        return

    # Create a new Excel file with the relevant cells highlighted
    # Load the CSV data into a pandas DataFrame
    csv_folder_path = os.path.join(BASE_DIR, "data", "csv_data")
