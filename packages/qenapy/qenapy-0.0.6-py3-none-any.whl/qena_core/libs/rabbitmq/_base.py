"""
Provides a base rabbitmq class

Classes:
- `RabbitMQ`: Manages connection and channel initialization.
"""

from asyncio import (
    get_running_loop,
    iscoroutinefunction,
    new_event_loop,
    set_event_loop,
)
from functools import partial
from typing import Callable, Dict, List, Type

from click import style
from pika.adapters.asyncio_connection import AsyncioConnection

from libs.logger import get_logger
from libs.rabbitmq._connector import Connector
from libs.rabbitmq._listener import Consumer, ListenerContext, RpcWorker
from libs.rabbitmq._publisher import Publisher
from libs.rabbitmq._rpc_client import RpcRequestManager


class RabbitMQ:
    """
    Manages connection and channel initialization.
    """

    def __init__(self):
        self.__consumers: List[Consumer] = []
        self.__workers: List[RpcWorker] = []
        self.__exception_handlers: Dict[Type[BaseException], Callable] = {}
        self.__logger = get_logger()

    def include_consumer(self, consumer: Consumer):
        """
        Register a rabbitmq message consumer.
            :param Consumer consumer: the consumer to be registered.
        """
        if not isinstance(consumer, Consumer):
            raise TypeError("Not valid consumer")
        if self.__consumer_exists(consumer.queue):
            raise ValueError(
                f'Consumer with the same queue "{consumer.queue}" exists.'
            )

        self.__consumers.append(consumer)

    def __consumer_exists(self, queue: str):
        for consumer in self.__consumers:
            if consumer.queue == queue:
                return True

        return False

    def include_worker(self, worker: RpcWorker):
        """
        Register a rabbitmq rpc worker.
            :param RpcWorker worker: the rpc worker to be registered.
        """
        if not isinstance(worker, RpcWorker):
            raise TypeError("Not valid rpc worker")
        if self.__worker_exists(worker.queue):
            raise ValueError(
                f'Consumer with the same queue "{worker.queue}" exists.'
            )

        self.__workers.append(worker)

    def __worker_exists(self, queue: str):
        for worker in self.__workers:
            if worker.queue == queue:
                return True

        return False

    def exception_handler(self, exception: Type[Exception]):
        """
        Register an exception handler for consumers or workers.
            Usage:
            ``` python
            rabbitmq = RabbitMQ()

            @rabbitmq.exception_handler(ValidationError)
            async def handler_validation_error(
                context: ConsumerContext,
                exception: ValidationError
            ):
                pass
            ```
        """
        if not issubclass(exception, Exception):
            raise TypeError('exception should be "Exception" type or subclass')

        def wrapper(handler):
            registered_handler = self.__exception_handlers.get(exception)

            if registered_handler is not None:
                raise ValueError(
                    f"handler for {exception} is already registered"
                )

            self.__exception_handlers[exception] = handler

        return wrapper

    def __invoke_exception_handler(
        self, context: ListenerContext, exception: BaseException
    ):
        exception_handler = None

        for exception_type in self.__exception_handlers:
            if exception_type in type(exception).mro():
                exception_handler = self.__exception_handlers.get(
                    type(exception)
                )
                break

        if exception_handler is None:
            exception_handler = self.__exception_handlers.get(Exception)

        if exception_handler is not None:
            if iscoroutinefunction(exception_handler):
                self.__loop.create_task(exception_handler(context, exception))
            else:
                self.__loop.run_in_executor(
                    executor=None,
                    func=partial(exception_handler, context, exception),
                )
            return True

        return False

    def stop(self):
        """
        Stops the currently running rabbitmq instance.
        """
        self.__connector.disconnect()

    def start(self):
        """
        Opens a connection to rabbitmq server, and opens channel for listeners.
            :param Logger logger: instance of a standard logger
        """
        self.__logger = get_logger()

        try:
            self.__loop = get_running_loop()
        except RuntimeError:
            self.__loop = new_event_loop()
            set_event_loop(self.__loop)

        self.__connector = Connector(
            on_connection_open=self.__on_connection_opened
        )
        self.__connector.connect()

    def __on_connection_opened(self, connection: AsyncioConnection):
        self.__connection = connection

        host = self.__connection.params.host
        port = self.__connection.params.port
        virtual_host = self.__connection.params.virtual_host

        uri = f"amqp://{host}:{port}/{virtual_host}"

        self.__logger.info(
            msg=f'Connection opened to rabbitmq server "{uri}"',
            extra={
                "color_message": (
                    f"Connection opened to rabbitmq server "
                    f"\"{style(text=uri, fg='white', bold=True)}\""
                )
            },
        )

        for consumer in self.__consumers:
            consumer.open_channel(
                connection=self.__connection,
                on_exception_callback=self.__invoke_exception_handler,
            )

        for worker in self.__workers:
            worker.open_channel(
                connection=self.__connection,
                on_exception_callback=self.__invoke_exception_handler,
            )

        Publisher.start(connection=self.__connection)

        RpcRequestManager.start(connection=self.__connection)
