import unittest
from opd import Task, factory

class OpdTests(unittest.TestCase):

    def test_task_create(self):
        task = Task.Task(name="test", key1="key1val", key2="key2val")
        self.assertTrue(True)

    def test_empty_plan(self):
        plan = factory.create_plan()
        self.assertTrue(len(plan.get_tasks()) == 0)