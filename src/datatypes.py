from typing import List

from langchain.pydantic_v1 import BaseModel, Field


class SpreadsheetCellLocation(BaseModel):
    sheet: str = Field(..., title="The exact name of the sheet")
    cell: str = Field(..., title="The specific cell in the CSV sheet, in this format: A1, B2, etc.")


class MetricAnswer(BaseModel):
    metric: str = Field(..., title="The metric to be calculated")
    value: str = Field(..., title="The final answer to the metric query")
    relevant_cells: List[SpreadsheetCellLocation] = Field(
        ..., title="The cell(s) used to determine the metric"
    )
