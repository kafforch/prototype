import unittest
from orch import plan_repo


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.plan_json = open('tests/json/plan_01.json', 'r').read()


class MyTestCase(MyTestCaseBase):

    def test_plan_save(self):
        plan_id = plan_repo.save_new_plan(self.plan_json)
        plan = plan_repo.get_plan_by_id(plan_id)
        self.assertEqual(plan.get_plan_id(), plan_id)

