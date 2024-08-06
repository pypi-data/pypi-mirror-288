"""
Module holding class for scheduler

Classes:
- `Scheduler`: A class to help organize related scheduled tasks.
- `ScheduleManager`: Management class to register scheduled tasks.
"""

from asyncio import (
    Future,
    InvalidStateError,
    Task,
    get_running_loop,
    iscoroutinefunction,
    sleep,
)
from datetime import datetime
from fcntl import LOCK_EX, LOCK_NB, lockf
from typing import List, Optional, Union
from zoneinfo import ZoneInfo

from click import style
from cronsim import CronSim

from app.core.libs.logger import get_logger


class Scheduler:
    """
    A class to help organize related scheduled tasks.
    """

    def __init__(self):
        self.__tasks: List[dict] = []

    def schedule(self, cron_expression: str, timezone: Optional[str] = None):
        """
        Decorate a task to run in a specified interval.
            usage:
                ``` python
                scheduler = Scheduler()

                @scheduler.schedule(
                    cron_expression="30 12 * * *",
                    timezone=\"Africa/Addis_Ababa\"
                )
                async def test_task():
                    ...
                ```
        """

        def wrapper(task):
            self.__tasks.append(
                {
                    "task": task,
                    "cron_expression": cron_expression,
                    "zone_info": ZoneInfo(timezone)
                    if timezone
                    else datetime.now().tzinfo,
                    "next_run_in": None,
                    "ran": False,
                }
            )

        return wrapper

    @property
    def tasks(self):
        return self.__tasks


class ScheduleManager:
    """
    Management class to register scheduled tasks.
    """

    def __init__(self):
        self.__logger = get_logger()
        self.__tasks: List[dict] = []
        self.__next_run_in = None

    def start(self):
        if not self.__aquired_lock():
            return self.__logger.warning("a scheduler is already running")

        self.__loop = get_running_loop()

        task_count = len(self.__tasks)
        if task_count > 1:
            tasks_or_task = "tasks"
        else:
            tasks_or_task = "task"

        self.__logger.info(
            msg=(
                "Scheduler has started :: "
                f"[{task_count} {tasks_or_task} scheduled]"
            )
        )

        if task_count == 0:
            return

        self.__loop.create_task(self.__run_scheduler()).add_done_callback(
            self.__on_scheduler_done
        )

    def __on_scheduler_done(self, task: Task):
        try:
            e = task.exception()
            if e is not None:
                self.__logger.error(
                    msg=f"Unable to start scheduler :: [{e}]",
                    extra={
                        "color_message": (
                            "Unable to start scheduler :: "
                            f"[{style(e, fg='red', bold=True)}]"
                        )
                    },
                )
        except InvalidStateError:
            self.__logger.info("Scheduler stopping")

    def __aquired_lock(self):
        try:
            self.__fd = open(file="scheduler.lock", mode="w+", encoding="utf-8")
            lockf(self.__fd, LOCK_EX | LOCK_NB)
        except OSError:
            return False

        return True

    async def __run_scheduler(self):
        while True:
            self.__calculate_next_schedule()

            await sleep(self.__next_run_in or 0)

            for task in self.__tasks:
                if task["next_run_in"] != self.__next_run_in:
                    continue

                if iscoroutinefunction(task["task"]):
                    self.__loop.create_task(task["task"]()).add_done_callback(
                        self.__on_task_done
                    )
                else:
                    self.__loop.run_in_executor(
                        executor=None, func=task["task"]
                    ).add_done_callback(self.__on_task_done)
                task["ran"] = True

    def __on_task_done(self, task_or_future: Union[Task, Future]):
        try:
            e = task_or_future.exception()
            if e is not None:
                self.__logger.error(
                    msg=f"Exception occured while executing task :: [{e}]",
                    extra={
                        "color_message": (
                            "Exception occured while executing task :: "
                            f"[{style(e, fg='red', bold=True)}]"
                        )
                    },
                )
        except InvalidStateError:
            ...

    def __calculate_next_schedule(self):
        prev_run_in = self.__next_run_in or 0
        self.__next_run_in = None

        for task in self.__tasks:
            if not task["ran"] and task["next_run_in"] is not None:
                task["next_run_in"] = task["next_run_in"] - prev_run_in

                if (
                    self.__next_run_in is not None
                    and task["next_run_in"] < self.__next_run_in
                ) or self.__next_run_in is None:
                    self.__next_run_in = task["next_run_in"]
                continue

            current_datetime = datetime.now(tz=task["zone_info"])
            next_datetime = next(
                CronSim(
                    expr=task["cron_expression"],
                    dt=datetime.now(tz=task["zone_info"]),
                )
            )

            next_run_in = (next_datetime - current_datetime).seconds

            if next_run_in == 0:
                continue

            if self.__next_run_in is None or next_run_in < self.__next_run_in:
                self.__next_run_in = next_run_in

            task["next_run_in"] = next_run_in
            task["ran"] = False

    def include_sheduler(self, scheduler: Scheduler):
        self.__tasks.extend(scheduler.tasks)

        return self
