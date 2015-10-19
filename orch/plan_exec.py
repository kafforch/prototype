import logging
import pykka
import task_exec
import plan_repo


def execute_plan(plan_id):
    logger = logging.getLogger(__name__)

    logger.debug("Called execute_plan for {0}".format(plan_id))
    ready_task_ids = plan_repo.initial_get_ready_tasks_for_plan(plan_id)

    plan_executor = PlanExecutor.start().proxy()

    for task_id in ready_task_ids:
        task_executor = task_exec.TaskExecutor.start(plan_exec=plan_executor).proxy()
        task_executor.execute_task(plan_id, task_id)


class PlanExecutor(pykka.ThreadingActor):
    def __init__(self):
        super(PlanExecutor, self).__init__()
        self.__logger = logging.getLogger(__name__)

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
                task_executor = task_exec.TaskExecutor.start(plan_exec=self).proxy()
                task_executor.execute_task(plan_id, dep_task_id)

