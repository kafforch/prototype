class PlanExec:

    def __init__(self, **kwargs):
        self.plan_repo = kwargs['plan_repo']
        self.task_exec = kwargs['task_exec']

    def execute_plan(self, plan_id):
        '''
        Orchestrates execution of the tasks ready for execution.

        :param plan_id:
        :return:
        '''

        ready_task_ids = self.plan_repo.get_ready_tasks_for_plan(plan_id)

        for task_id in ready_task_ids:
            self.task_exec.execute_task(plan_id, task_id)


