import json
import uuid


def parse_plan_json(plan_json):
    return __PlanParserDeco(plan_json)


class __PlanParserDeco:

    def __init__(self, plan_json):
        self.__plan = json.loads(plan_json)

    def set_plan_id(self, plan_id):
        self.__plan["plan_id"] = plan_id


    def get_plan_id(self):
        return self.__plan["plan_id"]


    def set_plan_as_new(self):
        self.__plan["plan_status"] = "INITIAL"


    def get_tasks(self):
        return self.__plan["tasks"]


    @staticmethod
    def task_get_id(task):
        return task["@id"]

    @staticmethod
    def task_get_name(task):
        return task["name"]

    @staticmethod
    def get_id():
        return str(uuid.uuid4())


    def set_plan_as_complete(self):
        self.__plan["plan_status"] = "COMPLETE"

    @staticmethod
    def is_task_complete(task):
        return task['task_status'] == "COMPLETE"

    @staticmethod
    def is_task_initial(task):
        return task['task_status'] == "INITIAL"

    @staticmethod
    def set_task_as_complete(task):
        task['task_status'] = "COMPLETE"

    @staticmethod
    def set_task_as_new(task):
        task['task_status'] = "INITIAL"

    @staticmethod
    def set_task_as_running(task):
        task['task_status'] = "RUNNING"

    @staticmethod
    def get_task_id(task):
        return task["@id"]


    def get_dependencies(self):
        return self.__plan["dependencies"]

    @staticmethod
    def get_dependency_from(dep):
        return dep["from"]

    @staticmethod
    def get_dependency_to(dep):
        return dep["to"]
