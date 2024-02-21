'''
This file runs evaluation tests of the various strategies implemented to carry
out the highlight operation. It loops over the example queries given in the
problem statement along with expected cells to be highlighted. It then runs the
strategy for each prompt, testing it's output against expectations. It grants a
score based on how many cells are covered, will full coverage given a score of
1 and less than one for any cells uncovered by the strategy output.
'''
import re
import string
import asyncio
from typing import List, Any, Tuple
from itertools import filterfalse

from sheetseeker.spreadsheet import Spreadsheet
from sheetseeker.spreadsheet.operations.highlight.strategies.one_shot_simple import aone_shot_simple
from sheetseeker.spreadsheet.operations.highlight.strategies.row_col_based import arow_col_based
from sheetseeker.spreadsheet.operations.highlight.strategies.one_shot_multistep import aone_shot_multistep
from sheetseeker.spreadsheet.operations.highlight.strategies.two_step_strict import atwo_step_strict
from sheetseeker.spreadsheet.operations.highlight.strategies.two_step_loose import atwo_step_loose

def eval_one_shot_simple():
    return asyncio.run(eval_strategy(aone_shot_simple))

def eval_row_col_based():
    return asyncio.run(eval_strategy(arow_col_based))

def eval_one_shot_multistep():
    return asyncio.run(eval_strategy(aone_shot_multistep))

def eval_two_step_strict():
    return asyncio.run(eval_strategy(atwo_step_strict))

def eval_two_step_loose():
    return asyncio.run(eval_strategy(atwo_step_loose))

async def eval_strategy(strategy):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for expectation in TEST_EXPECTATIONS:
            tasks.append(tg.create_task(run_test(expectation, strategy)))

    return list(map(lambda t: t.result(), tasks))

async def run_test(expectation, strategy_func):
    test_run_output = await strategy_func(expectation["prompt"], Spreadsheet(expectation["sheet"]))
    test_run_output = sorted(test_run_output)
    unmet_expectations = calculate_unmet_expectations(expectation["output"], test_run_output, expectation["prompt"])
    return unmet_expectations


def calculate_unmet_expectations(expected_output, test_run_output, prompt):
    output = []
    for (sheet_idx, expected_cells) in expected_output:
        curr_sheet_output_cells = test_run_output[sheet_idx][1]
        if not expected_cells:
            continue
        if not curr_sheet_output_cells:
            output.append(expected_cells)
            continue

        total_expected_in_group = sum(map(lambda c: cell_count(c), expected_cells))
        remainder = list(set(expected_cells) - set(curr_sheet_output_cells))

        # map not working here for some reason
        #cells_to_eliminate = flatten(list(set(map(lambda r: cells_in_range(r), remainder))))
        cells_to_eliminate = list(set(flatten([cells_in_range(r) for r in remainder])))
        unmatched_leftovers = list(filterfalse(lambda cell: is_in_any_range(curr_sheet_output_cells, cell), cells_to_eliminate))
        unmatched_leftovers_count = sum(map(lambda c: cell_count(c), unmatched_leftovers))
        group_score = (total_expected_in_group - unmatched_leftovers_count) / total_expected_in_group
        output.append( {
            "prompt": prompt,
            "score": group_score,
            "unmatched": unmatched_leftovers,
            "output": curr_sheet_output_cells})

    return output


TEST_EXPECTATIONS = [
    { "prompt": "Please highlight cells related to revenue",
        "output": [(0, ['B14:D14', 'B43:D43', 'B50:D50']), (1, None), (2, None)],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Cost of Goods Sold (COGS)",
        "output": [(0, ['B17:D17', 'B46:D46', 'B53:D53']), (1, None), (2, None)],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Operating Expenses",
        "output": [(0, ['A20', 'B21:D23', 'B24:D24']), (1, None), (2, None)],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Other Income/Expenses",
        "output": [(0, ['B27:D28']), (1, None), (2, ['B21:D21', 'B38:D38'])],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Interest Expense",
        "output": [(0, None), (1, None), (2, ['B55:D55'])],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Depreciation and Amortization",
        "output": [(0, ['A57:D57']), (1, None), (2, ['B19:D19'])],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Stock-Based Compensation",
        "output": [(0, ['A57:D57']), (1, None), (2, ['B19:D19'])],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Capital Expenditures",
        "output": [(0, None), (1, None), (2, ['A33:D33'])],
        "sheet": "data/sample_input.xlsx"},
    { "prompt": "Please identify data related to Gain/Loss on Assets",
        "output": [(0, None), (1, None), (2, None)],
        "sheet": "data/sample_input.xlsx"},
]

