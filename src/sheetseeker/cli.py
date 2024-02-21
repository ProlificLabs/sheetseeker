import os
import sys
import argparse
from pathlib import Path
from sheetseeker.api import highlight_spreadsheet

def main():
    """
    call this with
    `poetry run sheetseeker "<your query>" <path/to/input_file.xlsx> [--output_file=<path/to/output_file.xlsx>] [--strategy=<strategy>]
    available strategies are:
        one_shot_simple
        row_col_based
        one_shot_multistep
        two_step_strict
        two_step_loose
    """
    parser = argparse.ArgumentParser(description="Arguments for sheetseeker cli")
    parser.add_argument('user_query', type=str, help="The user's query over the data.")
    parser.add_argument('input_file', type=str, help="The excel file to operate on")
    parser.add_argument('--output_file', type=str, required=False, help="Optional outfile path.")
    parser.add_argument('--strategy', type=str, required=False, help="The strategy to use to carry out the operation. Currently supported: two_step_loose(default), two_step_strict, one_shot_simple")
    args = parser.parse_args()
    user_query = args.user_query
    input_file = args.input_file
    output_file = args.output_file
    strategy = args.strategy

    highlight_spreadsheet(user_query, input_file, output_file_path=output_file, strategy=strategy)

def print_usage():
    print("USAGE:")
    print("sheetseeker <query over data> <path/to/input_spreadsheet.xlsx> [--output_file=output_spreadsheet] [--strategy=strategy]")

if __name__ == "__main__":
    main()
