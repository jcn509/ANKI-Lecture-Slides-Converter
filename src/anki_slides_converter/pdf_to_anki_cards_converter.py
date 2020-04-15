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
    def __init__(
        self,
        pdf_file_path: str,
        skip_first: int = 0,
        skip_last: int = 0,
        merge_consecutive_cards_with_same_title: bool = True,
        password: str = "",
        get_title_from_lines: Tuple[int] = (0,),
        title_line_seperator: str = "\n",
    ):
        self._pdf_file_path = pdf_file_path
        self._skip_first = skip_first
        self._skip_last = skip_last
        self._merge_consecutive_cards_with_same_title = (
            merge_consecutive_cards_with_same_title
        )
        self._password = password
        self._get_title_from_lines = get_title_from_lines
        self._title_line_seperator = title_line_seperator
        self._titles = None  # type: List[str]

    def get_image_filename(self, page_index: int) -> str:
        return (
            self._pdf_file_path.replace(os.sep, "_").replace(".", "_")
            + "_page_"
            + str(page_index + self._skip_first + 1)
            + ".jpg"
        )

    def output_images_to_directory(
        self,
        output_directory: str,
        dpi: int = 200,
        thread_count: int = multiprocessing.cpu_count(),
    ) -> None:
        page_count = pdf2image.pdfinfo_from_path(
            self._pdf_file_path, userpw=self._password
        )["Pages"]
        first_page = self._skip_first
        last_page = page_count - self._skip_last
        images = pdf2image.convert_from_path(
            self._pdf_file_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page,
            thread_count=thread_count,
            userpw=self._password,
        )
        for image_number, image in enumerate(images):
            image.save(
                os.path.join(output_directory, self.get_image_filename(image_number))
            )

    def _get_title_for_page(self, pdf_page: str) -> str:
        lines_of_page = pdf_page.split("\n")
        lines_for_title = (
            lines_of_page[line].strip() for line in self._get_title_from_lines
        )
        return self._title_line_seperator.join(lines_for_title)

    def get_page_titles(self) -> List[str]:
        if self._titles is None:
            self._titles = []
            with open(self._pdf_file_path, "rb") as f:
                pdf = pdftotext.PDF(f, self._password)

                # Slicing not supported here
                for page in range(self._skip_first, len(pdf) - self._skip_last):
                    title = self._get_title_for_page(pdf[page])
                    self._titles.append(title)

        return self._titles

    def _should_merge_cards(self, card_title_1: str, card_title_2: str) -> bool:
        return (
            self._merge_consecutive_cards_with_same_title
            and card_title_1 == card_title_2
        )

    def output_cards_to_csv_file(self, csv_file) -> None:
        titles = self.get_page_titles()
        previous_title = titles[0]
        current_image_xml = ""
        num_titles = len(titles)
        for title_number, title in enumerate(titles):

            image_filename = self.get_image_filename(title_number)
            is_last_card = title_number == num_titles
            if is_last_card or not self._should_merge_cards(title, previous_title):
                # Note: writing previous card here
                csv_file.writerow((previous_title, current_image_xml))
                current_image_xml = ""
            current_image_xml += _get_image_tag(image_filename)
            previous_title = title
        csv_file.writerow((title, current_image_xml))
