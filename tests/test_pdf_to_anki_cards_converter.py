import pytest
import os
from anki_slides_converter import PDFToAnkiCardsConverter

TEST_LECTURE_SLIDES_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_slides"
)
LECTURE1 = os.path.join(TEST_LECTURE_SLIDES_DIRECTORY, "MIT6_0001F16_Lec1.pdf")

@pytest.mark.parametrize(
    "pdf_filename,line_numbers,line_seperator,skip_first,skip_last,expected_result",
    [
        (
            LECTURE1,
            [0],
            "\n",
            0,
            0,
            [
                "WELCOME!",
                "TODAY",
                "COURSE INFO",
                "COURSE POLICIES",
                "RECITATIONS",
                "FAST PACED COURSE",
                "PROBLEM",
                "TOPICS",
                "WHAT DOES A COMPUTER DO",
                "TYPES OF KNOWLEDGE",
                "A NUMERICAL EXAMPLE",
                "WHAT IS A RECIPE",
                "COMPUTERS ARE MACHINES",
                "BASIC MACHINE ARCHITECTURE",
                "STORED PROGRAM COMPUTER",
                "BASIC PRIMITIVES",
                "CREATING RECIPES",
                "ASPECTS OF LANGUAGES",
                "ASPECTS OF LANGUAGES",
                "ASPECTS OF LANGUAGES",
                "ASPECTS OF LANGUAGES",
                "WHERE THINGS GO WRONG",
                "PYTHON PROGRAMS",
                "OBJECTS",
                "SCALAR OBJECTS",
                "TYPE CONVERSIONS (CAST)",
                "PRINTING TO CONSOLE",
                "EXPRESSIONS",
                "OPERATORS ON ints and floats",
                "SIMPLE OPERATIONS",
                "BINDING VARIABLES AND",
                "ABSTRACTING EXPRESSIONS",
                "PROGRAMMING vs MATH",
                "CHANGING BINDINGS",
                "MIT OpenCourseWare",
            ],
        ),
        (
            LECTURE1,
            [0],
            "\n",
            20,
            0,
            [
                "ASPECTS OF LANGUAGES",
                "WHERE THINGS GO WRONG",
                "PYTHON PROGRAMS",
                "OBJECTS",
                "SCALAR OBJECTS",
                "TYPE CONVERSIONS (CAST)",
                "PRINTING TO CONSOLE",
                "EXPRESSIONS",
                "OPERATORS ON ints and floats",
                "SIMPLE OPERATIONS",
                "BINDING VARIABLES AND",
                "ABSTRACTING EXPRESSIONS",
                "PROGRAMMING vs MATH",
                "CHANGING BINDINGS",
                "MIT OpenCourseWare",
            ],
        ),
        (
            LECTURE1,
            [0],
            "\n",
            20,
            13,
            ["ASPECTS OF LANGUAGES", "WHERE THINGS GO WRONG"],
        ),
        (LECTURE1, [0], "\n", 20, 14, ["ASPECTS OF LANGUAGES"]),
        (
            LECTURE1,
            [0, 1],
            "\n",
            20,
            14,
            ["ASPECTS OF LANGUAGES\n\uf0a7 semantics is the meaning associated with a"],
        ),
        (
            LECTURE1,
            [0, 2],
            "\n",
            20,
            14,
            [
                "ASPECTS OF LANGUAGES\n syntactically correct string of symbols with no static"
            ],
        ),
    ],
)
def test_get_page_titles(
    pdf_filename, line_numbers, line_seperator, skip_first, skip_last, expected_result
):
    pdf = PDFToAnkiCardsConverter(pdf_filename, skip_first=skip_first, skip_last=skip_last)
    result = pdf.get_page_titles(line_numbers, line_seperator)
    assert result == expected_result

@pytest.mark.parametrize(
    "image_filenames,page_titles,expected_result",
    [(["img1.jpg"], ["test"], [("test", "<img src='img1.jpg'>")])],
)
def test_output_cards_csv_file(mocker, image_filenames, page_titles, expected_result):
    pdf = PDFToAnkiCardsConverter("")
    pdf.get_page_titles = mocker.MagicMock(return_value=page_titles)
    pdf.get_image_filename = mocker.MagicMock(side_effect=image_filenames)
    pdf.convert_pdf_to_images = mocker.MagicMock()

    csv_writer = mocker.MagicMock()
    csv_writer.writerow = mocker.MagicMock()
    pdf.output_cards_to_csv_file(csv_writer)
    calls = [mocker.call(x) for x in expected_result]
    csv_writer.writerow.assert_has_calls(calls, any_order=True)
