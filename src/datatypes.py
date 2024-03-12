from typing import List
from langchain.pydantic_v1 import BaseModel, Field


class MetricAnswer(BaseModel):
    metric: str = Field(..., description="The metric to be calculated")
    # finding that adding the value improves LLM ability to get the right cells
    value: str = Field(..., description="The final answer to the metric query")
    # sheet and cells values returned by LLM used to highlight the cells in the spreadsheet
    relevant_sheet: str = Field(..., description="The sheet used to answer/estimate the metric")
    relevant_cells: List[str] = Field(
        ..., description="The most relevant cell(s) used to answer/estimate the metric, in this format: A1, B2, etc.",
    )
