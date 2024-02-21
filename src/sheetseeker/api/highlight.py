from sheetseeker.spreadsheet.operations.highlight import highlight

DEFAULT_STRATEGY = "two_step_loose"

def highlight_spreadsheet(query: str, spreadsheet_file_path: str, output_file_path: str=None, strategy: str=None) -> None:
    '''
    Given a user query for some data they want to highlight and a spreadsheet
    file with the data, create a duplicate spreadsheet with the appropriate
    cells highlighted.
    '''

    highlight(query, spreadsheet_file_path, output_file_path=output_file_path, strategy=strategy or DEFAULT_STRATEGY)
