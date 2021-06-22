from snapflow_importers.base import Importer
from snapflow_importers.constants import AuthorizationChoices


class ShopifyOrdersImporter(Importer):
    SOURCE_NAME = 'shopify'
    SOURCE_TYPE = 'order'
    AUTHORIZATION_TYPE = AuthorizationChoices.BASIC_AUTH.value


class ShopifyCustomersImporter(ShopifyOrdersImporter):
    SOURCE_TYPE = 'customers'
