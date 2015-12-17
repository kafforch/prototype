from scheduler import sched_svc, timer_svc
from orch import orchestrator, plan_repo

import unittest
from mock import patch
import logging


class SchedSvcTestsBase(unittest.TestCase):
    def setUp(self):
        logger = logging.getLogger('scheduler.sched_svc')
        logger.setLevel(logging.DEBUG)

        # Save two plans with timed start and one without
        plan_repo.purge_all_plans()
        self.plan1_id = plan_repo.save_new_plan(open ( 'tests/scheduler_tests/json/plan_01.json', 'r' ).read ( ))
        self.plan2_id = plan_repo.save_new_plan(open ( 'tests/scheduler_tests/json/plan_03.json', 'r' ).read ( ))
        self.plan3_id = plan_repo.save_new_plan(open ( 'tests/scheduler_tests/json/plan_03.json', 'r' ).read ( ))
        self.plan4_id = plan_repo.save_new_plan(open ( 'tests/scheduler_tests/json/plan_04.json', 'r' ).read ( ))

    def tearDown(self):
        plan_repo.purge_all_plans()


class SchedSvcTests1(SchedSvcTestsBase):

    def test_start_timed_tasks_for_running_plans1(self):

        # Start 4 plans
        orchestrator.execute_plan(self.plan1_id)
        orchestrator.execute_plan(self.plan2_id)
        orchestrator.execute_plan(self.plan3_id)
        orchestrator.execute_plan(self.plan4_id)

        # Set datetime
        timer_svc.set_datetime("2015-11-12T11:23:44.123Z")

        with patch("orch.orchestrator.execute_task") as mock_execute_task:
            sched_svc.start_timed_tasks_for_running_plans()

        self.assertEqual(mock_execute_task.call_count, 3)


class SchedSvcTests2(SchedSvcTestsBase):

    def test_start_timed_plans1(self):

        # Set datetime
        timer_svc.set_datetime("2015-11-12T11:23:44.123Z")

        with patch("orch.orchestrator.execute_plan") as mock_execute_plan:
            sched_svc.start_timed_plans()

        self.assertEqual(mock_execute_plan.call_count, 3)


    def test_start_timed_plans2(self):

        # Set datetime
        timer_svc.set_datetime("2013-11-12T11:23:44.123Z")

        with patch("orch.orchestrator.execute_plan") as mock_execute_plan:
            sched_svc.start_timed_plans()

        self.assertEqual(mock_execute_plan.call_count, 2)


    def test_start_timed_plans3(self):

        # Set datetime
        timer_svc.set_datetime("2011-11-12T11:23:44.123Z")

        with patch("orch.orchestrator.execute_plan") as mock_execute_plan:
            sched_svc.start_timed_plans()

        self.assertEqual(mock_execute_plan.call_count, 0)