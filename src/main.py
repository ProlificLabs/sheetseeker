from typing import List

from datatypes import MetricAnswer
from highlight import create_highlighted_excel_file
from llm import llm_query
from parse_sheet import get_raw_data
from config import CONFIG


def run(query: str = CONFIG.get("query", "")):
    """
    Run the main application logic

    General flow of logic:
    - read data from the Excel spreadsheet
    - get the metrics we want to query
    - send the raw data + target metrics to an LLM
    - get structured data back from the LLM
        - containing which cells need to be highlighted in the spreadsheet, per metric
    - for each metric, create a new spreadsheet and highlight the relevant cells

    :return:
    """
    try:
        csv_data = get_raw_data()
    except FileNotFoundError as err:
        print(
            f"FileNotFoundError: {err.strerror} {err.filename}.\n "
            f"Please ensure that the file exists and is in the /data folder.\n "
            f"Also ensure that the file name is correctly set in config.py."
        )
        return

    metric_answers: List[MetricAnswer] = llm_query(query, csv_data)
    print(f"Metric Answer: {metric_answers}")

    created_file_path = create_highlighted_excel_file(metric_answers)
    print(f"Highlighted file created at: {created_file_path}")


if __name__ == "__main__":
    run()
