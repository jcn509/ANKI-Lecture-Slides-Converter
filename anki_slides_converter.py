import pdf2image
import os
import csv
import pdftotext
from typing import Tuple, List, Iterable

class PDFToCardConverter:
    def __init__(self, pdf_filename: str, skip_first: int = 0, skip_last: int = 0):
        self._pdf_filename = pdf_filename
        self._skip_first = skip_first
        self._skip_last = skip_last

    def get_image_filename(self, page_number:int) -> str:
        return self._pdf_filename.split(os.sep)[-1] + "_page_" + str(page_number + self._skip_first + 1) + ".jpg"

    def convert_pdf_to_images(self, output_directory: str) -> None:
        skip_last = None if self._skip_last == 0 else - self._skip_last
        images = pdf2image.convert_from_path(self._pdf_filename)
        for image_number, image in enumerate(images[self._skip_first: -skip_last]):
            image.save(os.path.join(output_directory, self.get_image_filename(image_number)))

    def get_card_titles(self, line_numbers: Tuple[int]= (0,), line_seperator: str = "\n") -> List[str]:
        titles = []
        with open(self._pdf_filename, "rb") as f:
            pdf = pdftotext.PDF(f)

            # Slicing not supported here
            for page in range(self._skip_first, len(pdf) - self._skip_last):
                lines = pdf[page].split("\n")
                titles.append(
                    line_seperator.join((lines[line] for line in line_numbers)).strip())
                
        return titles

def _get_image_tag(image_filename: str) -> str:
    return "<img src='" + image_filename + "'>"


def output_cards_to_csv_file(csv_file: csv.writer, pdf: PDFToCardConverter) -> None:
    titles = pdf.get_card_titles()
    previous_title = titles[0]
    current_image_xml = ""
    for title_number, title in enumerate(titles):
        
        image_filename = pdf.get_image_filename(title_number) 
        if title != previous_title:
            csv_file.writerow((previous_title, current_image_xml))
            current_image_xml = ""
        current_image_xml += _get_image_tag(image_filename) 
        previous_title = title
    csv_file.writerow((title, current_image_xml))

if __name__ == "__main__":
    import sys
    with open(sys.argv[2], "w") as file:
        csv_file = csv.writer(file)
        pdf_filename = sys.argv[1]
        pdf = PDFToCardConverter(pdf_filename)
        output_cards_to_csv_file(csv_file, pdf)
