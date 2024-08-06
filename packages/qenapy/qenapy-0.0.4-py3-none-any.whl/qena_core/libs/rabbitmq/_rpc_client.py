"""
This module contains rpc client related classes.
"""

from asyncio import (
    FIRST_COMPLETED,
    AbstractEventLoop,
    Event,
    Queue,
    get_running_loop,
    new_event_loop,
    sleep,
    wait,
)
from dataclasses import dataclass
from json import JSONDecodeError, dumps, loads
from logging import Logger
from typing import Callable, Optional, Type
from uuid import uuid4

from click import style
from pika import BasicProperties
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.channel import Channel
from pika.frame import Method
from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder

from libs.exception import RabbitMQException
from libs.logger import get_logger
from libs.rabbitmq._connector import Connector


class ExitHandler:
    """
    Binds to unvicorn exit handler to terminate
    pending rpc requests.
    """

    _exiting = False
    exit_event: Event
    _original_exit_handler: Callable

    @classmethod
    def is_exising(cls):
        return cls._exiting

    @classmethod
    def set_exiting(cls):
        cls._exiting = True

    @staticmethod
    def patch_exit_handler():
        try:
            from uvicorn.server import Server  # pylint: disable=C0415
        except ModuleNotFoundError:
            return

        ExitHandler.exit_event = Event()
        ExitHandler._original_exit_handler = Server.handle_exit
        Server.handle_exit = ExitHandler.handle_exit

    @staticmethod
    def notify_clients():
        ExitHandler.set_exiting()
        ExitHandler.exit_event.set()

    @staticmethod
    def handle_exit(*args, **kwargs):
        ExitHandler.notify_clients()
        ExitHandler._original_exit_handler(*args, **kwargs)


# patchs the default exit handler for uvicorn
# to terminate any open rpc request when
# the server is closed.
ExitHandler.patch_exit_handler()


@dataclass
class RpcRequest:
    """
    Container class for each rpc request.
    """

    routing_key: str
    exchange: str
    procedure: str
    return_type: Optional[Type]
    legacy: bool
    timeout: int

    def set_future_response(
        self, loop: AbstractEventLoop, message: Optional[dict], logger: Logger
    ):
        self.__loop = loop
        self.__message = message
        self.__logger = logger
        self.future = self.__loop.create_future()

    def assign_channel(self, channel: Channel):
        self.__channel = channel

        try:
            self.__channel.queue_declare(
                queue="",
                exclusive=True,
                auto_delete=True,
                callback=self.__on_queue_declare,
            )
        except Exception as e:  # pylint: disable=W0718
            return self.future.set_exception(e)

    def __on_queue_declare(self, method: Method):
        self.__callback_queue = method.method.queue

        try:
            self.__consumer_tag = self.__channel.basic_consume(
                queue=self.__callback_queue,
                on_message_callback=self.__on_message,
                auto_ack=True,
            )
        except Exception as e:  # pylint: disable=W0718
            self.future.set_exception(e)

            return self.__finalize()

        self.__corr_id = str(uuid4())

        headers = {"procedure": self.procedure}

        try:
            self.__channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                properties=BasicProperties(
                    content_type="application/json",
                    reply_to=self.__callback_queue,
                    correlation_id=self.__corr_id,
                    headers=headers,
                ),
                body=dumps(obj=self.__message, default=pydantic_encoder),
            )
        except Exception as e:  # pylint: disable=W0718
            self.future.set_exception(e)

            return self.__finalize()

        if self.timeout > 0:
            if self.__loop is None:
                raise ValueError(
                    "running loop not assigned yet :: "
                    "for client request timeout"
                )

            self.__loop.create_task(
                wait(
                    fs={
                        self.__loop.create_task(sleep(self.timeout)),
                        self.__loop.create_task(ExitHandler.exit_event.wait()),
                    },
                    return_when=FIRST_COMPLETED,
                )
            ).add_done_callback(self.__timeout_or_exit_handler)

    def __timeout_or_exit_handler(self, _):
        if ExitHandler.is_exising():
            self.future.cancel()

            return self.__finalize()

        if not self.future.done():
            colored_routing_key = style(
                text=self.routing_key, fg="cyan", bold=True
            )
            colored_procedure = style(
                text=self.procedure, fg="yellow", bold=True
            )

            if self.__logger is not None:
                self.__logger.error(
                    msg=(
                        f"Rpc worker didn't responed in a timely manner - "
                        f'"{self.routing_key} => '
                        f'{self.procedure}" stopping...'
                    ),
                    extra={
                        "color_message": (
                            "Rpc worker didn't responed in a timely manner - "
                            f'"{colored_routing_key} => '
                            f'{colored_procedure}" stopping...'
                        )
                    },
                )

            self.future.set_exception(
                TimeoutError("Rpc worker didn't responed in a timely manner")
            )

            self.__finalize()

    def __on_message(self, unused_channel, unused_method, props, body: bytes):
        if self.__corr_id != props.correlation_id:
            return

        try:
            deserialized_response = loads(body.decode())
        except (JSONDecodeError, TypeError, ValueError) as e:
            if self.__logger is not None:
                self.__logger.error(
                    msg=f"Rpc response is not deserializable :: [{e}]",
                    extra={
                        "color_message": (
                            "Rpc response is not deserializable :: "
                            f"[{style(text=e, fg='red', bold=True)}]"
                        )
                    },
                )

            self.future.set_exception(
                RabbitMQException(
                    code=0,
                    message=f"Rpc response is not deserializable :: [{e}]",
                )
            )

            return self.__finalize()

        if isinstance(deserialized_response, dict):
            if deserialized_response.get("exception"):
                self.future.set_exception(
                    RabbitMQException(
                        code=deserialized_response.get("code") or 0,
                        message=(
                            deserialized_response.get("message")
                            or (
                                "something went wrong while processing"
                                " rpc client response."
                            )
                        ),
                    )
                )

                return self.__finalize()

        if self.return_type is not None:
            try:
                deserialized_response = parse_obj_as(
                    self.return_type, deserialized_response
                )
            except Exception as e:  # pylint: disable=W0718
                self.future.set_exception(e)

                return self.__finalize()

        self.future.set_result(deserialized_response)

        self.__finalize()

    def __finalize(self):
        if not self.__channel.is_closed and self.__consumer_tag is not None:
            self.__channel.basic_cancel(self.__consumer_tag)

        RpcRequestManager.recycle_channel(self.__channel)


