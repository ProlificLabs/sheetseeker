from typing import List

from constants import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from datatypes import MetricAnswer


def parse_llm_output(output: AIMessage) -> List[MetricAnswer]:
    result = []
    tool_calls = output.additional_kwargs.get("tool_calls", [])

    if not tool_calls:
        return result

    for tool_call in tool_calls:
        function_response = tool_call.get("function", {})
        if function_response.get("name") == "MetricAnswer":
            answer = MetricAnswer.parse_raw(function_response.get("arguments"))
            result.append(answer)

    return result


def llm_query(input_query: str, csv_data: str) -> List[MetricAnswer]:
    # Set up the OpenAI language model
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-1106", temperature=0)

    messages = [
            SystemMessage(
                          ),
            HumanMessage(csv_data),
            HumanMessage(input_query)
    ]

    llm = llm.bind_tools([MetricAnswer])

    res = llm.invoke(messages)
    return parse_llm_output(res) if isinstance(res, AIMessage) else []

