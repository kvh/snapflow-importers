from snapflow_shopify.connector import ShopifyOrdersImporter


def import_orders():
    # This is a very simple implementation of a
    # Shopify importer
    importer = ShopifyOrdersImporter()
    yield from importer.get_data()
