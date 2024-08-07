"""
client errors defined by HTTP codes 400-500

see:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses
"""

from ._microservice_exception import MicroserviceException
from ._severity import Severity


class _ClientError(MicroserviceException):
    severity = Severity.MEDIUM


class BadRequest(_ClientError):
    status_code = 400


class Unauthorized(_ClientError):
    status_code = 401


class PaymentRequired(_ClientError):
    status_code = 402


class Forbidden(_ClientError):
    status_code = 403


class NotFound(_ClientError):
    status_code = 404


class MethodNotAllowed(_ClientError):
    status_code = 405


class NotAcceptable(_ClientError):
    status_code = 406


class ProxyAuthenticationRequired(_ClientError):
    status_code = 407


class RequestTimeout(_ClientError):
    status_code = 408


class Conflict(_ClientError):
    status_code = 409


class Gone(_ClientError):
    status_code = 410


class LengthRequired(_ClientError):
    status_code = 411


class PreconditionFailed(_ClientError):
    status_code = 412


class PayloadTooLarge(_ClientError):
    status_code = 413


class URITooLong(_ClientError):
    status_code = 414


class UnsupportedMediaType(_ClientError):
    status_code = 415


class RangeNotSatisfiable(_ClientError):
    status_code = 416


class ExpectationFailed(_ClientError):
    status_code = 417


class IAmATeapot(_ClientError):
    status_code = 418


class MisdirectedRequest(_ClientError):
    status_code = 421


class UnprocessableEntity(_ClientError):
    status_code = 422


class Locked(_ClientError):
    status_code = 423


class FailedDependency(_ClientError):
    status_code = 424


class TooEarly(_ClientError):
    status_code = 425


class UpgradeRequired(_ClientError):
    status_code = 426


class PreconditionRequired(_ClientError):
    status_code = 428


class TooManyRequests(_ClientError):
    status_code = 429


class RequestHeaderFieldsTooLarge(_ClientError):
    status_code = 431


class UnavailableForLegalReasons(_ClientError):
    status_code = 451
