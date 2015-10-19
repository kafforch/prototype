import unittest
from orch import plan_parser


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.plan_json = open('tests/json/plan_01.json', 'r').read()


class MyTestCase(MyTestCaseBase):
    def test_plan_01(self):
        plan = plan_parser.parse_plan_json(self.plan_json)
        self.assertEqual(len(plan.get_tasks()), 3)
        self.assertEqual(len(plan.get_dependencies()), 2)
