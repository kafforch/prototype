from scheduler import sched_svc
from orch import plan_repo

import mock
from mock import call
import unittest
import logging
import ConfigParser


class SchedSvcTests(unittest.TestCase):
    def setUp(self):
        logger = logging.getLogger('scheduler.sched_svc')
        logger.setLevel(logging.INFO)

    @mock.patch("scheduler.sched_svc.interrupt", return_value=True)
    @mock.patch("scheduler.sched_svc.open")
    @mock.patch.object(ConfigParser.RawConfigParser, "readfp")
    @mock.patch.object(ConfigParser.RawConfigParser, "getint", return_value=0)
    @mock.patch("orch.plan_repo.get_plan_ids_with_outstanding_time_based_tasks", return_value=['1','2','3'])
    @mock.patch("orch.orchestrator.run_ready_timed_tasks")
    def test_scheduler_loop(self, mock_run_ready_tasks, *args):

        # Run the loop
        sched_svc.scheduler_loop()

        # Check correct sequence of calls
        mock_run_ready_tasks.assert_has_calls([call('1'), call('2'), call('3')])


    @mock.patch("scheduler.sched_svc.interrupt", return_value=True)
    @mock.patch("scheduler.sched_svc.open")
    @mock.patch.object(ConfigParser.RawConfigParser, "readfp")
    @mock.patch.object(ConfigParser.RawConfigParser, "getint", return_value=0)
    @mock.patch("orch.plan_repo.get_plan_ids_with_outstanding_time_based_tasks", return_value=[])
    @mock.patch("orch.orchestrator.execute_plan")
    def test_scheduler_loop_with_not_started_plans(self, mock_execute_plan, *args):

        # Add two plans to the plan_repo
        plan_repo.save_new_plan(open ( 'tests/orch_tests/json/plan_03.json', 'r' ).read ( ))
        plan_repo.save_new_plan(open ( 'tests/orch_tests/json/plan_03.json', 'r' ).read ( ))

        # Run the loop
        sched_svc.scheduler_loop()

        # Check 2 calls to execute plans
        self.assertEqual( mock_execute_plan.call_count, 2)
