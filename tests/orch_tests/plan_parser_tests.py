import unittest
from orch import plan_parser


class MyTestCase(unittest.TestCase):
    def test_plan_01(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()
        plan = plan_parser.parse_plan_json(plan_json)
        self.assertEqual(len(plan.get_tasks()), 3)
        self.assertEqual(len(plan.get_dependencies()), 2)
