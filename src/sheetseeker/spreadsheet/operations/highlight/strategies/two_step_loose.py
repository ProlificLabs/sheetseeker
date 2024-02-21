import asyncio
from typing import List, Any, Tuple
from sheetseeker.llm import acall_openai, jinja_env
from sheetseeker.spreadsheet import Spreadsheet
from openpyxl.worksheet.worksheet import Worksheet
from .common import prep_data_from_worksheet, parse_llm_output_cell_ranges

FIRST_STEP_SYSTEM_TEMPLATE = "two_shot_first_sys_prompt_02.txt"
FIRST_STEP_USER_TEMPLATE = "two_shot_first_step_user_03.txt"
SECOND_STEP_SYSTEM_TEMPLATE = "two_shot_second_prompt_loose_03.txt"

def two_step_loose(query: str, spreadsheet: Spreadsheet) -> List[Tuple[int, List[str]|None]]:
    return asyncio.run(highlight_worksheets(query, spreadsheet))

async def atwo_step_loose(query: str, spreadsheet: Spreadsheet) -> List[Tuple[int, List[str]|None]]:
    return await highlight_worksheets(query, spreadsheet)

def generate_first_prompt(user_query: str, data: List[List[Any]]) -> str:
    system_template = jinja_env.get_template(FIRST_STEP_SYSTEM_TEMPLATE)
    user_template = jinja_env.get_template(FIRST_STEP_USER_TEMPLATE)

    return (system_template.render(data=data), user_template.render(user_query=user_query))

def generate_second_prompt(user_query: str, prev_response: str, data: List[List[Any]]) -> str:
    template = jinja_env.get_template(SECOND_STEP_SYSTEM_TEMPLATE)

    return template.render(user_query=user_query, prev_response=prev_response, data=data)

async def identify_cells_to_highlight(sheet: Worksheet, query: str) -> List[str]:
    prepped_data = prep_data_from_worksheet(sheet)
    (first_prompt, first_prompt_user) = generate_first_prompt(query, prepped_data)
    openai_response = await acall_openai(first_prompt, first_prompt_user)
    #print(f"DEBUG: assessment for query : {query} -------------> {openai_response}")

    second_prompt = generate_second_prompt(query, openai_response, prepped_data)
    #print(f"DEBUG: two_step_loose final query: {query} -------------> {second_prompt}")

    openai_response = await acall_openai(second_prompt, query)
    return parse_llm_output_cell_ranges(openai_response)

async def highlight_worksheets(query: str, spreadsheet: Spreadsheet):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for curr_sheet_idx, curr_sheet in enumerate(spreadsheet.sheets):
            tasks.append((curr_sheet_idx, tg.create_task(identify_cells_to_highlight(curr_sheet, query))))

    return list(map(lambda t: (t[0], t[1].result()), tasks))
