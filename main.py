import PyPDF2
import re
from transaction import Transaction

FOOTER_STRING = "Please note that youarebound byaduty under therules governing theoperation ofthisaccount"
BALANCE_STRING = "BALANCE B/F"


def clean_amount(text):
    return float(text.replace(',', ''))


def match_multi_line_transaction_start(text):
    pattern = r'(?i)((?:\d\d) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))(.*)'
    return re.match(pattern, text.strip())


def is_date(text):
    pattern = r'(?i)(\d\d) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(.*)'
    return re.match(pattern, text.strip())


def is_single_line_transaction(text):
    pattern = (r'(?i)((?:\d\d) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))(.*) (\d+,?\d+\.(?:\d+)) (\d+,'
               r'?\d+\.(?:\d+))')
    return re.match(pattern, text.strip())


def match_balance(text):
    pattern = r'(?i)(.*) (\d+,?\d+\.(?:\d+))'
    return re.match(pattern, text.strip())


def is_transaction_start(text):
    return BALANCE_STRING not in text


def clean_text(text):
    transaction_start = []
    lines = text.splitlines()
    transactions = []

    index = 0
    for i in range(len(lines)):
        if index >= i:
            continue

        if is_date(lines[i]) and is_transaction_start(lines[i]):
            transaction_start.append(i)

            match = is_single_line_transaction(lines[i])
            if match:
                transactions.append(Transaction(match.group(1), match.group(2), clean_amount(match.group(3)),
                                                clean_amount(match.group(4))))
            else:
                match = match_multi_line_transaction_start(lines[i])

                if not match:
                    continue

                date = match.group(1)
                description = match.group(2)
                balance = None

                index = i + 1
                while index < len(lines) and not is_date(lines[index]):
                    match = match_balance(lines[index])

                    if match:
                        description += match.group(1)
                        balance = clean_amount(match.group(2))
                    else:
                        description += lines[index]

                    index += 1

                index -= 1
                transactions.append(Transaction(date, description, None, balance))

    for i in range(1, len(transactions)):
        transactions[i].difference = round(transactions[i].balance - transactions[i - 1].balance, 2)

    return transactions


# Open the PDF file in binary mode
with open('example.pdf', 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)

    # Get the total number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    pages = []

    # Iterate through each page and extract text
    for page_number in range(1, num_pages - 1):
        # Get a specific page
        page = pdf_reader.pages[page_number]

        # Extract text from the page
        text = page.extract_text()
        pages.append(text)

    csv = [('Date', 'Description', 'Difference', 'Balance')]
    for i in range(len(pages)):
        transactions = clean_text(pages[i])
        csv += [transaction.to_tuple() for transaction in transactions]

    for c in csv:
        print(c)

    print(len(csv))
