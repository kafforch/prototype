import unittest
import opd

class OpdTests(unittest.TestCase):
    def test_empty_plan(self):
        plan = opd.create_plan()
        self.assertTrue(len(plan.get_tasks()) == 0)