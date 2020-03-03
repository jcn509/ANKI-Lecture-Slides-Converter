import csv
from anki_slides_converter import PDFToCardConverter, output_cards_to_csv_file

if __name__ == "__main__":
    import sys
    with open(sys.argv[2], "w") as file:
        csv_file = csv.writer(file)
        pdf_filename = sys.argv[1]
        pdf = PDFToCardConverter(pdf_filename)
        output_cards_to_csv_file(csv_file, pdf)
