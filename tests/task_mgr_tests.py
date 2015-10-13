import unittest
from orchestrator import orchestrator, task_mgr

class TaskManagerTest(unittest.TestCase):

    def test_adding_tasks_and_dependencies(self):
        id = orchestrator.submit_plan(open('tests/json/plan_01.json', 'r').read())
        plan = orchestrator.get_plan(id)
        self.assertTrue(plan["plan_state"] == "INITIAL")
        orchestrator.execute_plans()
        plan = orchestrator.get_plan(id)
        self.assertTrue(plan["plan_state"] == "RUNNING")
        orchestrator.execute_plans()
        orchestrator.purge_plans()