"""Provides the command line interface for ANKI Slides Converter"""

import os
from glob import glob
import csv
import argparse
from anki_slides_converter import PDFToAnkiCardsConverter
from typing import List

def parse_arguments(args: List[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "Convert lecture slides to ANKI flashcards")
    parser.add_argument('PDFs', type=str, nargs='+', help='PDF files or directories containing PDFs')
    parser.add_argument('output_csv_file', type=str, help='Path to the output file')
    parser.add_argument('output_image_directory', type=str, help='The directory in which the generated images should be placed')
    parser.add_argument("--verbose", "-v", default = False, action='store_true', help = "Print out all the pdf titles and slide titles")
    parser.add_argument("--practice-run", "-p", default = False, action='store_true', help = "Don't output images or a csv file - just print out all the pdf titles and slide titles")
    parser.add_argument("--skip-first", "-f", type=int, default = 0, help = "Skip the first n slides in each PDF")
    parser.add_argument("--skip-last", "-l", type=int, default = 0, help = "Skip the last n slides in each PDF")
    parser.add_argument("--title-lines", "-t", type = int, nargs="+", help="after converting a PDF to text which lines should you take to use as the title", default=(0,)) 
    parser.add_argument("--password", "-w", type =str, default = "", help = "The PDF password")
    parser.add_argument("--keep-csv-contents", "-e", default = False, action='store_true', help = "If the CSV file already exists append to it rather than overwrite it")
    parser.add_argument("--dont-merge-consecutive-cards-with-same-title", "-d", default = False, action='store_true', help = "If 2 or more consecutive cards have the same title don't merge them")

    return parser.parse_args(args)

def get_pdf_file_paths(pdfs_and_directories):
    pdf_file_paths = []
    for file_or_dir in pdfs_and_directories:
        if os.path.isfile(file_or_dir):
            pdf_file_paths.append(file_or_dir)
        elif os.path.isdir(file_or_dir):
            pdf_file_paths += glob(file_or_dir + "*.pdf") 
    return pdf_file_paths

def main():
    args = parse_arguments()
    print(args)
    csv_open_mode = "w"
    if args.keep_csv_contents:
        csv_open_mode = "a+"
    with open(args.output_csv_file, csv_open_mode) as file: 
        csv_file = csv.writer(file)
        for pdf_file_path in get_pdf_file_paths(args.PDFs):
            pdf = PDFToAnkiCardsConverter(pdf_file_path, skip_first = args.skip_first, merge_consecutive_cards_with_same_title = not args.dont_merge_consecutive_cards_with_same_title, skip_last = args.skip_last, password = args.password, get_title_from_lines = args.title_lines)
            if args.verbose or args.practice_run:
                print("File: " + pdf_file_path)
                print("\n\n".join(pdf.get_page_titles()))
            if not args.practice_run:    
                pdf.output_cards_to_csv_file(csv_file)
                pdf.output_images_to_directory(args.output_image_directory)

if __name__ == "__main__":
    main()
