# Sheetseeker Solution

This folder contains my submission to the Sheetseeker challenge.
Refer to `README.ipynb` for an interactive README and a basic evaluation framework.

## Installation

In your favorite Python environment manager:
`pip install -r requirements.txt`

## Basic Usage

You can invoke `main.py` as such
`python main.py -q {query} -i {input xlsx file} -o {output xlsx file}`

Or you can use programmatically as below:
```python
from highlighter import FinancialDataHighlighter

input_book = '../data/sample_input.xlsx'
output_book = '../data/sample_input_revenue.xlsx'
query = "Revenue"

analyst = FinancialDataHighlighter()
analyst.analyze_workbook(query, input_book, output_book)
```

## Future ideas

* add in context examples
* Fix observed issues:
    * column index consistency seems to be off, examples might help, different labeling strategies might help
* Test with different financial statement document formats beyond the example data
* Maybe do a second pass asking the LLM if the extracted cells are actually relevant
* If first pass does not highlight any data, do a 2 pass approach where you generate potential synonyms or relevant data types on the first pass and try to highlight those. (depends on precision/recall requirements of the product in question) 
* try a multi model approach, sending easier queries to gpt-3.5 (depends if model call optimizations are needed in a production scenario)