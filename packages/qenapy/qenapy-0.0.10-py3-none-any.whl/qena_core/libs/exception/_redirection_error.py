"""
Redirection errors defined by HTTP codes 300-400

see:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages
"""

from ._microservice_exception import MicroserviceException
from ._severity import Severity


class _Redirection(MicroserviceException):
    severity = Severity.LOW


class MultipleChoices(_Redirection):
    status_code = 300


class MovedPermanently(_Redirection):
    status_code = 301


class Found(_Redirection):
    status_code = 302


class SeeOther(_Redirection):
    status_code = 303


class NotModified(_Redirection):
    status_code = 304


class UseProxy(_Redirection):
    status_code = 305


class Unused(_Redirection):
    status_code = 306


class TemporaryRedirect(_Redirection):
    status_code = 307


class PermanentRedirect(_Redirection):
    status_code = 308
