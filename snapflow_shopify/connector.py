import base64

from snapflow_importers.base import Importer
from snapflow_importers.base import ImporterResponse
from snapflow_importers.constants import AuthorizationChoices


class ShopifyResponse(ImporterResponse):
    DATA_KEY = 'orders'

    def get_next_page_from_response(self, response):
        headers = response.headers
        if not headers:
            return None
        values = headers.get("Link", headers.get("link"))
        if not values:
            return None
        result = {}
        for value in values.split(", "):
            link, rel = value.split("; ")
            result[rel.split('"')[1]] = link[1:-1]
        return result.get("next")


class ShopifyOrdersImporter(Importer):
    SOURCE_NAME = 'shopify'
    SOURCE_TYPE = 'orders'
    AUTHORIZATION_TYPE = AuthorizationChoices.BASIC_AUTH.value
    BASIC_AUTH = (
        '36604ac070fe6fc6493e92585badee92',
        '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'
    )
    RESPONSE_CLASS = ShopifyResponse

    @property
    def base_api_url(self, *args, **kwargs):
        return 'https://agh-test.myshopify.com/admin/api/2021-04'

    def get_resource_url(self):
        return f"{self.base_api_url}/orders.json"

    def _get_access_token(self):
        auth = "36604ac070fe6fc6493e92585badee92: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"
        return base64.b64encode(auth.encode()).decode("ascii")


class ShopifyCustomersImporter(ShopifyOrdersImporter):
    SOURCE_TYPE = 'customers'

    def get_resource_url(self):
        return f"{self.base_api_url}/customers.json"


class ShopifyRefundsImporter(ShopifyOrdersImporter):
    SOURCE_TYPE = 'refunds'

    def get_resource_url(self):
        return f"{self.base_api_url}/refunds.json"
