class Plan():

    def __init__(self, tasks=[], dependencies=[]):
        self.tasks = tasks
        self.dependencies = dependencies

    def add_tasks(self, in_tasks):
        self.tasks.extend(in_tasks)

    def add_task(self, task):
        self.tasks.append(task)

    def add_dependencies(self, in_dependencies):
        self.dependencies.extend(in_dependencies)

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def get_tasks(self):
        return self.tasks