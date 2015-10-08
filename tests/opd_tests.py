import unittest
from opd import factory

class OpdTests(unittest.TestCase):
    def test_empty_plan(self):
        plan = factory.create_plan()
        self.assertTrue(len(plan.get_tasks()) == 0)