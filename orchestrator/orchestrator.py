import plan_mgr
import json

def _parse_json(json_str):
    return json.loads(json_str)

def submit_plan(json_string):
    _plan_mgr = plan_mgr.PlanManager()
    plan = json.loads(json_string)
    plan_id = _plan_mgr.create_plan(plan)
    return plan_id

def get_plan(plan_id):
    _plan_mgr = plan_mgr.PlanManager()
    return _plan_mgr.plans[plan_id]

def get_all_plans():
    _plan_mgr = plan_mgr.PlanManager()
    return _plan_mgr.get_plans()

def execute_all_plans():
    _plan_mgr = plan_mgr.PlanManager()
    return _plan_mgr.execute_all_plans()

def purge_all_plans_and_tasks():
    _plan_mgr = plan_mgr.PlanManager()
    _plan_mgr.purge_ll_plans_and_tasks()