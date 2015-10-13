class TaskManager:

    # Singleton
    __shared_state = dict(
    )


    def __init__(self):
        self.__dict__ = self.__shared_state


    def execute(self, tasks, dependencies):
        return 0