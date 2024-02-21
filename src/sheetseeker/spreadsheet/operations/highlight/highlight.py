import re
from sheetseeker.spreadsheet import Spreadsheet

from .strategies import *

def highlight(query: str, spreadsheet_file_path: str, output_file_path=None, strategy=None) -> None:
    '''Load the spreadsheet, select a strategy, execute the strategy, and apply the outcome to the spreadsheet. Finally save a copy of the spreadsheet with the changes'''
    spreadsheet = Spreadsheet(spreadsheet_file_path)

    cells_identified = None
    match strategy:
        case "one_shot_simple":
            cells_identified = one_shot_simple(query, spreadsheet)
        case "one_shot_multistep":
            cells_identified = one_shot_multistep(query, spreadsheet)
        case "two_step_strict":
            cells_identified = two_step_strict(query, spreadsheet)
        case "two_step_loose":
            cells_identified = two_step_loose(query, spreadsheet)
        case "row_col_based":
            cells_identified = row_col_based(query, spreadsheet)
        case _:
            print(f"Unsupported strategy requested: {strategy}. Falling back to two_step_loose.")
            cells_identified = two_step_loose(query, spreadsheet)

    print(f"DEBUG: strategy completed, cells identified ----> {cells_identified}")
    for (curr_sheet_index, cells_to_highlight) in cells_identified:
        if cells_to_highlight:
            spreadsheet.highlight(curr_sheet_index, cells_to_highlight)

    save_highlighted_spreadsheet(spreadsheet, output_file_path)

def save_highlighted_spreadsheet(spreadsheet: Spreadsheet, output_file_path=None):
    if output_file_path:
        spreadsheet.save(output_file_path)
    else:
        new_filename = re.sub(r'(.+).xlsx$', r'\1_highlighted.xlsx', spreadsheet.original_filepath)
        spreadsheet.save(new_filename)

