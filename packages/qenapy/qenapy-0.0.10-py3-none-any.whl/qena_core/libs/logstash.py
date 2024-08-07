"""
Used to push logs to ELK stack.
"""

import asyncio
from asyncio import (
    AbstractEventLoop,
    CancelledError,
    Task,
    get_running_loop,
    new_event_loop,
    set_event_loop,
)
from functools import partial
from sys import exc_info
from traceback import format_tb
from typing import Any, List, Optional

from click import style
from httpx import AsyncClient

from qena_core.libs.logger import get_logger
from qena_core.libs.singleton import Singleton
from qena_core.settings import settings


class Logstash(metaclass=Singleton):
    """
    Logstash logging utility class.
    """

    def __init__(self) -> None:
        self.__logger = get_logger()
        self.__loop: AbstractEventLoop
        self.__client: AsyncClient
        self.start()

    def info(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(severity="info", message=message, tags=tags, extra=extra)

    def success(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(
            severity="success", message=message, tags=tags, extra=extra
        )

    def warning(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(
            severity="warning", message=message, tags=tags, extra=extra
        )

    def error(
        self,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        self.log_with_status(severity="error", message=message, tags=tags, extra=extra)

    def log_with_status(
        self,
        severity: str,
        message: Any,
        tags: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ):
        """Log a message with a given severity, tags, and extra information."""
        data_to_log = {
            "microservice": settings.microservice,
            "severity": severity,
            "message": message,
        }

        if tags is not None:
            data_to_log["tags"] = tags

        if extra is not None:
            data_to_log["more"] = str(extra)

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
            self.__loop: AbstractEventLoop = get_running_loop()
        except RuntimeError:
            self.__loop: AbstractEventLoop = new_event_loop()
            set_event_loop(self.__loop)

        auth = None
        if settings.logstash_user is not None or settings.logstash_password is not None:
            auth = (settings.logstash_user or "", settings.logstash_password or "")

        self.__client = AsyncClient(auth=auth)

    def stop(self):
        if self.__client is not None:
            asyncio.run(self.__client.aclose())
        if self.__loop is not None:
            self.__loop.stop()

    def __log(self, message: dict):
        """Send the log message to Logstash."""
        severity_to_color = {
            "info": "cyan",
            "success": "green",
            "warning": "yellow",
            "error": "red",
        }

        fg = severity_to_color.get(message["severity"], "red")

        async def post_log():
            response = await self.__client.post(
                url=settings.logstash_host, json=message
            )

            return response

        task = self.__loop.create_task(post_log())
        task.add_done_callback(
            lambda tk: asyncio.ensure_future(self.__on_logger_done(message, fg, tk))
        )

    async def __on_logger_done(self, message: dict, fg: str, task: Task) -> None:
        """Handle the result of the log message being sent."""
        try:
            response = await task
            if response.status_code >= 400:
                response_message = (
                    response.text[:10] + "..."
                    if len(response.text) > 13
                    else response.text
                )

                colored_severity = style(text=message["severity"], fg=fg, bold=True)
                colored_status_code = style(
                    text=response.status_code, fg="yellow", bold=True
                )
                colored_response_message = style(
                    text=response_message, fg="bright_black", bold=True
                )

                self.__logger.error(
                    msg=(
                        "Unable to log :: "
                        f'severity: "{message["severity"]}" | '
                        f"status code: {response.status_code} | "
                        f'message: "{response_message}"'
                    ),
                    extra={
                        "color_message": (
                            "Unable to log :: "
                            f"severity: {colored_severity} | "
                            f"status code: {colored_status_code} | "
                            f'message: "{colored_response_message}"'
                        )
                    },
                )

            colored_severity = style(text=message["severity"], fg=fg, bold=True)

            self.__logger.info(
                msg=f'Logstash logger :: severity [{message["severity"]}]',
                extra={
                    "color_message": f"Logstash logger :: severity [{colored_severity}]"
                },
            )
        except CancelledError:
            ...
        except Exception as e:
            self.__logger.error(
                msg=f"Error occurred while logging through logstash :: [{e}]",
                extra={
                    "color_message": (
                        f"Error occurred while logging through logstash :: [{style(text=str(e), fg='red', bold=True)}]"
                    )
                },
            )

    def get_event_loop(self) -> AbstractEventLoop:
        return self.__loop
