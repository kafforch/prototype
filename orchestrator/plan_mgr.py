import uuid
import task_mgr

def _get_id(prefix=""):
    return "{0}{1}".format(prefix, uuid.uuid4())


# noinspection PyAttributeOutsideInit
class PlanManager:

    # Singleton
    __shared_state = dict(
        plans={}
    )


    def __init__(self):
        self.__dict__ = self.__shared_state

    def store(self, plan_id, plan):
        self.plans[plan_id] = plan


    def get_plans(self):
        return self.__shared_state['plans']


    def purge_plans(self):
        self.plans = {}


    def create_plan(self, plan):
        plan_id = _get_id()
        plan['plan_id'] = plan_id
        plan['plan_state'] = 'INITIAL'

        try:
            len(plan['tasks']) >= 0
        except KeyError:
            plan['tasks'] = []

        try:
            len(plan['dependencies']) >= 0
        except KeyError:
            plan['dependencies'] = []

        self.store(plan_id, plan)
        return plan_id


    def execute_plans(self):
        started_plan_ids = []
        for plan in self.plans.values():
             self.execute_plan(plan['plan_id'])


    def execute_plan(self, plan_id):
        for plan in self.plans.values():
            if plan['plan_id'] == plan_id and plan["plan_state"] == 'INITIAL':
                plan['plan_state'] = 'RUNNING'
                _task_mgr = task_mgr.TaskManager()
                _task_mgr.execute_tasks(plan['plan_id'], plan['tasks'], plan['dependencies'])
