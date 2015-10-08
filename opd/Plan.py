class Plan():

    def __init__(self):
        tasks = []
        dependencies = []

    def add_tasks(self, in_tasks):
        for task in in_tasks:
            self.tasks.add(task)

    def add_dependencies(self, in_dependencies):
        for dep in in_dependencies:
            self.dependencies.add(dep)