"""
Used to add background tasks to the asyncio eventloop
with a specific id.
"""

from asyncio import (
    AbstractEventLoop,
    Event,
    Queue,
    Task,
    create_task,
    gather,
    get_running_loop,
    new_event_loop,
    set_event_loop,
)
from typing import Dict, Optional
from uuid import uuid4

from starlette.background import BackgroundTask

from app.core.libs.logger import get_logger
from app.core.libs.logstash import Logstash
from app.core.libs.singleton import Singleton


class Background(metaclass=Singleton):
    """
    Background task runner class.
    """

    def __init__(self) -> None:
        self.__queue = Queue()
        self.__stop_event = Event()
        self.__loop: AbstractEventLoop  # type: ignore
        self.__logger = get_logger()
        self.__logstash = Logstash()
        self.__tasks: Dict[str, Task] = {}

    def _set_event_loop(self):
        try:
            self.__loop = get_running_loop()
        except RuntimeError:
            self.__loop = new_event_loop()
            set_event_loop(self.__loop)

    async def _task_manager(
        self, task: BackgroundTask, task_id: Optional[str] = None
    ):
        self.__logger.info(
            "running %s: %s with %s", task_id, task.func.__name__, task.args
        )

        if task_id is None:
            # set new task id by generating a new uuid
            task_id = str(uuid4())

        try:
            self.__tasks[task_id] = create_task(
                task.func(*task.args, **task.kwargs)
            )
            await self.__tasks[task_id]
        # disable Catching too general exception because we don't know
        # the task we are running
        except Exception:  # pylint: disable=W0718
            self.__logstash.error(
                "exception occured when running background task "
                f"{task.func.__name__} with id {task_id}"
            )
        finally:
            self.__logger.info("finished running %s", task.func.__name__)
            self.__tasks.pop(task_id, None)

    def _run(self, task: BackgroundTask, task_id: Optional[str] = None):
        if not self.__stop_event.is_set() and (
            task_id is None or task_id not in self.__tasks
        ):
            self.__loop.create_task(self._task_manager(task, task_id))

    async def _run_tasks(self):
        while not self.__stop_event.is_set() or not self.__queue.empty():
            task = await self.__queue.get()
            if task is None:
                break

            self._run(task[0], task[1])

        tasks = [t for _, t in self.__tasks.items() if not t.done()]
        await gather(*tasks)

    def add_task(self, task: BackgroundTask, task_id: Optional[str] = None):
        self.__queue.put_nowait((task, task_id))

    def start(self):
        self._set_event_loop()
        self.__loop.create_task(self._run_tasks())

    def stop(self):
        self.__stop_event.set()
        self.__queue.put_nowait(None)

    def is_alive(self, task_id: str):
        if task_id in self.__tasks and not self.__tasks[task_id].done():
            return True
        return False

    def count(self):
        return len(self.__tasks)
