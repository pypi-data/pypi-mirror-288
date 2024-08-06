"""
Application Error base class

All application errors must have this class as base.
"""

from typing import Any, List, Optional

from app.core.libs.response import ResponseCode

from ._severity import Severity


class MicroserviceException(Exception):
    """
    General microservice exception which other exceptions inherit.
    """

    def __init__(
        self,
        message: str,
        body: Optional[Any] = None,
        corrective_action: Optional[str] = None,
        severity: Optional[Severity] = None,
        status_code: Optional[int] = None,
        response_code: Optional[ResponseCode] = None,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        logstash_logging: bool = True,
    ):
        """
        An exception for microservices with message and severity.

        :param message str: string message
        :param body Optional[Any]: an optional response body
        :param corrective_action Optional[str]: a corrective action
            to counter the error
        :param severity Optional[Severity]: a severity with scale of
            (LOW, MEDIUM, HIGH)
        :param status_code Optional[int]: the http status code incase
            it reaches the api exception handler
        :param response_code Optional[ResponseCode]: the response code
            to represent the error
        :param tags Optional[Optional[List[str]]: a set of strings
            to represent the error occured in a log
        :param extra Optional[Any]: additional generic information
            to include with the exception
        :param logstash_logging bool: whether to log it to logstash or not
        """
        self.message = message
        self.body = body
        self.corrective_action = corrective_action
        self.response_code = response_code
        self.tags = tags
        self.extra = extra
        self.logstash_logging = logstash_logging

        if hasattr(self, "severity") and severity is not None:
            self.severity = severity

        if hasattr(self, "status_code") and status_code is not None:
            self.status_code = status_code

        self.args = tuple({"message": self.message, "tags": self.tags})

    def __str__(self):
        return str(self.args)
