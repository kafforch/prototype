import pykka
import task_exec
import plan_repo


class PlanExecutor(pykka.ThreadingActor):
    def __init__(self):
        super(PlanExecutor, self).__init__()


    def execute_plan(self, plan_id):
        print "Called execute_plan for {0}".format(plan_id)
        ready_task_ids = plan_repo.initial_get_ready_tasks_for_plan(plan_id)

        for task_id in ready_task_ids:
            task_executor = task_exec.TaskExecutor.start(plan_exec=self).proxy()
            task_executor.execute_task(plan_id, task_id)


    def task_complete(self, plan_id, task_id):
        print "Called task_complete for plan {0}, task {1}".format(plan_id, task_id)
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

