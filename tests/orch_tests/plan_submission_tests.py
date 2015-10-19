import logging
import unittest

from orch import orchestrator, plan_repo, task_exec


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)


class MyTestCase(MyTestCaseBase):

    def test_pykka_plan_01_submission(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()
        plan_01_id = plan_repo.save_new_plan(plan_json)
        test_self = self

        class Test01TaskListener(task_exec.BaseTaskListener):
            def create_listener(self, plan_id, task_id, plan_executor):
                test_self.assertIn(int(task_id), range(1, 5))
                self.task_completed(plan_executor, plan_id, task_id)

        orchestrator.execute_plan(plan_id=plan_01_id, task_listener=Test01TaskListener())

    def test_pykka_plan_02_submission(self):
        plan_json = open('tests/json/plan_02.json', 'r').read()
        plan_02_id = plan_repo.save_new_plan(plan_json)
        test_self = self

        class Test02TaskListener(task_exec.BaseTaskListener):
            def create_listener(self, plan_id, task_id, plan_executor):
                test_self.assertIn(int(task_id), range(1, 11))
                self.task_completed(plan_executor, plan_id, task_id)

        orchestrator.execute_plan(plan_id=plan_02_id, task_listener=Test02TaskListener())
