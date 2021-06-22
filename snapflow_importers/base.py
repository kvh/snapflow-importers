import logging
import requests
from requests.auth import HTTPBasicAuth

from snapflow_importers.constants import AuthorizationChoices

logger = logging.getLogger(__name__)


class TokenAuthMixin:

    @property
    def _token_name(self):
        """
        The default token name that we're going to use is Bearer
        Clients can override this to use their customized version
        """
        return "Bearer"

    @property
    def _token(self):
        return self._get_access_token()


class Importer(TokenAuthMixin):
    SOURCE_NAME = None
    SOURCE_TYPE = None
    BASE_API_URL = None
    AUTHORIZATION_TYPE = None
    BASIC_AUTH = ()

    def __init__(self):
        if not self.SOURCE_NAME:
            raise ValueError(
                "Can not create Importer subclass without SOURCE_NAME"
            )

        if not self.SOURCE_TYPE:
            raise ValueError(
                "Can not create Importer subclass without SOURCE_TYPE"
            )

        if not self.BASE_API_URL:
            raise ValueError(
                "Can not create Importer subclass without BASE_API_URL"
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
            session.auth = HTTPBasicAuth(self._get_basic_auth())
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
            f'Authorization: {self._token_name} {self._token}'
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
        pass
