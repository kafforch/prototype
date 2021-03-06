import ConfigParser
import logging
import time

from orch import plan_repo, orchestrator
from scheduler import timer_svc

logger = logging.getLogger ( __name__ )


def get_delay():
    config = ConfigParser.RawConfigParser ( )
    config.readfp ( open ( "../defaults.cfg" ) )
    delay = config.getint ( "Scheduler", "loop_delay_secs" )
    logger.debug ( "Read delay value {}".format ( delay ) )
    return delay


def interrupt():
    False


def start_timed_plans():
    for plan_id in plan_repo.get_not_started_timed_plan_ids():
        plan = plan_repo.get_plan_by_id(plan_id)
        if timer_svc.is_current_datetime_later_than( plan.get_start_on() ):
            # TODO Add task_starter and task_listener
            orchestrator.execute_plan(plan_id)


def start_timed_tasks_for_running_plans():
    for plan_id in plan_repo.get_running_plan_ids():
        plan = plan_repo.get_plan_by_id(plan_id)
        for task in plan.get_tasks():
            task_start_time = task.get_start_on()
            if task_start_time and timer_svc.is_current_datetime_later_than(task_start_time):
                orchestrator.execute_task(plan_id, task.get_task_id())


def scheduler_loop():
    # Main scheduler loop
    while 1 == 1:

        time.sleep ( get_delay ( ) )

        logger.debug ( "Setting new timer time" )
        timer_svc.set_datetime ( timer_svc.get_current_datetime ( ) )

        # Check if there are initial plans with start_on that need to be started.
        start_timed_plans()

        # Check if there are running plans that have tasks with start_on. If the task is not active
        # and it is time to start it, start it.
        start_timed_tasks_for_running_plans()


        if interrupt():
            return


if __name__ == "__main__":
    scheduler_loop ( )
