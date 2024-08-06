"""
Rabbitmq message listeners (Consumer or Worker).
"""

from asyncio import (
    CancelledError,
    Future,
    Task,
    get_running_loop,
    iscoroutinefunction,
    new_event_loop,
    set_event_loop,
    sleep,
)
from dataclasses import dataclass
from enum import Enum
from functools import partial
from inspect import Parameter, signature
from json import JSONDecodeError, dumps, loads
from random import random
from types import MappingProxyType
from typing import Any, Callable, Dict, Optional, Tuple, Union

from click import style
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from pydantic import ValidationError, parse_obj_as
from pydantic.json import pydantic_encoder

from libs.exception import RabbitMQException
from libs.logger import get_logger
from libs.rabbitmq._connector import Connector


class ConsumerType(str, Enum):
    CONSUMER = "Consumer"
    WORKER = "Worker"


@dataclass
class ListenerContext:
    """
    Context of the listener at the time exception occured.
    """

    queue: str
    target: Optional[str]
    consumer_type: ConsumerType


class Listener:
    """
    Interface for message listeners
    """

    def __init__(self):
        self._queue: str
        self._pre_fetch_count: int
        self._durable: bool
        self._auto_ack: bool
        self._consumer_methods: Dict[
            str, Tuple[Callable, MappingProxyType[str, Parameter]]
        ]
        self._target_key: str
        self._consumer_type: ConsumerType

    def open_channel(
        self,
        connection: Optional[AsyncioConnection] = None,
        on_exception_callback: Optional[
            Callable[[ListenerContext, BaseException], bool]
        ] = None,
    ):
        """
        Opens a channel for either consumer or rpc worker.
            :param AsyncioConnectio connection: pika asyncio connection.
            :param AbstractEventLoop loop: currently running event loop.
            :param Logger logger: pythons standard logger.
            :param Callable on_exception_callback: a function to be invoked
                when exeption occurs while consuming message.
        """
        try:
            self.__loop = get_running_loop()
        except RuntimeError:
            self.__loop = new_event_loop()
            set_event_loop(self.__loop)

        self._logger = get_logger()
        self._on_exception_callback = on_exception_callback
        self.__failed_open = 0

        if connection is None:
            self.__connector = Connector(
                on_connection_open=self.__on_connection_open
            )

            self.__connector.connect()
        else:
            self.__on_connection_open(connection)

    def close_channel(self):
        """
        Closes the connection and the underling channels in standalone mode.
        """
        self.__connector.disconnect()

    @property
    def queue(self) -> str:
        return self._queue

    def __on_connection_open(self, connection: AsyncioConnection):
        connection.channel(on_open_callback=self.__on_channel_open)

    def __on_channel_open(self, opened_channel):
        self._channel: Channel = opened_channel

        self._channel.add_on_cancel_callback(self.__on_consumer_cancel)

        self._channel.add_on_close_callback(self.__on_channel_close)

        self.__declare_queue()

    def __declare_queue(self):
        self._channel.queue_declare(
            queue=self._queue,
            durable=self._durable,
            callback=self.__on_queue_declared,
        )

    def __on_consumer_cancel(self, _):
        colored_queue = style(text=self._queue, fg="red", bold=True)

        self._logger.error(
            msg=(
                "Consumer cancelled while consuming possibly from queue "
                f'"{self._queue}" getting deleted, declaring queue'
            ),
            extra={
                "color_message": (
                    "Consumer cancelled while consuming possibly from queue "
                    f'"{colored_queue}" getting deleted, declaring queue'
                )
            },
        )

        self.__declare_queue()

    def __on_queue_declared(self, _):
        self._channel.basic_qos(prefetch_count=self._pre_fetch_count)

        self._channel.basic_consume(
            queue=self._queue,
            auto_ack=self._auto_ack,
            on_message_callback=self.__handle_consumption,
        )

        self.__failed_open = 0

    def __handle_consumption(
        self,
        unused_channel: Channel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        if properties.headers is not None:
            target = properties.headers.get(self._target_key) or "__default__"
        else:
            target = "__default__"

        consumer_method = self._consumer_methods.get(target)

        if consumer_method is None:
            return self._logger.error(
                msg=(
                    f"Consumer for {self._consumer_type.value} "
                    f'"{target}" not found'
                ),
                extra={
                    "color_message": (
                        f"Consumer for {self._consumer_type.value} "
                        f"\"{style(text=target, fg='yellow', bold=True)}\""
                        " not found"
                    )
                },
            )

        self.__handle_callback(
            body=body,
            target=target,
            callback=consumer_method,
            on_callback_done=partial(
                self._on_consumer_done, method, properties, target
            ),
        )

    def __handle_callback(
        self,
        body: bytes,
        target: str,
        callback: Tuple[Callable, MappingProxyType[str, Parameter]],
        on_callback_done: Callable,
    ):
        try:
            callback_args, callback_kwargs = self.__parse_args(
                body=body, parameters=callback[1]
            )
        except (ValidationError, ValueError) as e:
            if self._on_exception_callback and not self._on_exception_callback(
                ListenerContext(
                    queue=self._queue,
                    target=target,
                    consumer_type=self._consumer_type,
                ),
                e,
            ):
                colored_target_key = style(
                    text=self._target_key, fg="cyan", bold=True
                )
                colored_target = style(text=target, fg="white", bold=True)
                colored_exception = style(text=e, fg="red", bold=True)

                return self._logger.error(
                    msg=(
                        f'arguments for "{self._target_key}" {target} '
                        f"are not valid :: [{e}]"
                    ),
                    extra={
                        "color_message": (
                            f'arguments for "{colored_target_key}" '
                            f"{colored_target} are not valid :: "
                            f"[{colored_exception}]"
                        )
                    },
                )

            return

        if iscoroutinefunction(callback[0]):
            self.__loop.create_task(
                callback[0](*callback_args, **callback_kwargs)
            ).add_done_callback(on_callback_done)
        else:
            self.__loop.run_in_executor(
                executor=None,
                func=partial(callback[0], *callback_args, **callback_kwargs),
            ).add_done_callback(on_callback_done)

    def __parse_args(
        self, body: bytes, parameters: MappingProxyType[str, Parameter]
    ):
        try:
            message = loads(body.decode())
        except JSONDecodeError:
            message = body.decode()

        assigned_args = []

        callback_args = []
        callback_kwargs = {}

        if isinstance(message, dict):
            args = message.get("args")
            kwargs = message.get("kwargs")

            if isinstance(args, list) and isinstance(kwargs, dict):
                for idx, parameter_name in enumerate(parameters):
                    parameter = parameters[parameter_name]
                    if (
                        parameter.kind is Parameter.POSITIONAL_ONLY
                        or parameter.kind is Parameter.POSITIONAL_OR_KEYWORD
                    ) and idx < len(args):
                        callback_args.append(
                            self.__try_parse(parameter=parameter, obj=args[idx])
                        )
                    elif parameter.kind is Parameter.VAR_POSITIONAL:
                        callback_args.extend(
                            [
                                self.__try_parse(parameter=parameter, obj=arg)
                                for arg in args[idx:]
                            ]
                        )
                    elif (
                        parameter.kind is Parameter.KEYWORD_ONLY
                        or parameter.kind is Parameter.POSITIONAL_OR_KEYWORD
                    ):
                        if parameter.name in kwargs:
                            if parameter.name in assigned_args:
                                raise KeyError(
                                    f"argument {parameter.name} "
                                    "already assigned"
                                )

                            callback_kwargs[parameter.name] = self.__try_parse(
                                parameter=parameter, obj=kwargs[parameter.name]
                            )
                        elif (
                            parameter.name not in assigned_args
                            and parameter.default is Parameter.empty
                        ):
                            raise ValueError(
                                f"argument {parameter.name} has no default"
                            )
                    elif parameter.kind is Parameter.VAR_KEYWORD:
                        callback_kwargs.update(
                            {
                                k: self.__try_parse(parameter=parameter, obj=v)
                                for k, v in kwargs.items()
                                if k not in assigned_args
                            }
                        )

                    assigned_args.append(parameter.name)

                return callback_args, callback_kwargs

        for idx, parameter_name in enumerate(parameters):
            if idx == 0 and message is not None:
                callback_args.append(
                    self.__try_parse(
                        parameter=parameters[parameter_name], obj=message
                    )
                )
            elif (
                parameters[parameter_name].kind is not Parameter.VAR_KEYWORD
                and parameters[parameter_name].default is Parameter.empty
            ):
                raise ValueError(f"argument {parameter_name} has no default")

        return callback_args, callback_kwargs

    def __try_parse(self, parameter: Parameter, obj: Any) -> Any:
        if parameter.annotation is Parameter.empty:
            return obj

        return parse_obj_as(parameter.annotation, obj)

    def _on_consumer_done(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        target: str,
        task_or_future: Union[Task, Future],
    ):
        """
        Method to be registered for the consumer or rpc worker.
        """
        raise NotImplementedError("this method needs implementing")

    def __on_channel_close(self, channel: Channel, exception: Exception):
        if (
            not channel.connection.is_closing
            and not channel.connection.is_closed
        ):
            colored_queue = style(text=self._queue, fg="cyan", bold=True)
            colored_exception = style(text=exception, fg="red", bold=True)

            self._logger.error(
                msg=(
                    "Rabbitmq channel for "
                    f"queue {self._queue} close unexpectedly :: "
                    f"[{exception}]"
                ),
                extra={
                    "color_message": (
                        "Rabbitmq channel for "
                        f"queue {colored_queue} "
                        f"close unexpectedly [{colored_exception}]"
                    )
                },
            )

            if self.__failed_open < 6:
                self.__failed_open += 1

            second = (10 * self.__failed_open) + round(random() * 5, 4)

            self._logger.info(
                "Reopening in approximately %s seconds", int(second)
            )

            self.__loop.create_task(sleep(second)).add_done_callback(
                lambda _: channel.connection.channel(
                    on_open_callback=self.__on_channel_open
                )
                if (
                    not channel.connection.is_closing
                    and not channel.connection.is_closed
                )
                else None
            )


class Consumer(Listener):
    """
    Rabbitmq message listener without respose of the result to the client
    """

    def __init__(
        self,
        queue: str,
        pre_fetch_count: int = 250,
        durable: bool = True,
        auto_ack: bool = True,
    ):
        super().__init__()
        self._queue = queue
        self._pre_fetch_count = pre_fetch_count
        self._durable = durable
        self._auto_ack = auto_ack
        self._consumer_methods = {}
        self._target_key = "target"
        self._consumer_type = ConsumerType.CONSUMER

    def consume(self, target: Optional[str] = None):
        """
        This is used to decorate a consumer method.
            :param Optional[str] target: an optional target name.
        Usage:
            @consumer_instance.consume("your_target")
            def your_target_method(data: bytes):
                ...
                return True # or False
        """

        def wrapper(consumer: Callable):
            if target is None:
                if "__default__" in self._consumer_methods:
                    raise ValueError(
                        "Rabbitmq queue message consumer "
                        "with the default empty target exists."
                    )

                self._consumer_methods["__default__"] = (
                    consumer,
                    signature(consumer).parameters,
                )
            else:
                if target in self._consumer_methods:
                    raise ValueError(
                        "Rabbitmq queue message consumer with similar"
                        f'target "{target}" exists.'
                    )

                self._consumer_methods[target] = (
                    consumer,
                    signature(consumer).parameters,
                )

        return wrapper

    def _on_consumer_done(
        self,
        method: Basic.Deliver,
        properties: BasicProperties,
        target: str,
        task_or_future: Union[Task, Future],
    ):
        try:
            e = task_or_future.exception()
            if e is not None:
                if (
                    self._on_exception_callback
                    and not self._on_exception_callback(
                        ListenerContext(
                            queue=self._queue,
                            target=target,
                            consumer_type=self._consumer_type,
                        ),
                        e,
                    )
                ):
                    colored_queue = style(
                        text=self._queue, fg="cyan", bold=True
                    )
                    colored_target = style(text=target, fg="yellow", bold=True)
                    colored_exception = style(text=e, fg="red", bold=True)

                    self._logger.error(
                        msg=(
                            "Exception occured while processing "
                            f"queued message for Queue = {self._queue}, "
                            'Target = {target} - "{e}"'
                        ),
                        extra={
                            "color_message": (
                                "Exception occured while processing"
                                f"queued message for Queue = {colored_queue}, "
                                f"Target = {colored_target} - "
                                f'"{colored_exception}"'
                            )
                        },
                    )
            else:
                if not self._auto_ack and task_or_future.result():
                    self._channel.basic_ack(method.delivery_tag)

                colored_queue = style(text=self._queue, fg="cyan", bold=True)
                colored_target = style(text=target, fg="yellow", bold=True)

                self._logger.info(
                    msg=(
                        "Message consumed  <<| "
                        f"Queue = {self._queue}, Target = {target}"
                    ),
                    extra={
                        "color_message": (
                            "Message consumed  <<| "
                            f"Queue = {colored_queue},"
                            f"Target = {colored_target}"
                        )
                    },
                )
        except CancelledError:
            ...


class RpcWorker(Listener):
    """
    Rabbitmq message listener which responds back the result.
    """

    def __init__(
        self, queue: str, pre_fetch_count: int = 250, durable: bool = False
    ):
        super().__init__()
        self._queue = queue
        self._pre_fetch_count = pre_fetch_count
        self._durable = durable
        self._auto_ack = True
        self._consumer_methods = {}
        self._target_key = "procedure"
        self._consumer_type = ConsumerType.WORKER

    def execute(self, procedure: Optional[str] = None):
        """
        This a decorator for a worker method.
            :param Optional[str] procedure: an optional procedure name.
        Usage:
            @worker_instance.execute("your_target")
            def your_target_method(data: bytes):
                ...
                return "Some data"
        """

        def wrapper(worker: Callable):
            if procedure is None:
                if "__default__" in self._consumer_methods:
                    raise ValueError(
                        "Rabbitmq rpc worker with the default empty "
                        "procedure exists."
                    )

                target = "__default__"
            else:
                if procedure in self._consumer_methods:
                    raise ValueError(
                        "Rabbitmq rpc worker with similar procedure "
                        f'"{procedure}" exists.'
                    )

                target = procedure

            self._consumer_methods[target] = (
                worker,
                signature(worker).parameters,
            )

        return wrapper

    def _on_consumer_done(
        self,
        _,
        properties: BasicProperties,
        target: str,
        task_or_future: Union[Task, Future],
    ):
        try:
            e = task_or_future.exception()
            if e is not None:
                if (
                    self._on_exception_callback
                    and not self._on_exception_callback(
                        ListenerContext(
                            queue=self._queue,
                            target=target,
                            consumer_type=self._consumer_type,
                        ),
                        e,
                    )
                ):
                    self.__worker_error_logger(e=e, procedure=target)

                response = self.__handle_exception(e)
            else:
                response = task_or_future.result()

                colored_queue = style(text=self._queue, fg="cyan", bold=True)
                colored_procedure = style(text=target, fg="yellow", bold=True)

                self._logger.info(
                    msg=(
                        "Rpc request recieved for "
                        f"RPC queue = {self._queue}, "
                        f"Procedure = {target}"
                    ),
                    extra={
                        "color_message": (
                            "Rpc request recieved for "
                            f"RPC queue = {colored_queue}, "
                            f"Procedure = {colored_procedure}"
                        )
                    },
                )

            self.__reply_response(properties=properties, response=response)
        except CancelledError:
            ...
        except Exception as e:  # pylint: disable=W0718
            self.__worker_error_logger(e=e, procedure=target)

    def __worker_error_logger(self, e: BaseException, procedure: str):
        colored_queue = style(text=self._queue, fg="cyan", bold=True)
        colored_procedure = style(text=procedure, fg="yellow", bold=True)
        colored_exception = style(text=e, fg="red", bold=True)

        self._logger.error(
            msg=(
                "Exception occured while processing rpc message "
                f"for RPC queue = {self._queue}, "
                f'Procedure = {procedure} - "{e}"'
            ),
            extra={
                "color_message": (
                    "Exception occured while processing rpc message "
                    f"for RPC queue = {colored_queue}, "
                    f"Procedure = {colored_procedure} - "
                    f'"{colored_exception}"'
                )
            },
        )

    def __handle_exception(self, exception: BaseException):
        if isinstance(exception, RabbitMQException):
            return {
                "exception": True,
                "code": exception.code,
                "message": exception.message,
            }

        if isinstance(exception, ValidationError):
            return {
                "exception": True,
                "code": 1,
                "message": str(exception.errors()),
            }

        return {
            "exception": True,
            "code": 0,
            "message": "something went wrong while processing rpc request",
        }

    def __reply_response(self, properties: BasicProperties, response: Any):
        if properties.correlation_id is None:
            return self._logger.error(
                '"correlation_id" property not supplied for rpcworker to reply'
            )

        publish_properties = BasicProperties(
            correlation_id=properties.correlation_id
        )

        try:
            response_json = dumps(
                obj=response, default=pydantic_encoder
            ).encode()
        except (JSONDecodeError, TypeError, ValueError) as e:
            self._logger.error(
                msg=f"Rpc Worker response is not serializable :: [{e}]",
                extra={
                    "color_message": (
                        "Rpc Worker response is not serializable :: "
                        f"[{style(text=e, fg='red', bold=True)}]"
                    )
                },
            )

            return

        if properties.reply_to is None:
            return self._logger.error(
                '"reply_to" property not supplied for rpc worker to reply'
            )

        self._channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=publish_properties,
            body=response_json,
        )
