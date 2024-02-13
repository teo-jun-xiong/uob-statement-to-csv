import PyPDF2
from transaction import Transaction
import util
import csv
import os

FOOTER_STRING = 'Please note that youarebound byaduty under therules governing theoperation ofthisaccount'
PARENT_DIR = './output/'


def clean_text(text):
    transaction_start = []
    lines = text.splitlines()
    transactions = []

    index = 0
    for i in range(len(lines)):
        if index >= i:
            continue

        if util.is_date(lines[i]) and util.is_transaction_start(lines[i]):
            transaction_start.append(i)

            match = util.is_single_line_transaction(lines[i])
            if match:
                transactions.append(
                    Transaction(match.group(1), match.group(2), util.clean_amount(match.group(3)),
                                util.clean_amount(match.group(4))))
            else:
                match = util.match_multi_line_transaction_start(lines[i])

                if not match:
                    continue

                date = match.group(1)
                description = match.group(2)
                balance = None

                index = i + 1
                while index < len(lines) and not util.is_date(lines[index]):
                    match = util.match_balance(lines[index])

                    if match:
                        description += match.group(1)
                        balance = util.clean_amount(match.group(2))
                    else:
                        description += lines[index]

                    index += 1

                index -= 1
                transactions.append(Transaction(date, description, None, balance))

    return transactions


def get_csv_name(file_name):
    return file_name.rsplit('.pdf', 1)[0] + '.csv'


def write_to_csv(file_path, data):
    file_name = os.path.basename(file_path)
    csv_file_name = get_csv_name(file_name)

    if not os.path.exists(PARENT_DIR):
        os.makedirs(PARENT_DIR)

    with open(PARENT_DIR + csv_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for tuple_item in data:
            csv_writer.writerow(tuple_item)


def convert_to_csv():
    with open('input/example.pdf', 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        rows = [('Date', 'Description', 'Difference', 'Balance')]
        transactions = []

        for page_number in range(1, num_pages - 1):
            page = pdf_reader.pages[page_number]
            text = page.extract_text()
            transactions += clean_text(text)

        for i in range(1, len(transactions)):
            transactions[i].difference = round(transactions[i].balance - transactions[i - 1].balance, 2)

        rows += [transaction.to_tuple() for transaction in transactions]
        write_to_csv('input/example.pdf', rows)


if __name__ == '__main__':
    convert_to_csv()
