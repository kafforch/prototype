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

    def test_submission(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()

        # simple callback with notification
        def callback(id, event, data):
            print "Received event {0} for id={1} with data {2}".format(event, id, data)
            print "Sending complete notification"

        self.event_mgr.subscribe("123456", "START_TASK", callback)
        self.event_mgr.subscribe("123456", "END_TASK", callback)

        self.orchestrator.submit_plan_for_execution(plan_json)