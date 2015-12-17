import mock
import unittest

from scheduler import timer_svc


class TimerSvcTests(unittest.TestCase):

    def test_set_get_current_time(self):
        timer_svc.set_time("2015-12-17T00:00:48.000Z")
        self.assertEqual(timer_svc.get_time(), "2015-12-17T00:00:48.000Z")