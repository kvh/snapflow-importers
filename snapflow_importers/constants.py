from enum import Enum


class AuthorizationChoices(str, Enum):
    """
    Supported built-in choices for 3rd party
    API authorization
    """
    BEARER = 'bearer'
    BASIC_AUTH = 'basic_auth'

    @classmethod
    def choices(cls):
        return (
            (cls.BEARER.value, "Bearer Token Authorization"),
            (cls.BASIC_AUTH.value, "Basic Authentication")
        )
