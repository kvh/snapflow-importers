from urllib.parse import urlsplit, urlunsplit, urlencode

from snapflow_importers.base import Importer
from snapflow_importers.base import ImporterResponse
from snapflow_importers.constants import AuthorizationChoices


class SquareUpResponse(ImporterResponse):
    def get_next_page_from_response(self, response):
        cursor = response.json().get('cursor')
        if not cursor:
            return None

        split = urlsplit(response.url)
        new_url = urlunsplit((
            split.scheme,
            split.netloc,
            split.path,
            urlencode(dict(cursor=cursor)),
            None,
        ))
        return new_url


class SquareUpItemsResponse(SquareUpResponse):
    def _get_data_key(self):
        return 'objects'

    def get_next_page_from_response(self, response):
        cursor = response.json().get('cursor')
        if not cursor:
            return None

        split = urlsplit(response.url)
        new_url = urlunsplit((
            split.scheme,
            split.netloc,
            split.path,
            urlencode(dict(types='item', cursor=cursor)),
            None,
        ))
        return new_url


class SquareUpCustomersImporter(Importer):
    SOURCE_NAME = 'squareup'
    SOURCE_TYPE = 'customers'
    AUTHORIZATION_TYPE = AuthorizationChoices.BEARER.value
    RESPONSE_CLASS = SquareUpResponse

    def _get_access_token(self):
        return ''

    @property
    def base_api_url(self):
        return "https://connect.squareup.com/v2/"

    def get_resource_url(self):
        return f"{self.base_api_url}customers/"


class SquareUpPaymentsImporter(SquareUpCustomersImporter):
    SOURCE_TYPE = 'payments'

    def get_resource_url(self):
        return f"{self.base_api_url}payments/"


class SquareUpItemsImporter(SquareUpCustomersImporter):
    SOURCE_TYPE = 'products'
    RESPONSE_CLASS = SquareUpItemsResponse

    def get_resource_url(self):
        return f"{self.base_api_url}catalog/list?types=item"
