import unittest

from orch import orchestrator, plan_parser, plan_exec, plan_repo, event_mgr

class PlanSubmissionTestsInit(unittest.TestCase):
    def setUp(self):
        self.plan_parser = plan_parser.PlanParser()

        self.plan_repo = plan_repo.PlanRepo(
            plan_parser=self.plan_parser
        )

        self.event_mgr = event_mgr.EventManager()

        self.plan_exec = plan_exec.PlanExec(
            plan_repo=self.plan_repo,
            event_mgr = self.event_mgr
        )

        self.orchestrator = orchestrator.Orchestrator(
            plan_repo=self.plan_repo,
            plan_exec=self.plan_exec,
        )

class PlanSubmissionTests(PlanSubmissionTestsInit):

    def test_plan_submission(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()

        # callback to simulate a fragment work
        def callback(id, event, data):
            print "Received event {0} for id={1} with data {2}".format(event, id, data)
            print "Sending complete notification"
            self.assertEqual(data['task_name'], 12)
            self.assertIn(data['task_id'], [1,2,3])
            self.event_mgr.publish("END_TASK", data)

        # simple callback on completion
        def callback_complete(id, event, data):
            print "Task {0} of plan {1} is complete".format(data['task_id'], data['plan_id'])
            self.assertIn(data['task_id'], [1,2,3])
            self.assertEqual(data['task_name'], 12)

        self.event_mgr.subscribe("123456", "START_TASK", callback)

        self.orchestrator.submit_plan_for_execution(plan_json, callback_complete)

        self.event_mgr.unsubscribe("123456", "START_TASK")
