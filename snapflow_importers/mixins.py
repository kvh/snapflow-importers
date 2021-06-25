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


class APIRequestsMixin:
    # This mixin will also implement retry mechanisms

    def get(self, url, params=None):
        response = self._session.get(
            url,
            params=params
        )
        response.raise_for_status()
        return self.RESPONSE_CLASS(
            response=response,
            data_key=self.SOURCE_TYPE
        )
