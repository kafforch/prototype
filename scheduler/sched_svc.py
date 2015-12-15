import ConfigParser
import logging
import time

from orch import plan_repo, orchestrator

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
        for plan_id in plan_repo.get_plan_ids_with_outstanding_time_based_tasks():
            logger.debug("Checking if plan {} has ready to run timed tasks".format(plan_id))
            orchestrator.run_ready_tasks(plan_id)

        if interrupt():
            return


if __name__ == "__main__":
    scheduler_loop()
