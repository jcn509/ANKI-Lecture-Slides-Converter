"""Provides the command line interface for ANKI Slides Converter"""

import csv
import argparse
from . import PDFToAnkiCardsConverter
from typing import List

def parse_arguments(args: List[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "Convert lecture slides to ANKI flascards")
    parser.add_argument('PDFs', type=str, nargs='+', help='PDF files or directories containing PDFs')
    parser.add_argument('output_file', type=str, help='Path to the output file')

    parser.add_argument("--skip-first", "-f", type=int, default = 0, help = "Skip the first n slides in each PDF")
    parser.add_argument("--skip-last", "-l", type=int, default = 0, help = "Skip the last n slides in each PDF")
    parser.add_argument("--title-lines", "-t", type = int, nargs="+", help="after converting a PDF to text which lines should you take to use as the title", default=(0)) 

    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_arguments()
    with open(args.output_file, "w") as file:
        csv_file = csv.writer(file)
        pdf_filename = args.PDFs[0]
        pdf = PDFToAnkiCardsConverter(pdf_filename)
        pdf.output_cards_to_csv_file(csv_file)
