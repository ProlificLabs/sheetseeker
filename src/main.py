from highlighter import FinancialDataHighlighter
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--query', '-q', type=str, required=True, help="The data that should be highlighted.")
    parser.add_argument('--input-path', '-i', type=str, required=True, help="Path to the workbook containing the data.")
    parser.add_argument('--output-path', '-o', type=str, required=True, help="Path where the highlighted workbook should be saved.")
    return parser.parse_args()

def main():
    args = parse_args()
    analyst = FinancialDataHighlighter()
    analyst.analyze_workbook(args.query, args.input_path, args.output_path)


if __name__ == "__main__":
    main()