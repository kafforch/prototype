import unittest
from orchestrator import orchestrator

class OrchTest(unittest.TestCase):

    def test_simple_json_parsing(self):
        parsed = orchestrator._parse_json('{"test" :"123"}')
        self.assertTrue(parsed["test"] == "123")

    def test_simple_submit_plan(self):
        orchestrator.submit_plan('{"test" :"123"}')
        plan = orchestrator._plan_mgr.get_plans().values()[0]
        orchestrator._plan_mgr.purge_plans()
        self.assertTrue(plan['test'] == "123")