import json
import uuid


def parse_plan_json(plan_json):
    return json.loads(plan_json)


def set_plan_id(plan, plan_id):
    plan["plan_id"] = plan_id


def get_plan_id(plan):
    return plan["plan_id"]


def set_plan_as_new(plan):
    plan["plan_status"] = "INITIAL"


def get_tasks(plan):
    return plan["tasks"]


def task_get_id(task):
    return task["@id"]


def task_get_name(task):
    return task["name"]


def get_id():
    return str(uuid.uuid4())


def set_plan_as_complete(plan):
    plan["plan_status"] = "COMPLETE"


def is_task_complete(task):
    return task['task_status'] == "COMPLETE"


def is_task_initial(task):
    return task['task_status'] == "INITIAL"


def set_task_as_complete(task):
    task['task_status'] = "COMPLETE"


def set_task_as_new(task):
    task['task_status'] = "INITIAL"


def set_task_as_running(task):
    task['task_status'] = "RUNNING"


def get_task_id(task):
    return task["@id"]


def get_dependencies(plan):
    return plan["dependencies"]


def get_dependency_from(dep):
    return dep["from"]


def get_dependency_to(dep):
    return dep["to"]
