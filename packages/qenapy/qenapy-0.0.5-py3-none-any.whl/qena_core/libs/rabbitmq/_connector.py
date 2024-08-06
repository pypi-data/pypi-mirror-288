"""
Manages connection and reconnection to rabbitmq
"""

from asyncio import get_running_loop, new_event_loop, set_event_loop, sleep
from random import random
from typing import Callable, Optional

from click import style
from pika import URLParameters
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.exceptions import ConnectionWrongStateError

from libs.logger import get_logger
from settings import settings


class Connector:
    """
    Manages connection and reconnection to rabbitmq
    """

    def __init__(
        self,
        on_connection_open: Callable[[AsyncioConnection], None],
        rabbitmq_uri: Optional[str] = None,
    ):
        try:
            self.__loop = get_running_loop()
        except RuntimeError:
            self.__loop = new_event_loop()
            set_event_loop(self.__loop)

        self.__rabbitmq_uri = rabbitmq_uri
        self.__logger = get_logger()
        self.__stopping = False
        self.__on_connection_opened = on_connection_open
        self.__failed_connection = 0

    def connect(self):
        self.__connect()

    def __connect(self):
        self.__connection = AsyncioConnection(
            parameters=URLParameters(
                self.__rabbitmq_uri or settings.rabbitmq_url
            ),
            on_open_callback=self.__on_connection_opened,
            on_open_error_callback=self.__on_connection_open_error,
            on_close_callback=self.__on_connection_closed,
            custom_ioloop=self.__loop,
        )

    def disconnect(self):
        try:
            self.__stopping = True
            self.__connection.close()
        except ConnectionWrongStateError as e:
            if not self.__stopping:
                self.__logger.info(
                    msg=f"Unable to stop consumer :: [{e}]",
                    extra={
                        "color_message": (
                            "Unable to stop consumer :: "
                            f"[{style(text=e, fg='red', bold=True)}]"
                        )
                    },
                )

    def __on_connection_open_error(self, _, exception):
        self.__logger.error(
            msg=f"Unable to connect to rabbitmq :: [{exception}]",
            extra={
                "color_message": (
                    "Unable to connect to rabbitmq :: "
                    f"[{style(text=exception, fg='red', bold=True)}]"
                )
            },
        )

        self.__reconnect(connecting_error=True)

    def __on_connection_closed(self, _, exception):
        if not self.__stopping:
            self.__logger.error(
                msg=f"Connection to rabbitmq closed :: [{exception}]",
                extra={
                    "color_message": (
                        "Connection to rabbitmq closed :: "
                        f"[{style(str(exception), fg='red', bold=True)}]"
                    )
                },
            )

            self.__reconnect()

    def __reconnect(self, connecting_error=False):
        if connecting_error and self.__failed_connection < 6:
            self.__failed_connection += 1

        second = (10 * self.__failed_connection) + round(random() * 5, 4)

        self.__logger.info(
            "Reconnecting in approximately %s seconds", int(second)
        )

        self.__loop.create_task(sleep(second)).add_done_callback(
            lambda _: self.__connect()
        )
