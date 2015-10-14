import json
import uuid


class PlanParser:

    def parse_plan_json(self, plan_json):
        return json.loads(plan_json)

    def set_plan_id(self, plan, plan_id):
        plan["plan_id"] = plan_id

    def set_plan_status_as_new(self, plan):
        plan["plan_status"] = "INITIAL"

    def get_plan_id(self, plan):
        return plan["plan_id"]

    def get_tasks(self, plan):
        return plan["tasks"]

    def task_get_id(self, task):
        return task["@id"]

    def task_get_name(self, task):
        return task["name"]

    def get_id(self):
        return str(uuid.uuid4())

    def set_plan_complete(self, plan):
        plan["plan_status"] = "COMPLETE"