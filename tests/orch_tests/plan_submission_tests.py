import logging
import unittest

from orch import orchestrator, plan_repo, task_exec


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)


#@unittest.skip("Skipping tests in {}".format(__name__))
class MyTestCase(MyTestCaseBase):

    def setUp(self):
        plan_repo.purge_all_plans()

    def test_pykka_plan_01_submission(self):
        plan_json = open('tests/orch_tests/json/plan_01.json', 'r').read()
        plan_01_id = plan_repo.save_new_plan(plan_json)
        test_self = self

        class Test01TaskListener(task_exec.BaseTaskListener):
            def create_listener(self, plan_id, task_id, plan_executor):
                test_self.assertIn(int(task_id), range(1, 5))
                plan = plan_repo.get_plan_by_id(plan_id)
                test_self.assertFalse(plan.is_plan_initial())
                test_self.assertTrue(plan.is_plan_running())
                self.task_completed(plan_executor, plan_id, task_id)

        orchestrator.execute_plan(plan_id=plan_01_id, task_listener=Test01TaskListener())

    def test_pykka_plan_02_submission(self):
        plan_json = open('tests/orch_tests/json/plan_02.json', 'r').read()
        plan_02_id = plan_repo.save_new_plan(plan_json)
        test_self = self

        class Test02TaskListener(task_exec.BaseTaskListener):
            def create_listener(self, plan_id, task_id, plan_executor):
                test_self.assertIn(int(task_id), range(1, 11))
                self.task_completed(plan_executor, plan_id, task_id)

        orchestrator.execute_plan(plan_id=plan_02_id, task_listener=Test02TaskListener())
