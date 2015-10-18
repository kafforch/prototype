import unittest

from orch import plan_exec, plan_repo


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.plan_executor = plan_exec.PlanExecutor.start().proxy()


class MyTestCase(MyTestCaseBase):

    def test_pykka_plan_02_submission(self):
        plan_json = open('tests/json/plan_02.json', 'r').read()
        plan_id = plan_repo.save_new_plan(plan_json)
        self.plan_executor.execute_plan(plan_id)