class RpcRequestManager:
    """
    Rpc request manager
    """

    _connection: AsyncioConnection
    _loop: AbstractEventLoop
    _logger: Logger
    _channel_pool: Queue[Channel]

    @classmethod
    def start(
        cls,
        connection: Optional[AsyncioConnection] = None,
        logger: Optional[Logger] = None,
    ):
        """
        Opens a channels for purpose of rpc requests.
            :param AsyncioConnection connection:
            :param AbstractEventLoop loop:
            :param Logger logger:
        """
        try:
            cls._loop = get_running_loop()
        except RuntimeError:
            cls._loop = new_event_loop()

        cls._logger = logger or get_logger()

        if connection is None:
            cls._connector = Connector(
                on_connection_open=cls.__on_connection_open
            )
            cls._connector.connect()
        else:
            cls.__on_connection_open(connection)

    @classmethod
    def stop(cls):
        """
        Disconnects the rabbitmq connector
        """
        ExitHandler.notify_clients()
        cls._connector.disconnect()

    @classmethod
    def __on_connection_open(cls, connection: AsyncioConnection):
        cls._connection = connection
        cls.__prewarm_channel_pool()

    @classmethod
    def __prewarm_channel_pool(cls):
        cls._channel_pool = Queue()
        for _ in range(250):
            cls._connection.channel(on_open_callback=cls.__fill_pool)

    @classmethod
    def __fill_pool(cls, channel: Channel):
        channel.add_on_close_callback(cls.__on_channel_closed)
        cls._channel_pool.put_nowait(channel)

    @classmethod
    def __on_channel_closed(cls, channel, exception):
        del channel, exception

        if (
            not ExitHandler.is_exising()
            and not cls._connection.is_closing
            and not cls._connection.is_closed
        ):
            cls._connection.channel(on_open_callback=cls.__fill_pool)

    @classmethod
    async def request_rpc(
        cls, rpc_request: RpcRequest, message: Optional[dict]
    ):
        if not hasattr(cls, "_loop"):
            raise ValueError("event loop not set")

        if not hasattr(cls, "_logger"):
            raise ValueError("logger not set")

        rpc_request.set_future_response(
            loop=cls._loop, message=message, logger=cls._logger
        )

        if not hasattr(cls, "_channel_pool"):
            raise ValueError("channel pool not instantiated")

        rpc_request.assign_channel(await cls._channel_pool.get())

        return await rpc_request.future

    @classmethod
    def recycle_channel(cls, channel: Channel):
        cls._channel_pool.put_nowait(channel)


class RpcClient:
    """
    A Rabbitmq RPC client to request to rpc worker.
    """

    def __init__(
        self,
        routing_key: str,
        exchange: Optional[str] = None,
        procedure: Optional[str] = None,
        return_type: Optional[Type] = None,
        legacy: bool = False,
        timeout: int = 0,
    ):
        """
        Rabbitmq rpc client

        :param str rpc_queue: the queue that is going to be used for the rpc.
        :param Optional[str] procedure: the handler identifier to direct to.
        :param int timeout: after how many seconds the rpc should close.
        """
        self.__rpc_request = RpcRequest(
            routing_key=routing_key,
            exchange=exchange or "",
            procedure=procedure or "__default__",
            return_type=return_type,
            legacy=legacy,
            timeout=timeout,
        )

    async def call(self, *args, **kwargs):
        """
        Request a message from rabbitmq rpc worker.
        this method blocks untill it recieves a message or timesout.
            :param *args:
            :param **kwargs:

            :raises: TimeoutError, RabbitMQException and ValidationError
        """

        if self.__rpc_request.legacy:
            if args:
                message = args[0]
            elif kwargs:
                message = kwargs.popitem()[1]
            else:
                message = None
        else:
            message = {"args": args, "kwargs": kwargs}

        return await RpcRequestManager.request_rpc(
            rpc_request=self.__rpc_request, message=message
        )

    async def __call__(self, *args, **kwargs):
        return await self.call(*args, **kwargs)
