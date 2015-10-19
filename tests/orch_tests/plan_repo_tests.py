import unittest
from orch import plan_repo


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.plan_json = open('tests/json/plan_01.json', 'r').read()
        self.plan_id = plan_repo.save_new_plan(self.plan_json)


class MyTestCase(MyTestCaseBase):

    def test_plan_save(self):
        plan = plan_repo.get_plan_by_id(self.plan_id)
        self.assertEqual(plan.get_plan_id(), self.plan_id)

