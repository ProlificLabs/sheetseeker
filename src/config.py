# single centralized file where all the modifiable parameters are stored

CONFIG = {
    "input_file_name": "sample_input.xlsx",
    "openai_model": "gpt-3.5-turbo-1106",
    "system_prompt": "You are a data analyst for a financial company. "
                     "You will be given the raw CSV data for the company's financial data. "
                     "Use the provided CSV data to answer queries, to the best of your ability, about key financial metrics. "
                     "Make sure you note the most relevant CSV cells used to answer the query. "
                     "Assume that the CSV cells are labelled in the format 'A1', 'B2', etc. ",
    "query": "For every year available, what is the:\n"
             "- Revenue\n"
             "- Cost of Goods Sold (COGS)\n"
             "- Operating Expenses\n"
             "- Other Income/Expenses\n"
             "- Interest Expense\n"
             "- Depreciation and Amortization\n"
             "- Stock-Based Compensation\n"
             "- Capital Expenditures\n"
             "- Gain/Loss on Assets\n"
}
