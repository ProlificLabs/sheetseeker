# How to run
- Pull down the repo/changes
- cd into src/
- create a .env file with your OPENAI_API_KEY
- `make run-shell`
- from in the shell, `poetry run sheetseeker "<your query>" <path/to/input_spreadsheet.xlsx> [--output_file=outfile.xlsx] [--strategy=<strategy>]`

If no output file is given it will save using the same name (and location) as the inputfile with `_highlighted` appended to the end of it.

Note the project is mounted in src/ so won't have access to the outer data/ directory. Any files you'll want to access inside the container must be placed in src. Apologies for this limitation but I wrote this in a separate folder with the compose file at the top level.

Dependencies are listed in the pyproject.toml file

# How does it work

First, the spreadsheet is loaded using the [openpyxl](https://openpyxl.readthedocs.io/en/stable/index.html) library. Then it executes a strategy for highlighting the appropriate cells, calling openai and returning a set of cells and/or ranges to be highlighted. This list is processed, utilizing openpyxl again to apply some style to the cells in question. Finally, a copy of the spreadsheet is saved.

There are a number of strategies for determining which cells to highlight. The default is what I call "two step loose". It utilizes two calls to the language model. The first to get a general understanding of the subject matter and how to answer the user's request. The second call takes the output of that and asks specifically for the cells to be highlighted. This two step process worked better than a one shot.

## In detail

The spreadsheet is processed worksheet by worksheet, each one being separately passed asynchronously to the strategy which calls the language model.

The spreadsheet data is formatted to be printed into the prompt which is prepared using jinja. The prompt includes instructions which are strategy specific. Openai returns an output format that is easily parsed.

Lastly, the output from the strategy is passed back to openpyxl to highlight the requisite cells. Openpyxl understands the standard cell range format ("A15:B23" etc), and we then apply a foreground color to the cells.

## Limitations

There are some things I cut scope for:
- No retries on failure (network or parsing)
- Cannot handle arbitrary spreadsheet sizes
- Did not try to get it working with gpt 3.5
- Language model's nondeterministic nature results in inconsistent results
