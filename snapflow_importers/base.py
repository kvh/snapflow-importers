import logging
import requests
from requests.auth import HTTPBasicAuth

from snapflow_importers.constants import AuthorizationChoices
from snapflow_importers.mixins import APIRequestsMixin
from snapflow_importers.mixins import TokenAuthMixin

logger = logging.getLogger(__name__)


class ImporterResponse:
    # Assuming a JSON response the DATA_KEY defines
    # where the actual object(s) will live.
    DATA_KEY = 'data'

    def __init__(self, response):
        # This is going to be the original response
        self._response = response
        try:
            self.json_data = response.json()[self.DATA_KEY]
        except:
            # Sometimes we simply don't have a json response format
            self.json_data = {}

        self.headers = response.headers
        self.next_page = self.get_next_page_from_response(response)

    @property
    def _metadata(self):
        # This is here to return metadata related directly with
        return {}

    def get_next_page_from_response(self, response):
        # This needs to be implemented by each of our future Importers
        raise NotImplementedError


class Importer(
    TokenAuthMixin,
    APIRequestsMixin
):
    # External Declarative Configuration
    SOURCE_NAME = None
    SOURCE_TYPE = None
    BASE_API_URL = None
    AUTHORIZATION_TYPE = None
    BASIC_AUTH = ()

    # Response class
    # Response class needs to be an instance of ImporterResponse
    RESPONSE_CLASS = ImporterResponse

    def __init__(self):
        if not self.SOURCE_NAME:
            raise ValueError(
                "Can not create Importer subclass without SOURCE_NAME"
            )

        if not self.SOURCE_TYPE:
            raise ValueError(
                "Can not create Importer subclass without SOURCE_TYPE"
            )

        # Session is private because we don't want this to change
        # Or to be accessed "easy" by clients
        # However, if there are very niched usecases it should be
        # around and ready to go with any pre-requisites configured
        session = requests.Session()
        self._session = self.authorize_session(
            session=session
        )

    def __str__(self):
        return f"{self.SOURCE_NAME} Importer ({self.SOURCE_TYPE})"

    def authorize_session(self, session):
        if self.AUTHORIZATION_TYPE == AuthorizationChoices.BEARER.value:
            session.headers.update(self._get_authorization_header())
            return session

        if self.AUTHORIZATION_TYPE == AuthorizationChoices.BASIC_AUTH.value:
            user, password = self._get_basic_auth()
            session.auth = HTTPBasicAuth(user, password)
            return session

        # We failed to automatically perform the session authorization
        # So at a minimum we'd expect a custom implementation, if not
        # we can't move forward
        raise NotImplementedError

    def _get_access_token(self):
        """
        Depending on what type of authorization is being used on the 3rd party API
        """
        raise NotImplementedError

    def _get_basic_auth(self):
        if not self.BASIC_AUTH:
            raise NotImplementedError
        return self.BASIC_AUTH

    def _get_authorization_header(self):
        logger.info(
            f"Initializing authorization header for {self.__str__()} using {self._token_name} Token"
        )
        return {
            "Authorization": f"{self._token_name} {self._token}"
        }

    def get_resource_url(self):
        """
        Starting with BASE_API_URL we expect this method to always return
        the resource URL for the data type we're trying to ingest from
        the 3rd party API
        """
        raise NotImplementedError

    @property
    def base_api_url(self, *args, **kwargs):
        """
        Base API URL can be either a generic one or one tied to a particular
        external entity.
        This method will return the URL either from class attr or custom
        implementation
        """
        if not self.BASE_API_URL:
            raise NotImplementedError
        return self.BASE_API_URL

    def get_data(self, *args, **kwargs):
        # This is a WIP implementation of the function
        url = self.get_resource_url()
        response = self.get(url=url)
        yield self.RESPONSE_CLASS(response=response)
