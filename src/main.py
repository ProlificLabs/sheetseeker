from highlight import create_highlighted_excel_file
from llm import llm_query
from parse_sheet import get_raw_data
from config import CONFIG


def run():
    csv_data = get_raw_data()
    metric_answers = llm_query(CONFIG.get("query", ""), csv_data)
    print(f"Metric Answer: {metric_answers}")
    created_file_path = create_highlighted_excel_file(metric_answers)
    print(f"Highlighted file created at: {created_file_path}")


if __name__ == "__main__":
    run()
