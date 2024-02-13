# Bank Statements to CSV Converter

## What is this?

The purpose of this project is to provide a tool to convert bank statements in PDF format into CSV (Comma-Separated
Values) files.

## Why?

Some bank's monthly statements only come in PDF format, which is cumbersome to work with when trying to extract
transaction data. Manually inputting transactions from a PDF into a spreadsheet like Excel or Google Sheets is *
*time-consuming and error-prone**. By converting the bank statement into CSV format, users can easily import the data
into spreadsheet software for further analysis or manipulation.

## Features

- Convert bank statements from PDF to CSV format
- Extract transaction data including date, description, amount, and other relevant information
- User-friendly interface
- Cross-platform compatibility

## Usage

To use this tool, follow these steps:

1. Clone the repository to your local machine:

   `git clone git@github.com:teo-jun-xiong/uob-statement-to-csv.git`
2. Install the necessary dependencies:

   `pip install -r requirements.txt`
3. Create a directory called `input` and copy your bank statements into it. This can be modified by updating `INPUT_DIR`
   in `convert.py`.
4. Run the conversion script: `python3 convert.py`.
5. The converted files will be created in `output/YYYMMDDTHHMMSS`. The output directory can be modified by
   updating `OUTPUT_DIR` in `convert.py`.

## Future enhancements

- [ ] Provide the option to convert all PDFs into a single CSV
- [ ] Improve compatibility with statements from different banks (only tested with UOB One)
- [ ] Automate update to Google Sheets