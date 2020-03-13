import pytest
from ..lib import output_cards_to_csv_file


@pytest.mark.parametrize(
    "image_filenames,page_titles,expected_result",
    [(["img1.jpg"], ["test"], [("test", "<img src='img1.jpg'>")])],
)
def test_output_cards_csv_file(mocker, image_filenames, page_titles, expected_result):
    pdf = mocker.MagicMock()
    pdf.get_page_titles = mocker.MagicMock(return_value=page_titles)
    pdf.get_image_filename = mocker.MagicMock(side_effect=image_filenames)
    pdf.convert_pdf_to_images = mocker.MagicMock()

    csv_writer = mocker.MagicMock()
    csv_writer.writerow = mocker.MagicMock()
    output_cards_to_csv_file(csv_writer, pdf)

    calls = [mocker.call(x) for x in expected_result]
    csv_writer.writerow.assert_has_calls(calls, any_order=True)
