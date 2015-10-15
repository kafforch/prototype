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

        self.event_mgr.publish(data=dict(
                                        plan_id=plan_id
                                    ), event="START_PLAN" )

        for task_id in ready_task_ids:
            self.execute_task(plan_id, task_id, complete_callback)


    # Empty callback
    def _empty_callback(self, a1, a2, a3):
        True


    def task_complete(self, id, event, data):
        '''
        Callback on completed events. Sets the completed task in the plan and checks if the plan can be marked completed.
        :param id: Subscriber id
        :param event: Event pubslished
        :param data: Dictionary with event data
        :return:
        '''
        self.plan_repo.set_task_complete(data['plan_id'], data['task_id'])

        if self.plan_repo.are_all_tasks_complete(data['plan_id']):
            self.plan_repo.set_plan_as_complete(data['plan_id'])
            self.event_mgr.publish(data=dict(
                                        plan_id=data["plan_id"]
                                    ), event="END_PLAN" )


    def execute_task(self, plan_id, task_id, callback=None):
        task_name = self.plan_repo.get_task_name(plan_id, task_id)

        # create subscription to update task status to complete
        self.event_mgr.subscribe("plan_exec", "END_TASK", self.task_complete)

        # subscribe to get notified on task completion with customer provided callback
        if callback:
            self.event_mgr.subscribe("custom_callback", "END_TASK", callback)
        else:
            self.event_mgr.subscribe("custom_callback", "END_TASK", self._empty_callback)

        self.plan_repo.set_task_running(plan_id, task_id)

        self.event_mgr.publish(data=dict(
                                        plan_id=plan_id,
                                        task_id=task_id,
                                        task_name=task_name
                                    ), event="START_TASK" )
