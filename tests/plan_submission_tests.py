import unittest

from orch import orchestrator, plan_parser, plan_exec, plan_repo, task_exec

class PlanSubmissionTestsInit(unittest.TestCase):
    def setUp(self):
        self.plan_repo = plan_repo.PlanRepo()
        self.task_exec = task_exec.TaskExec()
        self.plan_exec = plan_exec.PlanExec(
            plan_repo=self.plan_repo,
            task_exec=self.task_exec
        )
        self.plan_parser = plan_parser.PlanParser()
        self.orchestrator = orchestrator.Orchestrator(
            plan_repo=self.plan_repo,
            plan_exec=self.plan_exec,
            plan_parser=self.plan_parser
        )

class PlanSubmissionTests(PlanSubmissionTestsInit):

    def test_submission(self):
        plan_json = open('tests/json/plan_01.json', 'r').read()
        self.orchestrator.submit_plan_for_execution(plan_json)