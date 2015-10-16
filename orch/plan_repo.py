class PlanRepo:
    def __init__(self, plan_parser, **kwargs):
        self.__plan_parser = plan_parser
        self.__plans = []

    def save_new_plan(self, plan_json):
        plan = self.__plan_parser.parse_plan_json(plan_json)
        plan_id = self.__plan_parser.get_id()
        self.__plan_parser.set_plan_id(plan, plan_id)
        self.__plan_parser.set_plan_as_new(plan)

        for task in self.__plan_parser.get_tasks(plan):
            self.__plan_parser.set_task_as_new(task)

        self.__plans.append(plan)
        return plan_id

    def set_task_running(self, plan_id, task_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = self.__plan_parser.get_tasks(plan)
        for task in tasks:
            if task_id == self.__plan_parser.get_task_id(task):
                self.__plan_parser.set_task_as_running(task)
                return

    def set_task_complete(self, plan_id, task_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = self.__plan_parser.get_tasks(plan)
        for task in tasks:
            if task_id == self.__plan_parser.get_task_id(task):
                self.__plan_parser.set_task_as_complete(task)
                return

    def initial_get_ready_tasks_for_plan(self, plan_id):
        """
        Returns task_ids for plan_id that are ready for execution initially.

        :param plan_id:
        :return: task_ids of tasks ready to run.
        """

        task_ids = []

        plan = self.get_plan_by_id(plan_id)
        tasks = self.__plan_parser.get_tasks(plan)

        for task in tasks:
            if self.__plan_parser.is_task_initial(task) and len(self.task_predecessors(plan, task)) == 0:
                task_ids.append(self.__plan_parser.get_task_id(task))

        return task_ids

    def task_predecessors(self, plan, task):
        predecessors = []
        task_id = self.__plan_parser.get_task_id(task)

        for dependency in self.__plan_parser.get_dependencies(plan):
            dependency_id = self.__plan_parser.get_dependency_to(dependency)
            if dependency_id == task_id:
                predecessors.append(self.__plan_parser.get_dependency_from(dependency))

        return predecessors

    def all_dependencies_complete_for_task(self, plan, task_id):
        dependencies = self.__plan_parser.get_dependencies(plan)
        for dependency in dependencies:
            from_task_id = self.__plan_parser.get_dependency_from(dependency)
            from_task = self.get_task_by_id(plan, from_task_id)
            if self.__plan_parser.get_dependency_to(dependency) == task_id and \
                    not self.__plan_parser.is_task_complete(from_task):
                return False

        return True

    def get_ready_dependent_tasks(self, plan_id, task_id):
        task_ids = []
        plan = self.get_plan_by_id(plan_id)

        for dependency in self.__plan_parser.get_dependencies(plan):
            if self.__plan_parser.get_dependency_from(dependency) == task_id:
                dep_task_id = self.__plan_parser.get_dependency_to(dependency)
                dep_task = self.get_task_by_id(plan, dep_task_id)
                if self.__plan_parser.is_task_initial(dep_task) and \
                        self.all_dependencies_complete_for_task(plan, dep_task_id):
                    task_ids.append(dep_task_id)

        return task_ids

    def get_task_by_id(self, plan, task_id):
        for task in self.__plan_parser.get_tasks(plan):
            if self.__plan_parser.get_task_id(task) == task_id:
                return task

    def get_task_name(self, plan_id, task_id):
        for plan in self.__plans:
            if self.__plan_parser.get_plan_id(plan) == plan_id:
                for task in self.__plan_parser.get_tasks(plan):
                    if self.__plan_parser.task_get_id(task) == task_id:
                        return self.__plan_parser.task_get_name(task)

    def are_all_tasks_complete(self, plan_id):
        plan = self.get_plan_by_id(plan_id)
        tasks = self.__plan_parser.get_tasks(plan)
        for task in tasks:
            if not self.__plan_parser.is_task_complete(task):
                return False
        return True

    def set_plan_as_complete(self, plan_id):
        plan = self.get_plan_by_id(plan_id)
        self.__plan_parser.set_plan_as_complete(plan)

    def get_plan_by_id(self, plan_id):
        matching_plans = [x for x in self.__plans if self.__plan_parser.get_plan_id(x) == plan_id]
        if len(matching_plans):
            return matching_plans[0]
        else:
            raise ValueError("Plan {0} not found".format(plan_id))
