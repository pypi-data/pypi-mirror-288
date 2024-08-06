"""
Used to push logs to elk stack.
"""

from asyncio import (
    AbstractEventLoop,
    CancelledError,
    Task,
    get_running_loop,
    new_event_loop,
)
from functools import partial
from sys import exc_info
from traceback import format_tb
from typing import Any, List, Optional

from click import style
from httpx import AsyncClient
from libs.logger import get_logger
from libs.singleton import Singleton
from settings import settings


class Logstash(metaclass=Singleton):
    """
    Logstash logging utility class.
    """

    def __init__(self) -> None:
        self.__logger = get_logger()
        self.__loop: AbstractEventLoop
        self.__client: AsyncClient

    def info(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(
            severity="info",
            message=message,
            tags=tags,
            extra=extra,
        )

    def success(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(
            severity="success",
            message=message,
            tags=tags,
            extra=extra,
        )

    def warning(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(
            severity="warning",
            message=message,
            tags=tags,
            extra=extra,
        )

    def error(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(
            severity="error",
            message=message,
            tags=tags,
            extra=extra,
        )

    def log_with_status(
        self,
        severity: str,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        data_to_log = {
            "microservice": settings.microservice,
            "severity": severity,
            "message": message,
        }

        if tags is not None:
            data_to_log["tags"] = tags

        if extra is not None:
            if not isinstance(extra, str):
                data_to_log["more"] = str(extra)
            else:
                data_to_log["more"] = extra

        exception_type, exception, traceback = exc_info()

        if exception_type is not None:
            data_to_log["error.type"] = exception_type.__name__

        if exception is not None:
            data_to_log["error.message"] = str(exception)

        if traceback is not None:
            data_to_log["error.stack_trace"] = "".join(format_tb(traceback))

        self.__log(data_to_log)

    def start(self):
        try:
            self.__loop = get_running_loop()
        except RuntimeError:
            self.__loop = new_event_loop()
        auth = None

        if (
            settings.logstash_user is not None
            or settings.logstash_password is not None
        ):
            auth = (
                settings.logstash_user or "",
                settings.logstash_password or "",
            )

        self.__client = AsyncClient(auth=auth)

    async def stop(self):
        await self.__client.aclose()

    def __log(self, message: dict):
        if message["severity"] == "info":
            fg = "cyan"
        elif message["severity"] == "success":
            fg = "green"
        elif message["severity"] == "warning":
            fg = "yellow"
        else:
            fg = "red"

        self.__loop.create_task(
            self.__client.post(url=settings.logstash_host, json=message)
        ).add_done_callback(partial(self.__on_logger_done, message, fg))

    def __on_logger_done(self, message: dict, fg: str, task: Task):
        try:
            if task.exception() is not None:
                return self.__logger.error(
                    msg="Error occured while logging through logstash"
                )
            response = task.result()
            if response.status_code != 200:
                response_message = (
                    response.text[:10] + "." * 3
                    if len(response.text) > 13
                    else response.text
                )

                colored_severity = style(
                    text=message["severity"], fg=fg, bold=True
                )
                colored_status_code = style(
                    text=response.status_code, fg="yellow", bold=True
                )
                colored_response_message = style(
                    text=response_message, fg="bright_black", bold=True
                )

                self.__logger.error(
                    msg=(
                        "Unable to log :: "
                        f"severity: \"{message['severity']}\" | "
                        f"status code: {response.status_code} | "
                        f'message: "{response_message}"'
                    ),
                    extra={
                        "color_message": f"Unable to log :: "
                        f"severity: {colored_severity} | "
                        f"status code: {colored_status_code} | "
                        f'message: "{colored_response_message}"'
                    },
                )

            colored_severity = style(text=message["severity"], fg=fg, bold=True)

            self.__logger.info(
                msg=f"Logstash logger :: severity [{message['severity']}]",
                extra={
                    "color_message": (
                        "Logstash logger :: severity " f"[{colored_severity}]"
                    )
                },
            )
        except CancelledError:
            ...
        except Exception as e:  # pylint: disable=W0718
            self.__logger.error(
                msg="Error occured while logging through logstash :: [{e}]",
                extra={
                    "color_message": (
                        "Error occured while logging through logstash :: "
                        f"[{style(text=e, fg='red', bold=True)}]"
                    )
                },
            )
