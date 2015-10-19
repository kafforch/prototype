import unittest

from orch import orchestrator


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        pass


class MyTestCase(MyTestCaseBase):

    def test_pykka_plan_01_submission(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()
        orchestrator.submit_plan_for_execution(plan_json)

    def test_pykka_plan_02_submission(self):
        plan_json = open('tests/json/plan_02.json', 'r').read()
        orchestrator.submit_plan_for_execution(plan_json)
