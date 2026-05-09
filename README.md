# CrosswordsScraper

A Python tool that scrapes Russian crossword puzzles from [absite.ru](https://absite.ru/crossw/) and exports them as printable HTML files.

## Features

- Downloads crossword images, clues, and answers from absite.ru
- Generates a clean, print-optimized HTML file for each crossword
- Supports both single crossword and range export

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line with one or two arguments.

### Single crossword

```bash
python absite_crossword_export.py <crossword_id>
```

Example — export crossword #5000:

```bash
python absite_crossword_export.py 5000
```

This creates `crossword_5000.html`.

### Range of crosswords

```bash
python absite_crossword_export.py <start_id> <end_id>
```

Example — export crosswords #5000 through #5099 (inclusive):

```bash
python absite_crossword_export.py 5000 5099
```

Each crossword is saved as a separate HTML file (e.g., `crossword_5000.html`, `crossword_5001.html`, …).

## Output

Each generated HTML file contains:

- The crossword grid image
- The list of clues (questions)
- The answers section

The HTML is styled for both screen viewing and A4 printing.
