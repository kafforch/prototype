import logging
import pykka
import task_exec
import plan_repo


def execute_plan(plan_id, task_starter=None, task_listener=None):
    logger = logging.getLogger(__name__)

    logger.debug("Called execute_plan for {0}".format(plan_id))
    plan_repo.set_plan_as_running(plan_id)
    ready_task_ids = plan_repo.initial_get_ready_tasks_for_plan(plan_id)

    plan_executor = PlanExecutor(
            task_starter=task_starter,
            task_listener=task_listener
    ).proxy()

    plan_executor.start()

    for task_id in ready_task_ids:
        task_exec.execute_task(plan_executor, plan_id, task_id, task_starter, task_listener)


def execute_task(plan_id, task_id):
    plan = plan_repo.get_plan_by_id(plan_id)
    if plan.is_running():
        task = plan.get_task_by_id(task_id)


class PlanExecutor(pykka.ThreadingActor):
    def __init__(self, task_starter, task_listener):
        super(PlanExecutor, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__task_starter = task_starter
        self.__task_listener = task_listener

    # method that returns proxy - pykka defect #48
    def proxy(self):
        return self.actor_ref.proxy()

    def task_complete(self, plan_id, task_id):
        self.__logger.debug("Called task_complete for plan {0}, task {1}".format(plan_id, task_id))
        plan_repo.set_task_complete(plan_id, task_id)

        if plan_repo.are_all_tasks_complete(plan_id):
            # Plan is complete
            plan_repo.set_plan_as_complete(plan_id)
            self.stop()
        else:
            # Execute dependent tasks
            for dep_task_id in plan_repo.get_ready_dependent_tasks(plan_id, task_id):
                task_exec.execute_task(self, plan_id, dep_task_id, self.__task_starter, self.__task_listener)

