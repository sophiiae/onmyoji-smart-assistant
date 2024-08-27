
from functools import cached_property
from datetime import datetime, timedelta
from multiprocessing import Queue
from pathlib import Path
import time

import inflection

from module.base.logger import logger
from module.base.exception import RequestHumanTakeover, TaskEnd
from module.config.config import Config
from module.server.device import Device
from script.utils import load_module


class Script:

    def __init__(self, config_name: str = 'oas') -> None:
        self.config_name = config_name
        self.state_queue: Queue = None
        # Key: str, task name, value: int, failure count
        self.failure_record = {}

    @cached_property
    def config(self) -> "Config":
        try:
            from module.config.config import Config
            config = Config(config_name=self.config_name)
            return config
        except RequestHumanTakeover:
            logger.critical('Request human takeover')
            exit(1)
        except Exception as e:
            logger.exception(e)
            exit(1)

    @cached_property
    def device(self) -> "Device":
        try:
            from module.server.device import Device
            device = Device(config=self.config)
            return device
        except RequestHumanTakeover:
            logger.critical('Request human takeover')
            exit(1)
        except Exception as e:
            logger.exception(e)
            exit(1)

    def run(self, name: str) -> bool:
        """

        :param name:  大写驼峰命名的任务名字
        :return:
        """
        if name == 'start' or name == 'goto_main':
            logger.error(f'Invalid task: `{name}`')
            return False

        try:
            self.device.screenshot()
            module_name = 'task_script'
            module_path = str(Path.cwd() / 'tasks' /
                              name / (module_name + '.py')
                              )
            logger.info(f'module_path: {
                        module_path}, module_name: {module_name}')
            task_module = load_module(module_name, module_path)
            task_module.TaskScript(
                config=self.config,
                device=self.device
            ).run()
        except TaskEnd:
            self.config.task_call(name)
            return True

    def start(self):
        logger.info(f'Start scheduler loop: {self.config_name}')

        while 1:
            # Get task
            task = self.get_next_task()

            # Run
            logger.info(f'Scheduler: Start task `{task}`')
            success = self.run(inflection.underscore(task))
            print(inflection.underscore(task))

            logger.info(f'Scheduler: End task `{task}`')

            # Check failures
            # failed = deep_get(self.failure_record, keys=task, default=0)
            failed = self.failure_record[task] if task in self.failure_record else 0
            failed = 0 if success else failed + 1
            # deep_set(self.failure_record, keys=task, value=failed)
            self.failure_record[task] = failed
            if failed >= 3:
                logger.critical(f"Task `{task}` failed 3 or more times.")
                logger.critical("Possible reason #1: You haven't used it correctly. "
                                "Please read the help text of the options.")
                logger.critical("Possible reason #2: There is a problem with this task. "
                                "Please contact developers or try to fix it yourself.")
                logger.critical('Request human takeover')
                exit(1)

            if success:
                del self.config
                continue
            elif self.config.script.error.handle_error:
                del self.config
                continue
            else:
                break

    def wait_until(self, future):
        """
        Wait until a specific time.

        Args:
            future (datetime):

        Returns:
            bool: True if wait finished, False if config changed.
        """
        future = future + timedelta(seconds=1)
        self.config.start_watching()
        while 1:
            if datetime.now() > future:
                return True

            time.sleep(5)

            if self.config.should_reload():
                return False

    def get_next_task(self) -> str:
        """
        获取下一个任务的名字, 大驼峰。
        :return:
        """
        while 1:
            task = self.config.get_next()
            self.config.task = task
            if self.state_queue:
                self.state_queue.put(
                    {"schedule": self.config.get_schedule_data()}
                )

            if task.next_run > datetime.now():
                logger.info(f'Wait until {task.next_run} for task `{
                            task.name}`')

                logger.info('Goto main page during wait')
                self.run('GotoMain')
                self.device.release_during_wait()
                if not self.wait_until(task.next_run):
                    del self.config
                    continue
            break

        return task.name
