import plan_mgr
import json

_plan_mgr = plan_mgr.PlanManager()

def _parse_json(json_str):
    return json.loads(json_str)

def submit_plan(json_string):
    plan = json.loads(json_string)
    plan_id = _plan_mgr.create_plan(plan)
    return plan_id

def get_plan(plan_id):
    return _plan_mgr.plans[plan_id]