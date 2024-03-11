from constants import OPENAI_API_KEY, BASE_DIR
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.utils.function_calling import convert_to_openai_tool

from datatypes import MetricAnswer

os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = 'ls__92fed8feac1f436f8ee9a3aa6eae55af'


def parse_llm_output(output: AIMessage):
    tool_calls = output.additional_kwargs.get("tool_calls", [])
    if not tool_calls:
        return None

    function_response = tool_calls[0].get("function", {})
    if function_response.get("name") == "MetricAnswer":
        return MetricAnswer.parse_raw(function_response.get("arguments"))


def llm_query(input_query: str, csv_data: str):
    # Set up the OpenAI language model
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0)

    messages = [
            SystemMessage("You are a data analyst for a financial company. "
                          "You will be given the raw CSV data for the company's financial data. "
                          "Use only values from the provided CSV data to answer queries about key financial metrics. "
                          "Make sure you also note the specific CSV cells used to fulfill the query. "
                          "Assume that the CSV cells are labelled in the format 'A1', 'B2', etc. "),
            HumanMessage(csv_data),
            HumanMessage(input_query)
    ]

    llm = llm.bind_tools([convert_to_openai_tool(MetricAnswer)])

    res = llm.invoke(messages)
    return parse_llm_output(res) if isinstance(res, AIMessage) else None


if __name__ == "__main__":
    from parse_data import get_csv_data

    query = "What is the sum of revenues over the past 2 years?"
    csv_data = get_csv_data()
    metric_answer = llm_query(query, csv_data)

