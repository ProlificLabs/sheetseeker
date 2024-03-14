from typing import List
from config import CONFIG
from constants import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from datatypes import MetricAnswer


def parse_llm_output(output: AIMessage) -> List[MetricAnswer]:
    """
    Get the tool_calls parameter for the LLM output, and convert that to our recognized MetricAnswer model
    We passed the MetricAnswer model to the LLM, we assume the LLM will maintain our Pydantic model definition

    :param output: a list of MetricAnswer objects
    :return:
    """
    result = []
    tool_calls = output.additional_kwargs.get("tool_calls", [])

    if not tool_calls:
        return result

    for tool_call in tool_calls:
        function_response = tool_call.get("function", {})
        if function_response.get("name") == "MetricAnswer":
            # get the function-calling outputs, and use the structured data to generate MetricAnswer objects
            answer = MetricAnswer.parse_raw(function_response.get("arguments"))
            result.append(answer)

    return result


def llm_query(input_query: str, csv_data: str) -> List[MetricAnswer]:
    """
    Send the raw data + target metrics to an LLM, and get back recognizable MetricAnswer objects
    :param input_query:
    :param csv_data:
    :return:
    """

    # Set up the OpenAI language model
    system_prompt = CONFIG.get("system_prompt", "")
    openai_model = CONFIG.get("openai_model", "gpt-3.5-turbo-1106")

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=openai_model, temperature=0)
    messages = [
            SystemMessage(system_prompt),
            HumanMessage(csv_data),
            HumanMessage(input_query)
    ]

    # provide the MetricAnswer Pydantic model to OpenAI's LLM,
    # so that it returns function-calling outputs in our desired format
    # we're using the function-calling mechanism to return structured data
    llm = llm.bind_tools([MetricAnswer])

    res = llm.invoke(messages)

    return parse_llm_output(res) if isinstance(res, AIMessage) else []

