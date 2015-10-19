import unittest
from orch import plan_repo


class MyTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.plan_json1 = open('tests/orch_tests/json/plan_01.json', 'r').read()
        self.plan_json2 = open('tests/orch_tests/json/plan_02.json', 'r').read()


class MyTestCase(MyTestCaseBase):

    def test_plan_save(self):
        plan_id = plan_repo.save_new_plan(self.plan_json1)
        plan = plan_repo.get_plan_by_id(plan_id)
        self.assertEqual(plan.get_plan_id(), plan_id)

    def test_plan_ready_tasks_after_1(self):
        plan_id = plan_repo.save_new_plan(self.plan_json2)
        initial_tasks = plan_repo.initial_get_ready_tasks_for_plan(plan_id)
        self.assertSetEqual(set(initial_tasks), {'1'})
        plan_repo.set_task_complete(plan_id, '1')
        dependencies = plan_repo.get_ready_dependent_tasks(plan_id, '1')
        self.assertEqual(len(dependencies), 2)
        self.assertSetEqual(set(dependencies), {'3', '2'})

    def test_plan_ready_tasks_after_4(self):
        plan_id = plan_repo.save_new_plan(self.plan_json2)
        plan_repo.set_task_complete(plan_id, '4')
        plan = plan_repo.get_plan_by_id(plan_id)
        self.assertEqual(plan_repo.get_task_by_id(plan, '4').task_get_name(), 'new name')
        dependencies = plan_repo.get_ready_dependent_tasks(plan_id, '4')
        self.assertEqual(len(dependencies), 2)
        self.assertSetEqual(set(dependencies), {'5', '9'})
        self.assertFalse(plan_repo.are_all_tasks_complete(plan_id))

    def test_plan_ready_tasks_after_89(self):
        plan_id = plan_repo.save_new_plan(self.plan_json2)
        plan_repo.set_task_complete(plan_id, '8')
        plan_repo.set_task_complete(plan_id, '9')
        dependencies = plan_repo.get_ready_dependent_tasks(plan_id, '8')
        self.assertEqual(len(dependencies), 1)
        self.assertSetEqual(set(dependencies), {'10'})
