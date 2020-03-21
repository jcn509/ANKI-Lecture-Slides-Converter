import os
import csv
import multiprocessing
import pdf2image

# For some reason pytype doesn't like pdftotext
import pdftotext  # type: ignore
from typing import Tuple, List


def _get_image_tag(image_filename: str) -> str:
    return "<img src='" + image_filename + "'>"

class PDFToAnkiCardsConverter:
    def __init__(self, pdf_file_path: str, skip_first: int = 0, skip_last: int = 0, password: str = ""):
        self._pdf_file_path = pdf_file_path
        self._skip_first = skip_first
        self._skip_last = skip_last
        self._password = password
    
    def get_image_filename(self, page_index: int) -> str:
        return (
            self._pdf_file_path.replace(os.sep, "_").strip(".")
            + "_page_"
            + str(page_index + self._skip_first + 1)
            + ".jpg"
        )

    def output_images_to_directory(self, output_directory: str, dpi: int = 200, thread_count: int = multiprocessing.cpu_count()) -> None:
        skip_last = None if self._skip_last == 0 else self._skip_last
        page_count = pdf2image.pdfinfo_from_path(self._pdf_file_path, userpw = self._password)["Pages"]
        first_page = self._skip_first
        last_page = page_count - skip_last
        images = pdf2image.convert_from_path(self._pdf_file_path, dpi = dpi, first_page = first_page, last_page = last_page, thread_count = thread_count, userpw = self._password)
        for image_number, image in enumerate(images):
            image.save(
                os.path.join(output_directory, self.get_image_filename(image_number))
            )

    def output_cards_to_csv_file(self, csv_file) -> None:
        titles = self.get_page_titles()
        previous_title = titles[0]
        current_image_xml = ""
        num_titles = len(titles)
        for title_number, title in enumerate(titles):

            image_filename = self.get_image_filename(title_number)
            if title != previous_title or title_number == num_titles:
                csv_file.writerow((previous_title, current_image_xml))
                current_image_xml = ""
            current_image_xml += _get_image_tag(image_filename)
            previous_title = title
        csv_file.writerow((previous_title, current_image_xml))

    def get_page_titles(
        self, get_title_from_lines: Tuple[int] = (0,), line_seperator: str = "\n"
    ) -> List[str]:
        titles = []
        with open(self._pdf_file_path, "rb") as f:
            pdf = pdftotext.PDF(f, self._password)

            # Slicing not supported here
            for page in range(self._skip_first, len(pdf) - self._skip_last):
                lines = pdf[page].split("\n")
                titles.append(
                    line_seperator.join((lines[line] for line in get_title_from_lines)).strip()
                )

        return titles
