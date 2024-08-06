"""
server errors defined by HTTP codes 500-600

see:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses
"""

from ._microservice_exception import MicroserviceException
from ._severity import Severity


class _ServerError(MicroserviceException):
    severity = Severity.HIGH


class InternalServerError(_ServerError):
    status_code = 500


class NotImplemented(_ServerError):  # pylint: disable=W0622
    status_code = 501


class BadGateway(_ServerError):
    status_code = 502


class ServiceUnavailable(_ServerError):
    status_code = 503


class GatewayTimeout(_ServerError):
    status_code = 504


class HTTPVersionNotSupported(_ServerError):
    status_code = 505


class VariantAlsoNegotiates(_ServerError):
    status_code = 506


class InsufficientStorage(_ServerError):
    status_code = 507


class LoopDetected(_ServerError):
    status_code = 508


class NotExtended(_ServerError):
    status_code = 510


class NetworkAuthenticationRequired(_ServerError):
    status_code = 511
