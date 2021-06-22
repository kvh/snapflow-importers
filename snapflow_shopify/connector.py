from snapflow_importers.base import Importer
from snapflow_importers.constants import AuthorizationChoices


class ShopifyOrdersImporter(Importer):
    SOURCE_NAME = 'shopify'
    SOURCE_TYPE = 'orders'
    AUTHORIZATION_TYPE = AuthorizationChoices.BASIC_AUTH.value

    def base_api_url(self, *args, **kwargs):
        return 'https://my-store.myshopify.com/admin/api/2020-01/'

    def get_resource_url(self):
        return f"{self.base_api_url}/orders.json"


class ShopifyCustomersImporter(ShopifyOrdersImporter):
    SOURCE_TYPE = 'customers'

    def get_resource_url(self):
        return f"{self.base_api_url()}/customers.json"
