'''
    Orchestrator facade to expose API:
'''

class Orchestrator:

    def __init__(self, **kwargs):
        self.plan_repo = kwargs['plan_repo']
        self.plan_exec = kwargs['plan_exec']


    def submit_plan_for_execution(self, plan_json, complete_callback):
        '''
        Executes submitted plan.

        Algorithm:
            parse plan JSON
            save the plan and get back plan id
            trigger plan execution

        :param plan_json: json string describing a plan
        :return: plan_id: Autogenerated id of submitted plan
        '''

        plan_id = self.plan_repo.save_plan(plan_json)
        self.plan_exec.execute_plan(plan_id, complete_callback)

        return plan_id
