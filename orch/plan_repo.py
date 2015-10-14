class PlanRepo:

    def __init__(self, **kwargs):
        self.plan_parser = kwargs['plan_parser']
        self.plans = []


    def save_new_plan(self, plan_json):
        plan = self.plan_parser.parse_plan_json(plan_json)
        plan_id = self.plan_parser.get_id()
        self.plan_parser.set_plan_id(plan, plan_id)
        self.plan_parser.set_plan_status_as_new(plan)
        self.plans.append(plan)
        return plan_id


    def set_task_complete(self, plan_id, task_id):
        # TODO impement this method
        True


    def get_ready_tasks_for_plan(self, plan_id):
        '''
        Returns task_ids for plan_id that are ready for execution.

        :param plan_id:
        :return:
        '''
        # TODO implement this method
        return ["1","2","3"]


    def get_task_name(self, plan_id, task_id):
        for plan in self.plans:
            if self.plan_parser.get_plan_id(plan) == plan_id:
                for task in self.plan_parser.get_tasks(plan):
                    if self.plan_parser.task_get_id(task) == task_id:
                        return self.plan_parser.task_get_name(task)


    def are_all_tasks_complete(self, plan_id):
        # TODO implement this method
        False

    def set_plan_complete(self, plan_id):
        plan = [x for x in self.plans if self.plan_parser.get_plan_id(x) == plan_id][0]
        self.plan_parser.set_plan_complete(plan)