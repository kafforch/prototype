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
        # TODO - Will have to be done differently


        if interrupt():
            return


if __name__ == "__main__":
    scheduler_loop ( )
