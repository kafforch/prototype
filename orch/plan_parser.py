import json


class PlanParser:

    def parse_plan_json(self, plan_json):
        return json.loads(plan_json)

    def set_plan_id(self, plan, plan_id):
        new_plan = dict(plan)
        new_plan["plan_id"] = plan_id
        return new_plan

    def get_plan_id(self, plan):
        return plan["plan_id"]

    def get_tasks(self, plan):
        return plan["tasks"]

    def task_get_id(self, task):
        return task["@id"]

    def task_get_name(self, task):
        return task["name"]