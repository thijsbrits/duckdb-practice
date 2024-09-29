import csv


def load_csv_rows(filename: str):
    """Generator that yields rows from a CSV file as dictionaries."""
    with open(filename, 'r') as csv_file:

        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            yield row


def convert_empty_to_none(value):
    return None if value == '' else value


def create_placeholder_str(columns):
    """Dynamically create '?' placeholders for insertion queries
    Example: ?,?,? for columns ('a', 'b', 'c')"""
    return ', '.join(['?'] * len(columns))
