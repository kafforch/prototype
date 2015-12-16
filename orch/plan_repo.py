import uuid
import plan_parser

__plans = []


def get_id():
    return str(uuid.uuid4())


def get_plan_ids_with_outstanding_time_based_tasks():
    return map(lambda plan: plan.get_plan_id(), __plans)


def save_new_plan(plan_json):
    plan = plan_parser.parse_plan_json(plan_json)
    plan_id = get_id()
    plan.set_plan_id(plan_id)
    plan.set_plan_as_new()

    map(lambda task: task.set_task_as_new(), plan.get_tasks())

    __plans.append(plan)
    return plan_id


def set_task_running(plan_id, task_id):
    plan = get_plan_by_id(plan_id)
    tasks = plan.get_tasks()
    for task in tasks:
        if task_id == task.get_task_id():
            task.set_task_as_running()
            return


def set_task_complete(plan_id, task_id):
    plan = get_plan_by_id(plan_id)
    tasks = plan.get_tasks()
    for task in tasks:
        if task_id == task.get_task_id():
            task.set_task_as_complete()
            return


def initial_get_ready_tasks_for_plan(plan_id):
    plan = get_plan_by_id(plan_id)

    def get_next_tasks_to_run(task_id):
        task = get_task_by_id(plan, task_id)
        return task.is_task_initial() and len(get_ready_tasks_for_plan_task(plan, task)) == 0

    return filter(get_next_tasks_to_run, plan.get_task_ids())


def get_ready_tasks_for_plan_task(plan, task):
    predecessors = []
    task_id = task.get_task_id()

    for dependency in plan.get_dependencies():
        dependency_id = dependency.get_dependency_to()
        if dependency_id == task_id:
            predecessors.append(dependency.get_dependency_from())

    return predecessors


def all_dependencies_complete_for_task(plan, task_id):
    dependencies = plan.get_dependencies()
    for dependency in dependencies:
        from_task_id = dependency.get_dependency_from()
        from_task = get_task_by_id(plan, from_task_id)
        if dependency.get_dependency_to() == task_id and \
                not from_task.is_task_complete():
            return False

    return True


def get_ready_dependent_tasks(plan_id, task_id):
    task_ids = []
    plan = get_plan_by_id(plan_id)

    for dependency in plan.get_dependencies():
        if dependency.get_dependency_from() == task_id:
            dep_task_id = dependency.get_dependency_to()
            dep_task = get_task_by_id(plan, dep_task_id)
            if dep_task.is_task_initial() and \
                    all_dependencies_complete_for_task(plan, dep_task_id):
                task_ids.append(dep_task_id)

    return task_ids


def get_task_by_id(plan, task_id):
    for task in plan.get_tasks():
        if task.get_task_id() == task_id:
            return task


def get_task_name(plan_id, task_id):
    for plan in __plans:
        if plan.get_plan_id() == plan_id:
            for task in plan.get_tasks():
                if task.task_get_id() == task_id:
                    return task.task_get_name()


def are_all_tasks_complete(plan_id):
    plan = get_plan_by_id(plan_id)
    tasks = plan.get_tasks()
    for task in tasks:
        if not task.is_task_complete():
            return False
    return True


def set_plan_as_complete(plan_id):
    plan = get_plan_by_id(plan_id)
    plan.set_plan_as_complete()


def set_plan_as_running(plan_id):
    plan = get_plan_by_id(plan_id)
    plan.set_plan_as_running()


def get_plan_by_id(plan_id):
    matching_plans = [x for x in __plans if x.get_plan_id() == plan_id]
    if len(matching_plans):
        return matching_plans[0]
    else:
        raise ValueError("Plan {0} not found".format(plan_id))
