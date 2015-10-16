class PlanRepo:
    def __init__(self, plan_parser, **kwargs):
        self.__plan_parser = plan_parser
        self.__plans = []

    def save_new_plan(self, plan_json):
        plan = self.__plan_parser.parse_plan_json(plan_json)
        plan_id = plan.get_id()
        plan.set_plan_id(plan_id)
        plan.set_plan_as_new()

        for task in plan.get_tasks():
            plan.set_task_as_new(task)

        self.__plans.append(plan)
        return plan_id

    def set_task_running(self, plan_id, task_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = plan.get_tasks()
        for task in tasks:
            if task_id == plan.get_task_id(task):
                plan.set_task_as_running(task)
                return

    def set_task_complete(self, plan_id, task_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = plan.get_tasks()
        for task in tasks:
            if task_id == plan.get_task_id(task):
                plan.set_task_as_complete(task)
                return

    def initial_get_ready_tasks_for_plan(self, plan_id):
        """
        Returns task_ids for plan_id that are ready for execution initially.

        :param plan_id:
        :return: task_ids of tasks ready to run.
        """

        task_ids = []

        plan = self.get_plan_by_id(plan_id)
        tasks = plan.get_tasks()

        for task in tasks:
            if plan.is_task_initial(task) and len(self.get_ready_tasks_for_plan(plan, task)) == 0:
                task_ids.append(plan.get_task_id(task))

        return task_ids

    def get_ready_tasks_for_plan(self, plan, task):
        predecessors = []
        task_id = plan.get_task_id(task)

        for dependency in plan.get_dependencies():
            dependency_id = plan.get_dependency_to(dependency)
            if dependency_id == task_id:
                predecessors.append(plan.get_dependency_from(dependency))

        return predecessors

    def all_dependencies_complete_for_task(self, plan, task_id):
        dependencies = plan.get_dependencies()
        for dependency in dependencies:
            from_task_id = plan.get_dependency_from(dependency)
            from_task = self.get_task_by_id(plan, from_task_id)
            if plan.get_dependency_to(dependency) == task_id and \
                    not plan.is_task_complete(from_task):
                return False

        return True

    def get_ready_dependent_tasks(self, plan_id, task_id):
        task_ids = []
        plan = self.get_plan_by_id(plan_id)

        for dependency in plan.get_dependencies():
            if plan.get_dependency_from(dependency) == task_id:
                dep_task_id = plan.get_dependency_to(dependency)
                dep_task = self.get_task_by_id(plan, dep_task_id)
                if plan.is_task_initial(dep_task) and \
                        self.all_dependencies_complete_for_task(plan, dep_task_id):
                    task_ids.append(dep_task_id)

        return task_ids

    def get_task_by_id(self, plan, task_id):
        for task in plan.get_tasks():
            if plan.get_task_id(task) == task_id:
                return task

    def get_task_name(self, plan_id, task_id):
        for plan in self.__plans:
            if plan.get_plan_id() == plan_id:
                for task in plan.get_tasks():
                    if plan.task_get_id(task) == task_id:
                        return plan.task_get_name(task)

    def are_all_tasks_complete(self, plan_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = plan.get_tasks()
        for task in tasks:
            if not plan.is_task_complete(task):
                return False
        return True

    def set_plan_as_complete(self, plan_id):
        plan = self.get_plan_by_id(plan_id)
        plan.set_plan_as_complete()

    def get_plan_by_id(self, plan_id):
        matching_plans = [x for x in self.__plans if x.get_plan_id() == plan_id]
        if len(matching_plans):
            return matching_plans[0]
        else:
            raise ValueError("Plan {0} not found".format(plan_id))
