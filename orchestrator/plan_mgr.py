import uuid

class PlanManager:

    # Singleton
    __shared_state = dict(
        plans={}
    )


    def __init__(self):
        self.__dict__ = self.__shared_state


    def _get_id(self, prefix=""):
        return "%s%s" % (prefix, uuid.uuid4())


    def store(self, plan_id, plan):
        self.plans[plan_id] = plan


    def get_plans(self):
        return self.__shared_state["plans"]


    def purge_plans(self):
        self.plans = {}


    def create_plan(self, plan):
        plan_id = self._get_id()
        plan["plan_id"] = plan_id
        plan["plan_state"] = "INITIAL"
        self.store(plan_id, plan)
        return plan_id


    def execute_plans(self):
        running_plans = []
        for plan in self.plans.values():
            if plan["plan_state"] == "INITIAL":
                self.execute_plan(plan["plan_id"])
                running_plans.append(plan["plan_id"])

        return running_plans


    def execute_plan(self, plan_id):
        for plan in self.plans.values():
            if plan["plan_id"] == plan_id and plan["plan_state"] == "INITIAL":
                plan["plan_state"] = "RUNNING"