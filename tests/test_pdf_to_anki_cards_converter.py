import pytest
import os
from anki_slides_converter import PDFToAnkiCardsConverter

TEST_LECTURE_SLIDES_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_slides"
)
LECTURE1 = os.path.join(TEST_LECTURE_SLIDES_DIRECTORY, "MIT6_0001F16_Lec1.pdf")

@pytest.mark.parametrize(
    "pdf_filename,get_title_from_lines,line_seperator,skip_first,skip_last,expected_result",
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
                "ASPECTS OF LANGUAGES\nsyntactically correct string of symbols with no static"
            ],
        ),
    ],
)
def test_get_page_titles(
    pdf_filename, get_title_from_lines, line_seperator, skip_first, skip_last, expected_result
):
    pdf = PDFToAnkiCardsConverter(pdf_filename, skip_first=skip_first, skip_last=skip_last, get_title_from_lines=get_title_from_lines, title_line_seperator=line_seperator)
    result = pdf.get_page_titles()
    assert result == expected_result

# Don't care about should_merge_consecutive_cards_with_same_title
_parameters_for_output_cards_to_csv_file = [
    pytest.param(
        ["img1.jpg"], 
        ["test"], 
        [("test", "<img src='img1.jpg'>")],
        id="one image one title -> one card"
    ),
    pytest.param(
        ["blah.jpg", "test.jpg"], 
        ["title1", "title2"],
        [
            ("title1", "<img src='blah.jpg'>"),
            ("title2", "<img src='test.jpg'>")
        ],
        id="Different titles -> different cards"
    ),
    pytest.param(
        ["blah.jpg", "test.jpg", "test2.jpg", "test3.jpg"], 
        ["title1", "title2", "title3", "title2"],
        [
            ("title1", "<img src='blah.jpg'>"),
            ("title2", "<img src='test.jpg'>"),
            ("title3", "<img src='test2.jpg'>"),
            ("title2", "<img src='test3.jpg'>")
        ],
        id="Same title appears twice but not consecutively -> different cards"
    )
]

parameters_for_output_cards_to_csv_file_merge_consecutive_cards_with_same_title = _parameters_for_output_cards_to_csv_file + [
    pytest.param(
        ["blah.jpg", "test.jpg", "test2.jpg"], 
        ["title1", "title2", "title2"],
        [
            ("title1", "<img src='blah.jpg'>"),
            ("title2", "<img src='test.jpg'><img src='test2.jpg'>")
        ],
        id="Same title twice in a row -> both images on one card"
    ),
    pytest.param(
        ["blah.jpg", "test.jpg", "test2.jpg", "x.jpg", "y.jpg"], 
        ["title1", "title2", "title2", "title2", "last"],
        [
            ("title1", "<img src='blah.jpg'>"),
            ("title2", "<img src='test.jpg'><img src='test2.jpg'><img src='x.jpg'>"),
            ("last", "<img src='y.jpg'>")
        ],
        id="Same title three times in a row -> all three images on one card"
    )

]


parameters_for_output_cards_to_csv_file_dont_merge_consecutive_cards_with_same_title = _parameters_for_output_cards_to_csv_file + [
    pytest.param(
        ["blah.jpg", "test.jpg", "test2.jpg"], 
        ["title1", "title2", "title2"],
        [
            ("title1", "<img src='blah.jpg'>"),
            ("title2", "<img src='test.jpg'>"),
            ("title2", "<img src='test2.jpg'>")
        ],
        id="Same title twice in a row -> two separate cards"
    )
]

def _test_output_cards_csv_file(mocker, merge_consecutive_cards_with_same_title, image_filenames, page_titles, expected_result):
    """Just a helper function"""
    pdf = PDFToAnkiCardsConverter("", merge_consecutive_cards_with_same_title = merge_consecutive_cards_with_same_title)
    pdf.get_page_titles = mocker.MagicMock(return_value=page_titles)
    pdf.get_image_filename = mocker.MagicMock(side_effect=image_filenames)
    pdf.convert_pdf_to_images = mocker.MagicMock()

    csv_writer = mocker.MagicMock()
    csv_writer.writerow = mocker.MagicMock()
    pdf.output_cards_to_csv_file(csv_writer)
    calls = [mocker.call(x) for x in expected_result]
    csv_writer.writerow.assert_has_calls(calls, any_order=True)


@pytest.mark.parametrize(
    "image_filenames,page_titles,expected_result",
    parameters_for_output_cards_to_csv_file_merge_consecutive_cards_with_same_title
)
def test_output_cards_to_csv_merge_consecutive_cards_with_same_title(mocker, image_filenames, page_titles, expected_result):
    _test_output_cards_csv_file(mocker, True, image_filenames, page_titles, expected_result)

@pytest.mark.parametrize(
    "image_filenames,page_titles,expected_result",
    parameters_for_output_cards_to_csv_file_dont_merge_consecutive_cards_with_same_title
)
def test_output_cards_to_csv_dont_merge_consecutive_cards_with_same_title(mocker, image_filenames, page_titles, expected_result):
    _test_output_cards_csv_file(mocker, False, image_filenames, page_titles, expected_result)

