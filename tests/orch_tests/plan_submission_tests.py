import random
import unittest
import time

from orch import orchestrator, plan_parser, plan_exec, plan_repo
from util import pubsub


class PlanSubmissionTestsInit(unittest.TestCase):
    def setUp(self):
        self.plan_parser = plan_parser

        self.plan_repo = plan_repo.PlanRepo(
            plan_parser=plan_parser
        )

        self.plan_exec = plan_exec.PlanExec(
            plan_repo=self.plan_repo
        )

        self.orchestrator = orchestrator.Orchestrator(
            plan_repo=self.plan_repo,
            plan_exec=self.plan_exec
        )


class PlanSubmissionTests(PlanSubmissionTestsInit):

    def test_plan_submission_for_plan_02(self):
        plan_json = open('tests/json/plan_02.json', 'r').read()

        # callback to simulate a fragment work
        def callback(event, data):
            print "Received event {0} with data {1}".format(event, data)

            # pausing and randomness
            sleep_interval = random.randint(1,5)
            print "Sleeping for {0}".format(sleep_interval)
            time.sleep(sleep_interval)

            print "Sending complete notification for task {0}".format(data['task_id'])
            pubsub.publish("END_TASK", data)

        pubsub.subscribe("START_TASK", callback)

        # simple callback on completion
        def callback_complete(event, data):
            print "Task {0} of plan {1} is complete".format(data['task_id'], data['plan_id'])

        pubsub.subscribe("END_TASK", callback_complete)

        def callback_plan_complete(event, data):
            print "Plan {0} is complete".format(data['plan_id'])
            pubsub.unsubscribe(callback_plan_complete, "START_TASK")
            pubsub.unsubscribe(callback_plan_complete, "END_PLAN")
            pubsub.unsubscribe(callback_plan_complete, "START_PLAN")

        pubsub.subscribe("END_PLAN", callback_plan_complete)

        def callback_plan_start(event, data):
            print "Plan {0} is starting".format(data['plan_id'])

        pubsub.subscribe("START_PLAN", callback_plan_start)

        # Submission. All subscriptions happen before this
        self.orchestrator.submit_plan_for_execution(plan_json)


    def test_plan_submission_for_plan_01(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()

        # callback to simulate a fragment work
        def callback(event, data):
            # print "Received event {0} for id={1} with data {2}".format(event, subs_id, data)
            # print "Sending complete notification for task {0}".format(data['task_id'])
            self.assertIn(data['task_name'], ["123", "345", "999"])
            self.assertIn(data['task_id'], ["1", "2", "3"])
            pubsub.publish("END_TASK", data)

        # simple callback on completion
        def callback_complete(event, data):
            # print "Task {0} of plan {1} is complete".format(data['task_id'], data['plan_id'])
            self.assertIn(data['task_id'], ["1","2","3"])
            self.assertIn(data['task_name'], ["123", "345", "999"])

        pubsub.subscribe("START_TASK", callback)

        def callback_plan_complete(event, data):
            # print "Plan {0} is complete".format(data['plan_id'])
            self.assertEqual(pubsub.get_num_of_subscribers(event), 1)
            pubsub.unsubscribe(callback_plan_complete, "START_TASK")
            pubsub.unsubscribe(callback_plan_complete, "END_PLAN")
            pubsub.unsubscribe(callback_plan_complete, "START_PLAN")
            self.assertEqual(pubsub.get_num_of_subscribers(event), 0)

        pubsub.subscribe("END_PLAN", callback_plan_complete)

        def callback_plan_start(event, data):
            # print "Plan {0} is starting".format(data['plan_id'])
            True

        pubsub.subscribe("START_PLAN", callback_plan_start)

        # Submission. All subscriptions happen before this
        self.orchestrator.submit_plan_for_execution(plan_json)

