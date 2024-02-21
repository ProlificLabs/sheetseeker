import asyncio
from typing import List, Any, Tuple
from sheetseeker.llm import acall_openai, jinja_env
from sheetseeker.spreadsheet import Spreadsheet
from openpyxl.worksheet.worksheet import Worksheet
from .common import prep_data_from_worksheet, parse_llm_output_cell_ranges

SYSTEM_PROMPT_TEMPLATE = "highlight_cells_multistep_01.txt"

def one_shot_multistep(query: str, spreadsheet: Spreadsheet) -> List[Tuple[int, List[str]|None]]:
    return asyncio.run(highlight_worksheets(query, spreadsheet))

async def aone_shot_multistep(query: str, spreadsheet: Spreadsheet) -> List[Tuple[int, List[str]|None]]:
    return await highlight_worksheets(query, spreadsheet)

def generate_system_prompt(query: str, data: List[List[Any]]) -> str:
    template = jinja_env.get_template(SYSTEM_PROMPT_TEMPLATE)

    return template.render(user_query=query, data=data)

async def identify_cells_to_highlight(sheet: Worksheet, query: str) -> List[str]:
    system_prompt = generate_system_prompt(query, prep_data_from_worksheet(sheet))
    openai_response = await acall_openai(system_prompt, query)
    return parse_llm_output_cell_ranges(openai_response)

async def highlight_worksheets(query: str, spreadsheet: Spreadsheet):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for curr_sheet_idx, curr_sheet in enumerate(spreadsheet.sheets):
            tasks.append((curr_sheet_idx, tg.create_task(identify_cells_to_highlight(curr_sheet, query))))

    return list(map(lambda t: (t[0], t[1].result()), tasks))
