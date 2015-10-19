from abc import ABCMeta, abstractmethod
import logging
import pykka
import plan_repo

logger = logging.getLogger(__name__)


def execute_task(plan_executor, plan_id, task_id, task_starter, task_listener):
    logger.debug("Called execute_task for plan {0}, task {1}".format(plan_id, task_id))
    plan_repo.set_task_running(plan_id, task_id)
    _task_listener = task_listener if task_listener else SimpleTaskListener()
    _task_starter = task_starter if task_starter else SimpleTaskStarter()
    task_executor = TaskExecutor.start(
        plan_exec=plan_executor,
        task_starter=_task_starter,
        task_listener=_task_listener
    ).proxy()
    task_executor.execute_task(plan_id, task_id)


class TaskExecutor(pykka.ThreadingActor):
    def __init__(self, plan_exec, task_starter, task_listener):
        super(TaskExecutor, self).__init__()
        self.plan_exec = plan_exec
        self.__task_starter = task_starter
        self.__task_listener = task_listener


    def execute_task(self, plan_id, task_id):
        self.__task_starter.start_task(plan_id, task_id)
        self.__task_listener.create_listener(plan_id, task_id, self.plan_exec)
        self.stop()


# Abstract class to be inherited by task starters
class BaseTaskStarter:
    def __init__(self):
        pass

    __metaclass__ = ABCMeta

    @abstractmethod
    def start_task(self, plan_id, task_id):
        pass


# Default task starter when none is provided
class SimpleTaskStarter(BaseTaskStarter):
    def __init__(self):
        super(SimpleTaskStarter, self).__init__()
        self.__logger = logging.getLogger(__name__)


    def start_task(self, plan_id, task_id):
        self.__logger.debug("Calling start_task on {0}, task {1}". format(plan_id, task_id))


# Abstract class to be inherited by task complete listeners
# Has to call self.task_completed(plan_id, task_id) eventually
class BaseTaskListener:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_listener(self, plan_id, task_id, plan_executor):
        pass

    @staticmethod
    def task_completed(plan_executor, plan_id, task_id):
        plan_executor.task_complete(plan_id, task_id)


# Default task listener when none is provided
class SimpleTaskListener(BaseTaskListener):
    def __init__(self):
        super(SimpleTaskListener, self).__init__()

    def create_listener(self, plan_id, task_id, plan_executor):
        self.logger.debug("Calling create_listener on {0}, task {1}". format(plan_id, task_id))
        self.logger.debug("...and completing straight away")
        self.task_completed(plan_executor, plan_id, task_id)

