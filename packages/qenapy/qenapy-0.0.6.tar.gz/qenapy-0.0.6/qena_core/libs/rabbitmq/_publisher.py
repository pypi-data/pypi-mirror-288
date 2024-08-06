"""
Publisher class provides an interface to publish a message to a rabbitmq queue.
"""

from json import dumps
from logging import Logger
from typing import Any, Dict, Optional, Union

from click import style
from pika import BasicProperties
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.channel import Channel
from pydantic.json import pydantic_encoder

from libs.logger import get_logger
from libs.rabbitmq._connector import Connector


class Publisher:
    """
    Publisher class provides an interface
    to publish a message to a rabbitmq queue.
    """

    _logger: Logger
    _channel: Channel

    def __init__(
        self,
        routing_key: str,
        exchange: Optional[str] = None,
        target: Optional[str] = None,
        legacy: Optional[bool] = None,
    ):
        """
        Rabbitmq message to be published.
            :param str routing_key:
            :param typing.Optional[str] exchange:
            :param typing.Optional[str] target:
            :param typing.Optional[bool] legacy:
        """
        self.__routing_key = routing_key
        self.__exchange = exchange or ""
        self.__target = target or "__default__"
        self.__legacy = legacy or False

    def publish(self, *args, **kwargs):
        """
        Publish a message to rabbitmq queue by providing arbitrary positional.
        if message is legacy it would pick a single value from either positional
        or keyword arguments.
            :param *args:
            :param *kwargs:
        """
        payload: Dict[str, Any] = {
            "routing_key": self.__routing_key,
            "exchange": self.__exchange,
            "target": self.__target,
        }

        if self.__legacy:
            if args:
                payload["message"] = args[0]
            elif kwargs:
                payload["message"] = kwargs.popitem()[1]
            else:
                payload["message"] = None
        else:
            payload["message"] = {"args": args, "kwargs": kwargs}

        Publisher.publish_message(**payload)

    @classmethod
    def start(
        cls,
        connection: Optional[AsyncioConnection] = None,
    ):
        """
        Opens a channel for publishing messages.
            :param connection AsyncioConnection: pika asyncio connection.
            :param Logger logger: pythons standard logger.
        """
        cls.__logger = get_logger()

        if connection is None:
            cls.__connector = Connector(
                on_connection_open=cls.__on_connection_open,
            )
            cls.__connector.connect()
        else:
            cls.__on_connection_open(connection)

    @classmethod
    def stop(cls):
        """
        Disconnects the rabbitmq connector in standalone mode
        """
        cls.__connector.disconnect()

    @classmethod
    def __on_connection_open(cls, connection: AsyncioConnection):
        connection.channel(on_open_callback=cls.__on_channel_open)

    @classmethod
    def __on_channel_open(cls, channel: Channel):
        cls.__channel = channel

        cls.__channel.add_on_close_callback(cls.__on_channel_close)

    @classmethod
    def __on_channel_close(cls, channel: Channel, exception: Exception):
        if (
            not channel.connection.is_closing
            and not channel.connection.is_closed
        ):
            cls.__logger.error(
                msg=(
                    "Rabbitmq channel for publisher close unexpectedly :: "
                    f"[{exception}]"
                ),
                extra={
                    "color_message": (
                        "Rabbitmq channel for publisher close unexpectedly :: "
                        f"[{style(text=exception, fg='red', bold=True)}]"
                    )
                },
            )

            channel.connection.channel(on_open_callback=cls.__on_channel_open)

    @classmethod
    def publish_message(
        cls,
        routing_key: str,
        exchange: str,
        target: str,
        message: Union[Any, dict],
    ):
        """
        Publishes a message to specified exchange and routing key.
            :param str routing_key:
            :param str exchange:
            :param str target:
            :param str message
        """
        headers = {"target": target}

        properties = BasicProperties(
            content_type="application/json", headers=headers
        )

        cls.__channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=dumps(obj=message, default=pydantic_encoder),
            properties=properties,
        )

        cls.__logger.info(
            msg=(
                "Message published |>> Queue = "
                f"{routing_key}, Target = {target}"
            ),
            extra={
                "color_message": (
                    "Message published |>> Queue = "
                    f"{style(text=routing_key, fg='cyan', bold=True)}, "
                    f"Target = {style(text=target, fg='yellow', bold=True)}"
                )
            },
        )
