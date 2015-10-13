import unittest
from orchestrator import orchestrator, task_mgr

class TaskManagerTest(unittest.TestCase):

    def test_adding_tasks_and_dependencies(self):
        id = orchestrator.submit_plan(open('tests/json/plan_01.json', 'r').read())
        orchestrator.execute_all_plans()
        _tm = task_mgr.TaskManager()
        self.assertEqual(len(_tm.get_tasks_for_plan(id)), 3)
        self.assertEqual(len(_tm.get_dependencies_for_plan(id)), 2)
        # Testing list extension
        _tm.submit_tasks(id, [1,2], [3,4])
        self.assertEqual(len(_tm.get_tasks_for_plan(id)), 5)
        self.assertEqual(len(_tm.get_dependencies_for_plan(id)), 4)
        orchestrator.purge_all_plans_and_tasks()

