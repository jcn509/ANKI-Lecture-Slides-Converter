import csv
from . import PDFDataExtractor


def _get_image_tag(image_filename: str) -> str:
    return "<img src='" + image_filename + "'>"


def output_cards_to_csv_file(csv_file, pdf: PDFDataExtractor) -> None:
    titles = pdf.get_page_titles()
    previous_title = titles[0]
    current_image_xml = ""
    for title_number, title in enumerate(titles):

        image_filename = pdf.get_image_filename(title_number)
        if title != previous_title:
            csv_file.writerow((previous_title, current_image_xml))
            current_image_xml = ""
        current_image_xml += _get_image_tag(image_filename)
        previous_title = title
    csv_file.writerow((previous_title, current_image_xml))
