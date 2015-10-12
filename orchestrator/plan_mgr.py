import uuid

class PlanManager:

    # Singleton
    __shared_state = {
        "plans": {}
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    def _get_id(self, prefix=""):
        return "%s%s" % (prefix, uuid.uuid4())

    def store(self, plan_id, plan):
        self.__shared_state["plans"][plan_id] = plan

    def get_plans(self):
        return self.__shared_state["plans"]

    def purge_plans(self):
        self.__shared_state["plans"] = {}

    def create_plan(self, plan):
        plan_id = self._get_id()
        plan["plan_id"] = plan_id
        self.store(plan_id, plan)
