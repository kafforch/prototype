class TaskManager:

    # Singleton
    __shared_state = dict(
        tasks={},
        dependencies={}
    )


    def __init__(self):
        self.__dict__ = self.__shared_state


    def get_tasks_for_plan(self, plan_id):
        try:
            return self.tasks[plan_id]
        except KeyError:
            return []


    def get_dependencies_for_plan(self, plan_id):
        try:
            return self.dependencies[plan_id]
        except KeyError:
            return []


    def submit_tasks(self, plan_id, tasks, dependencies):

        try:
            self.tasks[plan_id].update(tasks)
        except KeyError:
            self.tasks[plan_id] = []

        try:
            self.dependencies[plan_id].update(dependencies)
        except KeyError:
            self.dependencies[plan_id] = []


    def trigger_execution(self):
        return 0