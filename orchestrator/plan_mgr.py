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


    def purge_ll_plans_and_tasks(self):
        _task_mgr = task_mgr.TaskManager()
        _task_mgr.purge_all_tasks()
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


    def execute_all_plans(self):

        _task_mgr = task_mgr.TaskManager()

        for plan in self.plans.values():
             self.execute_plan(plan)

        # Trigger task execution
        _task_mgr.execute_all_tasks()


    def execute_plan(self, plan):

        _task_mgr = task_mgr.TaskManager()

        # Start everything in INITIAL state
        if plan["plan_state"] == 'INITIAL':
            plan['plan_state'] = 'RUNNING'
            _task_mgr.submit_tasks(plan['plan_id'], plan['tasks'], plan['dependencies'])

