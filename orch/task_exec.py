import random
import pykka
import plan_repo
import time


class TaskExecutor(pykka.ThreadingActor):
    def __init__(self, plan_exec):
        super(TaskExecutor, self).__init__()
        self.__plan_exec = plan_exec


    def execute_task(self, plan_id, task_id):
        print "Called execute_task for plan {0}, task {1}".format(plan_id, task_id)

        plan_repo.set_task_running(plan_id, task_id)

        # pausing and randomness
        sleep_interval = random.randint(1,5)
        print "Sleeping for {0}".format(sleep_interval)
        time.sleep(sleep_interval)

        self.__plan_exec.task_complete(plan_id, task_id)

        self.stop()
        # TODO complete this, but now just perform callback
