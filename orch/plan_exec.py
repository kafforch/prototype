from util import pubsub
import plan_repo


def execute_plan(plan_id):
    """
    Orchestrates execution of the tasks ready for execution.

    :param plan_id:
    :return:
    """

    ready_task_ids = plan_repo.initial_get_ready_tasks_for_plan(plan_id)

    pubsub.publish(data=dict(
        plan_id=plan_id
    ), event="START_PLAN")

    for task_id in ready_task_ids:
        __execute_task(plan_id, task_id, __task_complete)


def __task_complete(_, data):
    """
    Callback on completed events. Sets the completed task in the plan and checks if the plan can be marked completed
    :param event: Event pubslished
    :param data: Dictionary with event data
    :return:
    """
    plan_repo.set_task_complete(data['plan_id'], data['task_id'])

    # unsubscribe
    pubsub.unsubscribe("END_TASK", __task_complete)

    if plan_repo.are_all_tasks_complete(data['plan_id']):
        plan_repo.set_plan_as_complete(data['plan_id'])
        pubsub.publish(data=dict(
            plan_id=data["plan_id"]
        ), event="END_PLAN")
    else:
        __execute_dependent_tasks(data['plan_id'], data['task_id'], __task_complete)


def __execute_dependent_tasks(plan_id, task_id, callback):
    for dep_task_id in plan_repo.get_ready_dependent_tasks(plan_id, task_id):
        __execute_task(plan_id, dep_task_id, callback)


def __execute_task(plan_id, task_id, callback=None):
    task_name = plan_repo.get_task_name(plan_id, task_id)

    # create subscription to update task status to complete
    pubsub.subscribe("END_TASK", __task_complete)

    # subscribe to get notified on task completion with customer provided callback
    if callback:
        pubsub.subscribe("END_TASK", callback)

    plan_repo.set_task_running(plan_id, task_id)

    pubsub.publish(data=dict(
        plan_id=plan_id,
        task_id=task_id,
        task_name=task_name
    ), event="START_TASK")
