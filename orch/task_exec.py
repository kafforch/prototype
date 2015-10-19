from abc import ABCMeta, abstractmethod
import logging
import pykka
import plan_repo

logger = logging.getLogger(__name__)


def execute_task(plan_executor, plan_id, task_id, task_starter=None):
    logger.debug("Called execute_task for plan {0}, task {1}".format(plan_id, task_id))
    plan_repo.set_task_running(plan_id, task_id)
    _task_starter = task_starter if task_starter else SimpleTaskStarter()
    task_executor = TaskExecutor.start(
        plan_exec=plan_executor,
        task_starter=_task_starter
    ).proxy()
    task_executor.execute_task(plan_id, task_id)


class TaskExecutor(pykka.ThreadingActor):

    def __init__(self, plan_exec, task_starter):
        super(TaskExecutor, self).__init__()
        self.__plan_exec = plan_exec
        self.__task_starter = task_starter

    def execute_task(self, plan_id, task_id):
        self.__task_starter.start_task(plan_id, task_id)

        self.__plan_exec.task_complete(plan_id, task_id)

        self.stop()
        # TODO complete this, but now just perform callback


# Abstract class to be inherited by task starters
class BaseTaskStarter:
    def __init__(self):
        pass

    __metaclass__ = ABCMeta

    @abstractmethod
    def start_task(self, plan_id, task_id, **kwargs):
        pass


# Default task starter when none is provided
class SimpleTaskStarter(BaseTaskStarter):
    def __init__(self):
        super(SimpleTaskStarter, self).__init__()
        self.__logger = logging.getLogger(__name__)


    def start_task(self, plan_id, task_id, **kwargs):
        self.__logger.info("Calling start_task on {0}, task {1}". format(plan_id, task_id))
