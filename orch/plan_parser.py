import json


class PlanParser:

    def parse_plan_json(self, plan_json):
        return json.loads(plan_json)