import unittest
from orchestrator import orchestrator, task_mgr

class TaskManagerTest(unittest.TestCase):

    def test_adding_tasks_and_dependencies(self):
        id = orchestrator.submit_plan(open('tests/json/plan_01.json', 'r').read())
        orchestrator.execute_plans()
        _tm = task_mgr.TaskManager()
        print _tm.get_tasks_for_plan(id)
        print _tm.get_dependencies_for_plan(id)
        orchestrator.purge_plans()