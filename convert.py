import csv
import os
from datetime import datetime

import PyPDF2

import util
from logger import log
from transaction import Transaction

FOOTER_STRING = 'Please note that youarebound byaduty under therules governing theoperation ofthisaccount'
INPUT_DIR = './input'
OUTPUT_DIR = './output'


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


def write_to_csv(file_path, datetime_string, data):
    file_name = os.path.basename(file_path)
    csv_file_name = get_csv_name(file_name)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(os.path.join(OUTPUT_DIR, datetime_string)):
        os.makedirs((os.path.join(OUTPUT_DIR, datetime_string)))

    with open(os.path.join(OUTPUT_DIR, datetime_string, csv_file_name), 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for tuple_item in data:
            csv_writer.writerow(tuple_item)


def convert_to_csv():
    datetime_string = datetime.now().strftime("%Y%m%dT%H%M%S")

    pdf_files = [file for file in os.listdir(INPUT_DIR) if file.endswith('.pdf')]

    for pdf in pdf_files:
        try:
            log.info("Converting %s to .csv" % pdf)
            with open(os.path.join(INPUT_DIR, pdf), 'rb') as file:
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
                write_to_csv(pdf, datetime_string, rows)
                log.info("Converted %s to .csv" % pdf)
        except Exception as e:
            log.error("Failed to convert %s to .csv" % pdf, e)


if __name__ == '__main__':
    convert_to_csv()
