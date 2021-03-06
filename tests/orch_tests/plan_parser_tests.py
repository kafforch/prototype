import unittest
from orch import plan_parser, plan_repo


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        plan_repo.purge_all_plans()
        self.plan_json = open('tests/orch_tests/json/plan_01.json', 'r').read()


class MyTestCase(MyTestCaseBase):
    def test_plan_01(self):
        plan = plan_parser.parse_plan_json(self.plan_json)
        self.assertEqual(len(plan.get_tasks()), 3)
        self.assertEqual(len(plan.get_dependencies()), 2)
