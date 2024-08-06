"""
microservice exception handler that turns all
MicroserviceException's to a JSONResponse
"""

from typing import Optional

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from libs.logger import get_logger
from libs.logstash import Logstash
from libs.response import ResponseCode

from ._microservice_exception import MicroserviceException
from ._severity import Severity

logger = get_logger()


def handle_microservice_exception(request: Request, exc: MicroserviceException):
    if exc.severity is None:
        exc.severity = Severity.LOW

    severity = "INFO"
    message = exc.message

    if exc.severity == Severity.LOW:
        severity = "INFO"
        logger.info(
            '%s %s :: "%s"', request.method, request.url.path, exc.message
        )

        if exc.logstash_logging:
            Logstash().info(
                message=exc.message,
                tags=exc.tags,
                extra=exc.extra,
            )
    elif exc.severity == Severity.MEDIUM:
        severity = "WARNING"
        logger.warning(
            '%s %s :: "%s"', request.method, request.url.path, exc.message
        )

        if exc.logstash_logging:
            Logstash().warning(
                message=exc.message,
                tags=exc.tags,
                extra=exc.extra,
            )
    else:
        severity = "ERROR"
        message = "something went wrong"
        logger.error(
            '%s %s :: "%s"', request.method, request.url.path, exc.message
        )

        if exc.logstash_logging:
            Logstash().error(
                message=exc.message,
                tags=exc.tags,
                extra=exc.extra,
            )

    return JSONResponse(
        content={
            "severity": severity,
            "message": message,
            **_response_code(exc.response_code),
            **_corrective_action(exc.corrective_action),
            **(exc.body if exc.body is not None else {}),
        },
        status_code=_detect_status_code(exc.severity, exc.status_code),
    )


def _corrective_action(corrective_action: Optional[str]):
    if corrective_action is not None:
        return {"correctiveAction": corrective_action}
    return {}


def _response_code(reponse_code: Optional[ResponseCode]):
    if reponse_code is not None:
        return {"code": reponse_code.value}
    return {}


def _detect_status_code(severity: Severity, status_code: Optional[int] = None):
    if status_code is not None:
        return status_code

    if severity == Severity.LOW or severity == Severity.MEDIUM:
        return status.HTTP_400_BAD_REQUEST

    if severity == severity.HIGH:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
