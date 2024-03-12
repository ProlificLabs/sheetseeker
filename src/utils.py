import os
import ast
from typing import List
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from constants import INSTRUCTION

# Initialize OpenAI client with API key from environment variable
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def query_gpt(model: str = "gpt-4-turbo-preview", messages: List[dict] = [], json: bool = False) -> str:
    """
    Sends a query to the OpenAI GPT model and retrieves the response.

    Args:
        model (str): The identifier of the GPT model to be used. Defaults to 'gpt-4-turbo-preview'.
        messages (List[dict]): A list of message dictionaries for the conversation with the GPT model.

    Returns:
        str: The trimmed content of the message from the GPT model.

    Raises:
        OpenAIError: If an error occurs during the API call to OpenAI.
    """
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={ "type": "json_object" if json else "text"} ,
    )
    return response.choices[0].message.content.strip()

@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=60))
def get_relevant_rows(first_col: List[str], query: str) -> List[str]:
    """
    Retrieves a list of relevant rows from a financial spreadsheet based on a user query.
    Retries if the output format is not a list.

    Args:
        first_col (List[str]): The first column of the spreadsheet, containing row labels.
        query (str): The user's query specifying the information sought.

    Returns:
        List[str]: A list of strings representing the relevant rows in the spreadsheet.

    Raises:
        ValueError: If the response from the GPT model cannot be converted into a list.
    """
    instruction = INSTRUCTION.format(first_col=first_col, query=query)
    system_message = "You are a helpful financial assistant that can identify the most relevant financial terms based on the query that the user inputs.\n\nRespond only with a list of strings."
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": instruction}]

    rows = query_gpt(messages=messages)
    try:
        rows = ast.literal_eval(rows)
        if not isinstance(rows, list):
            raise ValueError
    except Exception:
        fix_list_message = [
            {"role": "system", "content": "Convert the following to a JSON list"},
            {"role": "user", "content": rows}
        ]

        # Use JSON Mode to convert the response to a list
        rows = query_gpt(messages=fix_list_message, json=True)
        # Get values from rows dictionary
        rows = ast.literal_eval(rows)
        # Flatten list of lists
        rows = [item for sublist in rows.values() for item in sublist]
        if not isinstance(rows, list):
            raise ValueError("The response from GPT could not be converted into a list.")
    return rows
