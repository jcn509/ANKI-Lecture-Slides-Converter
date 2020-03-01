# ANKI lecture slides converter
A script that automatically converts lecture slides into ANKI flash cards. This script can extract the slide titles from lecture slides and use these as the "fronts" (title/questions) for the flash cards. It can also group together consecutive slides that that have the same title in to one card. 

## Advantages over [anki-slides-import](https://github.com/musically-ut/anki-slides-import)
 - Doesn't require you to store your notes in a text file marked with slide numbers
    - I prefer to take notes on paper and find it easier to copy them directly in to ANKI as it allows for bullet points, bolt text, underlining and other features not available in a text file
 - Automatically extracts flash card titles from slides
 - Can automatically group consecutive slides with the same title in to one card
 - Simple, cleaner and more reusable code

## Credits
Example lecture slides used in the tests were take from:
 - [MIT](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/lecture-slides-code/) 

## TO DO:
 - Automatic keyword extraction for the tags (to make it easier to search for cards)
 - Proper command line argument parsing
 - Either convert this script to an ANKI plugin or create a GUI
 - Documentation
 - Command line arguments
 - Allow slide cropping
 - Allow converting all PDFs in a directory

