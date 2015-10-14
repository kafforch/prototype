import json


class PlanParser:

    def parse_plan_json(self, plan_json):
        return json.loads(plan_json)

    def set_plan_id(self, plan, plan_id):
        new_plan = dict(plan)
        new_plan["plan_id"] = plan_id
        return plan