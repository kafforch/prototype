import ConfigParser
import logging
import time

from orch import plan_repo, orchestrator
from scheduler import timer_svc

logger = logging.getLogger(__name__)


def get_delay():
    config = ConfigParser.RawConfigParser()
    config.readfp(open("../defaults.cfg"))
    delay = config.getint("Scheduler", "loop_delay_secs")
    logger.debug("Read delay value {}".format(delay))
    return delay


def interrupt():
    False


def scheduler_loop():

    # Main scheduler loop
    while 1 == 1 :

        time.sleep(get_delay())

        logger.debug("Setting new timer time")
        timer_svc.set_datetime( timer_svc.get_current_datetime( ) )

        logger.debug("Checking if there are timed plans that can be started")
        for plan_id in plan_repo.get_not_started_timed_plan_ids():
            logger.debug("Found not started timed plan {}".format(plan_id))

            # This will check if the plan is ready to start
            plan = plan_repo.get_plan_by_id(plan_id)
            if timer_svc.is_less_than_current_datetime( plan.get_start_on() ):
                logger.debug("Executing plan {}".format(plan.get_plan_id()))
                # TODO add task_starter and task listener
                orchestrator.execute_plan(plan_id)

        for plan_id in plan_repo.get_plan_ids_with_outstanding_time_based_tasks():

            logger.debug("Checking if plan {} has ready to run timed tasks".format(plan_id))
            orchestrator.run_ready_timed_tasks(plan_id)

        if interrupt():
            return


if __name__ == "__main__":
    scheduler_loop()
