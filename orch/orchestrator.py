'''
    Orchestrator facade to expose API:
'''

class Orchestrator:

    def __init__(self, plan_repo, plan_exec, plan_parser):
        self.plan_repo = plan_repo
        self.plan_exec = plan_exec
        self.plan_parser = plan_parser
        pass

    def submit_plan_for_execution(self, plan_json):
        '''
        Executes submitted plan.

        Algorithm:
            parse plan JSON
            save the plan and get back plan id
            trigger plan execution

        :param plan:
        :return:
        '''

        plan = self.plan_parser.parse_plan_json(plan_json)
        plan_id = self.plan_repo.save_plan(plan)
        self.plan_exec.execute_plan(plan_id)