def cell_count(range_or_cell):
    split = range_or_cell.split(":")

    if len(split) == 1:
        return 1

    [left, right] = split

    (left_col, top_row) = breakdown_cell_coord(left)
    (right_col, bottom_row) = breakdown_cell_coord(right)

    num_cols = (ord(right_col) - ord(left_col)) + 1
    num_rows = (int(bottom_row) - int(top_row)) + 1

    return num_cols * num_rows

#cell_count("A15")
#cell_count("A1")
#cell_count("A1:A5")
#cell_count("B1:B5")
#cell_count("A1:B5")


def cells_in_range(range_or_cell):
    split = range_or_cell.split(":")

    if len(split) == 1:
        return split

    [left, right] = split

    (left_col, top_row) = breakdown_cell_coord(left)
    (right_col, bottom_row) = breakdown_cell_coord(right)

    alphabet = list(string.ascii_uppercase)
    letter_range = alphabet[alphabet.index(left_col):alphabet.index(right_col)+1]
    output = []
    for letter in letter_range:
        for rownum in range(int(top_row), int(bottom_row)+1):
            output.append(f"{letter}{rownum}")


    return output

#cells_in_range("A15") == ["A15"]
#cells_in_range("B15") == ["B15"]
#cells_in_range("A15:A16") == ["A15", "A16"]
#cells_in_range("A15:B15") == ["A15", "B15"]
#cells_in_range("A15:B15") == ["A15", "B15"]
#cells_in_range("A1:B2") == ["A1", "A2", "B1", "B2"]
#cells_in_range("A1:B22")



# TODO: need to update this to work with columns beyond Z
def is_cell_within_range(r: str, cell: str) -> bool:
    split = r.split(":")

    # r is not a range but a single cell
    if len(split) == 1:
        return r == cell

    [left, right] = split

    (cell_col, cell_row) = breakdown_cell_coord(cell)

    if left == right: # this indicates an entire row or column
        if left.isdigit() and cell_row == left:
            return True
        elif cell_col == left:
            return True
        else:
            return False

    (left_col, top_row) = breakdown_cell_coord(left)
    (right_col, bottom_row) = breakdown_cell_coord(right)

    if left_col <= cell_col and cell_col <= right_col and top_row <= cell_row and cell_row <= bottom_row:
        return True

    return False

#is_cell_within_range("A1", "A1") == True
#is_cell_within_range("G10", "G10") == True
#is_cell_within_range("A10:A15", "A9") == False
#is_cell_within_range("A10:A15", "A10") == True
#is_cell_within_range("A10:A15", "A14") == True
#is_cell_within_range("A10:A15", "A15") == True
#is_cell_within_range("A10:C15", "A10") == True
#is_cell_within_range("A10:C15", "B10") == True
#is_cell_within_range("A10:C15", "C10") == True
#is_cell_within_range("A10:C15", "B12") == True
#is_cell_within_range("A10:C15", "C15") == True
#is_cell_within_range("11:11", "A10") == False
#is_cell_within_range("1:1", "A1") == True
#is_cell_within_range("11:11", "A11") == True
#is_cell_within_range("11:11", "B11") == True
#is_cell_within_range("11:11", "D11") == True
#is_cell_within_range("A:A", "D11") == False
#is_cell_within_range("A:A", "A1") == True
#is_cell_within_range("A:A", "A4") == True
#is_cell_within_range("A:A", "A14") == True

# IN PROGRESS: now these need to handle entire row or column A:A and 15:15

def breakdown_cell_coord(cell_coord: str) -> Tuple[str, str]:
    ''' given a cell coordinate such as A15, return the column and row parts as a
    tuple ('A', '15')
    '''
    match = re.match(r'^([a-zA-Z]+)(\d+)', cell_coord)
    if match:
        return (match.group(1), match.group(2))

#breakdown_cell_coord("AA5")

def is_in_any_range(ranges: List[str], cell):
    for r in ranges:
        if is_cell_within_range(r, cell):
            return True

    return False


def flatten(xss):
    return [x for xs in xss for x in xs]

#is_cell_within_range("B14:D14", "G32") == False
#is_cell_within_range("B14:D14", "B14") == True
#is_cell_within_range("B14:D14", "C14") == True
#is_cell_within_range("B14:D14", "D14") == True
#is_cell_within_range("B14:D14", "C15") == False
#is_cell_within_range("B14:D14", "D15") == False
#is_cell_within_range("B14:D14", "A15") == False
#is_cell_within_range("B14:D14", "B13") == False
#is_cell_within_range("B14:D14", "B15") == False


