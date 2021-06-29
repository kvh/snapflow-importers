from snapflow_squareup.connector import SquareUpPaymentsImporter
from snapflow_squareup.connector import SquareUpCustomersImporter
from snapflow_squareup.connector import SquareUpItemsImporter


def import_payments():
    importer = SquareUpPaymentsImporter()
    yield from importer.get_data()


def import_customers():
    importer = SquareUpCustomersImporter()
    yield from importer.get_data()


def import_items():
    importer = SquareUpItemsImporter()
    yield from importer.get_data()
