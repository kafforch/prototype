import uuid


class PlanRepo:

    def __init__(self, **kwargs):
        self.plan_parser = kwargs['plan_parser']
        self.plans = []


    def get_id(self):
        return uuid.uuid4()


    def save_plan(self, plan_json):
        plan = self.plan_parser.parse_plan_json(plan_json)
        plan_id = str(self.get_id())
        plan = self.plan_parser.set_plan_id(plan, plan_id)
        self.plans.append(plan)
        return plan_id


    def set_task_complete(self, plan_id, task_id):
        # TODO impement this method
        True


    def get_ready_tasks_for_plan(self, plan_id):
        '''
        Returns tasks for plan_id that are ready for execution.

        :param plan_id:
        :return:
        '''
        # TODO implement this method
        return [1,2,3]


    def get_task_name(self, plan_id, task_id):
        # TODO implement this method
        return 12


    def are_all_tasks_complete(self, plan_id):
        # TODO implement this method
        False

    def set_plan_complete(self, plan_id):
        # TODO implement this method
        True