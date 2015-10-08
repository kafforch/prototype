import Plan

def create_plan(tasks=[], dependencies=[]):

    plan = Plan()
    plan.add_tasks(tasks)
    plan.create_dependencies(dependencies)

    return plan
