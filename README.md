# SheetSeeker Challenge

## Introduction

Welcome to the SheetSeeker Challenge! This unique challenge is designed for AI engineer candidates applying to Pulley, focusing on the innovative task of extracting specific financial metrics from complex spreadsheets based on natural language instructions. This challenge tests your prowess in data manipulation, interpretation, and the application of AI technologies to solve real-world problems in the financial domain. Our assumption is that you'll likely use GPT-4 for this problem, but that's not a hard requirement. Please feel free to use whatever tools and technologies that you think will work best.

## Objective

The core objective of the SheetSeeker Challenge is to develop a system that can:

- Accurately read and interpret financial statements from Excel spreadsheets. The provided sample input file includes an income statement, balance sheet, and cash flow statement of ServiceNow Incorporated for the fiscal years 2021, 2022, and 2023.
- Understand and process natural language instructions to identify and extract key financial metrics such as revenue, operating expenses, and capital expenditures, among others.
- Produce a new copy of the Excel file that has all the correct cells highlighted, showcasing the ability to not only understand but also to visually present the data.

This solution should not be a one-off; it must be generalizable enough to adapt to different spreadsheets and varied sets of natural language instructions, showcasing the robustness and versatility of your approach.

## Challenge Data

You'll find a sample Excel file named `sample_input.xlsx` in the `/data` directory, serving as your playground for this challenge. This file is structured with three sheets, each representing a different aspect of ServiceNow Incorporated's financials over the last three years.

## Requirements

- Your solution may employ any programming language or technology stack of your choice, provided it can be easily set up and executed in a standard development environment.
- Dependencies must be clearly listed in a `requirements.txt` or `Pipfile` for Python-based solutions, or an equivalent for other languages.
- If your approach benefits from containerization, please include a `Dockerfile`.

## Time Allocation and Flexibility


There is no strict time limit for this challenge; you can take as much time as you need. This flexibility allows individuals unfamiliar with the tech stack to dedicate time to learning, or for those who wish, to elevate the challenge to the next level. As a baseline, we expect someone proficient in the stack to complete this challenge in approximately 3-5 hours. This estimate is provided to help you set your own expectations regarding the amount of time you may need to allocate to complete it.

## Submission Guidelines

- Zip File: Zip up the code directory and send it to us. Leaving the .git directory is preferred so we can see the history of how you implemented your solution. To automatically clean files that are not in git, you can use git clean -fdx (with appropriate caution as this deletes files). Please include your example output xlsx file in the zip.

## Evaluation Criteria

Your submission will be assessed based on:

- **Accuracy**: Precision in extracting and highlighting the requested financial metrics.
- **Generalizability**: Ability to apply the solution to different datasets and instructions effectively.
- **Code Quality**: Cleanliness, organization, and documentation of the codebase.
- **Performance**: Efficiency in processing, especially with larger datasets.
- **Innovation**: Creative and effective approaches to problem-solving and data interpretation.

## Task Instructions

Your system should be capable of understanding the following instructions to extract corresponding data for each available year:

- Revenue
- Cost of Goods Sold (COGS)
- Operating Expenses
- Other Income/Expenses
- Interest Expense
- Depreciation and Amortization
- Stock-Based Compensation
- Capital Expenditures
- Gain/Loss on Assets

These metrics should be highlighted in a new version of the spreadsheet, demonstrating your system's ability to accurately process and visualize financial data.

## License

This project is released under the MIT License. See the LICENSE file for full details.

---

We're looking forward to seeing how you tackle the SheetSeeker Challenge! Impress us with your ingenuity, technical skills, and your ability to turn complex data into clear insights. Good luck!
