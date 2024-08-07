"""
API reponse classes.
"""

from enum import Enum


def OK(body: dict):
    """
    A successful severity response.
        :param body dict: Any data type that is json serializable
            preferably a dictionary.
    """
    if not isinstance(body, dict):
        raise ValueError("body is not type dict")
    return {"severity": "SUCCESS", **body}


class ResponseCode(Enum):
    SIGNATURE_INVALID = 100
    UNAUTHORIZED = 102
