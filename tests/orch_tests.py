import unittest
from orchestrator import orchestrator, plan_mgr

class OrchTest(unittest.TestCase):

    def test_simple_json_parsing(self):
        parsed = orchestrator._parse_json('{"test" :"123"}')
        self.assertTrue(parsed["test"] == "123")

    def test_simple_submit_plan(self):
        orchestrator.submit_plan('{"test" :"123"}')
        plan = orchestrator._plan_mgr.get_plans().values()[0]
        # Test plan retrieval worked
        self.assertTrue(plan['test'] == "123")
        orchestrator._plan_mgr.purge_plans()
        # test purge worked and the list is empty
        self.assertDictEqual(orchestrator._plan_mgr.get_plans(), {})

    def test_singleton(self):
        orchestrator.submit_plan('{"test" :"123"}')
        new_pm = plan_mgr.PlanManager()
        plan = new_pm.get_plans().values()[0]
        orchestrator._plan_mgr.purge_plans()
        self.assertTrue(plan['test'] == "123")

    def test_retrieval_by_id(self):
        id = orchestrator.submit_plan('{"test": "345"}')
        plan = orchestrator.get_plan(id)
        orchestrator._plan_mgr.purge_plans()
        self.assertTrue(plan['test'] == "345")


