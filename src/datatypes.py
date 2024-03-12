from typing import List

from langchain.pydantic_v1 import BaseModel, Field


class SpreadsheetCellLocation(BaseModel):
    sheet: str = Field(..., title="The exact name of the sheet")
    cell: str = Field(..., title="The specific cell in the CSV sheet")


class MetricAnswer(BaseModel):
    metric: str = Field(..., description="The metric to be calculated")
    value: str = Field(..., description="The final answer to the metric query")
    relevant_sheet: str = Field(..., description="The sheet used to answer/estimate the metric")
    relevant_cells: List[str] = Field(
        ..., description="The most relevant cell(s) used to answer/estimate the metric, in this format: A1, B2, etc.",

    )
