import re

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
    pattern = (r'(?i)((?:\d\d) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))(.*) (\d+,?(?:\d+)?\.(?:\d+)) ('
               r'\d+,?(?:\d+)?\.(?:\d+))')
    return re.match(pattern, text.strip())


def match_balance(text):
    pattern = r'(?i)(.*) (\d+,?(?:\d+)?\.(?:\d+))'
    return re.match(pattern, text.strip())


def is_transaction_start(text):
    return BALANCE_STRING not in text
