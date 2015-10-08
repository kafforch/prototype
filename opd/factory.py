from Plan import Plan

def create_plan(tasks=[], dependencies=[]):

    plan = Plan()
    plan.add_tasks(tasks)
    plan.add_dependencies(dependencies)

    return plan
