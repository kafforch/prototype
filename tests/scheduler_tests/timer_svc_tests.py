# coding=utf-8
import mock
import unittest

import time

from scheduler import timer_svc


class TimerSvcTests(unittest.TestCase):

    def test_set_get_current_time(self):
        timer_svc.set_datetime( "2015-12-17T00:00:48.000Z" )
        self.assertEqual( timer_svc.get_datetime_str( ), "2015-12-17T00:00:48.000Z" )

    def test_is_after_current_time(self):
        timer_svc.set_datetime("2015-12-17T00:00:48.000Z")
        self.assertTrue(timer_svc.is_less_than_current_datetime("2015-12-16T00:00:48.000Z"))
        self.assertFalse(timer_svc.is_less_than_current_datetime("2015-12-18T00:00:48.000Z"))
        self.assertTrue(timer_svc.is_less_than_current_datetime("2015-12-16T01:00:48.000Z"))
        self.assertTrue(timer_svc.is_less_than_current_datetime("2015-12-15T23:00:48.000Z"))
        self.assertTrue(timer_svc.is_less_than_current_datetime("2015-12-16T00:00:47.000Z"))
