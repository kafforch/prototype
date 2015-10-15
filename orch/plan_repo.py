class PlanRepo:

    def __init__(self, **kwargs):
        self.plan_parser = kwargs['plan_parser']
        self.plans = []


    def save_new_plan(self, plan_json):
        plan = self.plan_parser.parse_plan_json(plan_json)
        plan_id = self.plan_parser.get_id()
        self.plan_parser.set_plan_id(plan, plan_id)
        self.plan_parser.set_plan_as_new(plan)

        for task in self.plan_parser.get_tasks(plan):
            self.plan_parser.set_task_as_new(task)

        self.plans.append(plan)
        return plan_id


    def set_task_running(self, plan_id, task_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = self.plan_parser.get_tasks(plan)
        for task in tasks:
            if task_id == self.plan_parser.get_task_id(task):
                self.plan_parser.set_task_as_running(task)
                return


    def set_task_complete(self, plan_id, task_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = self.plan_parser.get_tasks(plan)
        for task in tasks:
            if task_id == self.plan_parser.get_task_id(task):
                self.plan_parser.set_task_as_complete(task)
                return


    def get_ready_tasks_for_plan(self, plan_id):
        '''
        Returns task_ids for plan_id that are ready for execution.

        :param plan_id:
        :return: task_ids of tasks ready to run.
        '''
        # TODO implement this method
        return ["2","3","1"]


    def get_task_name(self, plan_id, task_id):
        for plan in self.plans:
            if self.plan_parser.get_plan_id(plan) == plan_id:
                for task in self.plan_parser.get_tasks(plan):
                    if self.plan_parser.task_get_id(task) == task_id:
                        return self.plan_parser.task_get_name(task)


    def are_all_tasks_complete(self, plan_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = self.plan_parser.get_tasks(plan)
        for task in tasks:
            if not self.plan_parser.is_task_complete(task):
                return False
        return True


    def set_plan_as_complete(self, plan_id):
        plan = self.get_plan_by_id(plan_id)
        self.plan_parser.set_plan_as_complete(plan)


    def get_plan_by_id(self, plan_id):
        matching_plans = [x for x in self.plans if self.plan_parser.get_plan_id(x) == plan_id]
        if len(matching_plans):
            return matching_plans[0]
        else:
            raise ValueError("Plan {0} not found".format(plan_id))