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

        ready_tasks = self.plan_repo.get_ready_tasks_for_plan(plan_id)

        for task in ready_tasks:
            self.task_exec.execute_task(task)


