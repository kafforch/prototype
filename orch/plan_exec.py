from util import pubsub


class PlanExec:
    def __init__(self, plan_repo):
        self.__plan_repo = plan_repo

    def execute_plan(self, plan_id):
        """
        Orchestrates execution of the tasks ready for execution.

        :param plan_id:
        :return:
        """

        ready_task_ids = self.__plan_repo.initial_get_ready_tasks_for_plan(plan_id)

        pubsub.publish(data=dict(
            plan_id=plan_id
        ), event="START_PLAN")

        for task_id in ready_task_ids:
            self.__execute_task(plan_id, task_id, self.__task_complete)

    def __task_complete(self, event, data):
        """
        Callback on completed events. Sets the completed task in the plan and checks if the plan can be marked completed
        :param event: Event pubslished
        :param data: Dictionary with event data
        :return:
        """
        self.__plan_repo.set_task_complete(data['plan_id'], data['task_id'])

        # unsubscribe
        pubsub.unsubscribe("END_TASK", self.__task_complete)

        if self.__plan_repo.are_all_tasks_complete(data['plan_id']):
            self.__plan_repo.set_plan_as_complete(data['plan_id'])
            pubsub.publish(data=dict(
                plan_id=data["plan_id"]
            ), event="END_PLAN")
        else:
            self.__execute_dependent_tasks(data['plan_id'], data['task_id'], self.__task_complete)

    def __execute_dependent_tasks(self, plan_id, task_id, callback):
        for dep_task_id in self.__plan_repo.get_ready_dependent_tasks(plan_id, task_id):
            self.__execute_task(plan_id, dep_task_id, callback)

    def __execute_task(self, plan_id, task_id, callback=None):
        task_name = self.__plan_repo.get_task_name(plan_id, task_id)

        # create subscription to update task status to complete
        pubsub.subscribe("END_TASK", self.__task_complete)

        # subscribe to get notified on task completion with customer provided callback
        if callback:
            pubsub.subscribe("END_TASK", callback)

        self.__plan_repo.set_task_running(plan_id, task_id)

        pubsub.publish(data=dict(
            plan_id=plan_id,
            task_id=task_id,
            task_name=task_name
        ), event="START_TASK")
