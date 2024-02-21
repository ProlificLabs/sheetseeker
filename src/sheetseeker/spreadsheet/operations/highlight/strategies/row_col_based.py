import re
import asyncio
from typing import List, Any, Tuple
from sheetseeker.llm import acall_openai, jinja_env
from sheetseeker.spreadsheet import Spreadsheet
from openpyxl.worksheet.worksheet import Worksheet
from .common import prep_data_from_worksheet, parse_llm_output_cell_ranges

SYSTEM_PROMPT_TEMPLATE = "row_col_based_01.txt"


def row_col_based(query: str, spreadsheet: Spreadsheet) -> List[Tuple[int, List[str]|None]]:
    return asyncio.run(highlight_worksheets(query, spreadsheet))

async def arow_col_based(query: str, spreadsheet: Spreadsheet) -> List[Tuple[int, List[str]|None]]:
    return await highlight_worksheets(query, spreadsheet)

async def identify_cells_to_highlight(sheet: Worksheet, query: str) -> List[str]:
    system_prompt = generate_system_prompt(query, prep_data_from_worksheet(sheet))
    openai_response = await acall_openai(system_prompt, query)
    return parse_llm_rows_columns(openai_response)

def generate_system_prompt(query: str, data: List[List[Any]]) -> str:
    template = jinja_env.get_template(SYSTEM_PROMPT_TEMPLATE)

    return template.render(user_query=query, data=data)


async def highlight_worksheets(query: str, spreadsheet: Spreadsheet):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for curr_sheet_idx, curr_sheet in enumerate(spreadsheet.sheets):
            tasks.append((curr_sheet_idx, tg.create_task(identify_cells_to_highlight(curr_sheet, query))))

    return list(map(lambda t: (t[0], t[1].result()), tasks))

def parse_llm_rows_columns(openai_response: str):
    try:
        match = re.search('\\[(.+)\\]', openai_response)
        if match:
            openai_response = match.group(0)[1:-1] # strip out brackets
            return [convert_row_or_col_to_range(h.strip()) for h in openai_response.split(',')]

    except:
        raise AssertionError(f"Error, was unable to parse LLM output -> {openai_response}")


# TODO: make this work with columns beyond Z i.e. AA etc
def convert_row_or_col_to_range(row_or_col: str) -> str:
    m = re.match(r'^ROW(\d+)$', row_or_col)
    if m:
        return f"{m.group(1)}:{m.group(1)}"

    m = re.match(r'^[A-Z]', row_or_col)
    if m:
        return f"{row_or_col}:{row_or_col}"

    raise ValueError(f"There was an error, LM returned invalid row or column {row_or_col}")
