import unittest

from orch import orchestrator, plan_parser, plan_exec, plan_repo
from util import pubsub


class PlanSubmissionTestsInit(unittest.TestCase):
    def setUp(self):
        self.plan_parser = plan_parser.PlanParser()

        self.plan_repo = plan_repo.PlanRepo(
            plan_parser=self.plan_parser
        )

        self.pubsub = pubsub.PubSub()

        self.plan_exec = plan_exec.PlanExec(
            plan_repo=self.plan_repo,
            pubsub = self.pubsub
        )

        self.orchestrator = orchestrator.Orchestrator(
            plan_repo=self.plan_repo,
            plan_exec=self.plan_exec
        )


class PlanSubmissionTests(PlanSubmissionTestsInit):

    def test_plan_submission_for_plan_01(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()

        # callback to simulate a fragment work
        def callback(subs_id, event, data):
            print "Received event {0} for id={1} with data {2}".format(event, subs_id, data)
            print "Sending complete notification for task {0}".format(data['task_id'])
            self.assertIn(data['task_name'], ["123", "345", "999"])
            self.assertIn(data['task_id'], ["1","2","3"])
            self.pubsub.publish("END_TASK", data)

        # simple callback on completion
        def callback_complete(id, event, data):
            print "Task {0} of plan {1} is complete".format(data['task_id'], data['plan_id'])
            self.assertIn(data['task_id'], ["1","2","3"])
            self.assertIn(data['task_name'], ["123", "345", "999"])

        self.pubsub.subscribe("123456", "START_TASK", callback)

        def callback_plan_complete(id, event, data):
            print "Plan {0} is complete".format(data['plan_id'])
            self.assertEqual(len(self.pubsub.subscribers), 4)
            self.pubsub.unsubscribe("123456", "START_TASK")
            self.pubsub.unsubscribe("00001", "END_PLAN")
            self.pubsub.unsubscribe("00001a", "START_PLAN")
            self.assertEqual(len(self.pubsub.subscribers), 1)

        self.pubsub.subscribe("00001", "END_PLAN", callback_plan_complete)

        def callback_plan_start(id, event, data):
            print "Plan {0} is starting".format(data['plan_id'])

        self.pubsub.subscribe("00001a", "START_PLAN", callback_plan_start)

        # Submission. All subscriptions happen before this
        self.orchestrator.submit_plan_for_execution(plan_json, callback_complete)

