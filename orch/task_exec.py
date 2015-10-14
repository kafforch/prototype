class TaskExec:

    def __init__(self, **kwargs):
        self.plan_repo = kwargs['plan_repo']
        self.event_mgr = kwargs['event_mgr']

    def execute_task(self, plan_id, task_id):
        task_name = self.plan_repo.get_task_name(plan_id, task_id)
        self.event_mgr.publish(task_id=task_id, task_name=task_name, event="START_TASK")
