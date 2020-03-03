import pdf2image
import os
import pdftotext
from typing import Tuple, List

class PDFDataExtractor:
    def __init__(self, pdf_filename: str, skip_first: int = 0, skip_last: int = 0):
        self._pdf_filename = pdf_filename
        self._skip_first = skip_first
        self._skip_last = skip_last

    def get_image_filename(self, page_index:int) -> str:
        return self._pdf_filename.split(os.sep)[-1] + "_page_" + str(page_index + self._skip_first + 1) + ".jpg"

    def convert_pdf_to_images(self, output_directory: str) -> None:
        skip_last = None if self._skip_last == 0 else - self._skip_last
        images = pdf2image.convert_from_path(self._pdf_filename)
        for image_number, image in enumerate(images[self._skip_first: -skip_last]):
            image.save(os.path.join(output_directory, self.get_image_filename(image_number)))

    def get_page_titles(self, line_numbers: Tuple[int]= (0,), line_seperator: str = "\n") -> List[str]:
        titles = []
        with open(self._pdf_filename, "rb") as f:
            pdf = pdftotext.PDF(f)

            # Slicing not supported here
            for page in range(self._skip_first, len(pdf) - self._skip_last):
                lines = pdf[page].split("\n")
                titles.append(
                    line_seperator.join((lines[line] for line in line_numbers)).strip())
                
        return titles

