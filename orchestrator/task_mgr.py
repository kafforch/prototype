class TaskManager:

    # Singleton
    __shared_state = dict(
    )


    def __init__(self):
        self.__dict__ = self.__shared_state


    def execute_tasks(self, plan_id, tasks, dependencies):
        return 0