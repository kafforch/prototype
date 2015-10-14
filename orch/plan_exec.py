class PlanExec:

    def __init__(self, **kwargs):
        self.plan_repo = kwargs['plan_repo']
        self.event_mgr = kwargs['event_mgr']

    def execute_plan(self, plan_id, complete_callback=None):
        '''
        Orchestrates execution of the tasks ready for execution.

        :param plan_id:
        :return:
        '''

        ready_task_ids = self.plan_repo.get_ready_tasks_for_plan(plan_id)

        for task_id in ready_task_ids:
            self.execute_task(plan_id, task_id, complete_callback)


    def empty_callback(self, a1, a2, a3):
        True


    def execute_task(self, plan_id, task_id, callback=None):
        task_name = self.plan_repo.get_task_name(plan_id, task_id)

        # subscribe to get notified on task completion
        if callback:
            self.event_mgr.subscribe("plan_exec", "END_TASK", callback)
        else:
            self.event_mgr.subscribe("plan_exec", "END_TASK", self.empty_callback)

        self.event_mgr.publish(data=dict(
                                        plan_id=plan_id,
                                        task_id=task_id,
                                        task_name=task_name
                                    ), event="START_TASK" )
