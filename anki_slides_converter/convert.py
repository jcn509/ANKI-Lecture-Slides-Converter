import csv
from .lib import PDFDataExtractor, output_cards_to_csv_file

if __name__ == "__main__":
    import sys

    with open(sys.argv[2], "w") as file:
        csv_file = csv.writer(file)
        pdf_filename = sys.argv[1]
        pdf = PDFDataExtractor(pdf_filename)
        output_cards_to_csv_file(csv_file, pdf)
