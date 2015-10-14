import unittest
from orch import event_mgr

class EventManagerTestsBase(unittest.TestCase):
    def setUp(self):
        self.event_mgr = event_mgr.EventManager()


class EventManagerTests(EventManagerTestsBase):

    def test_pubsub(self):

        self.assertEqual(len(self.event_mgr.subscribers), 0)

        def callback(event, data):
            self.assertEqual(event, "START")
            self.assertDictEqual(data, dict(
                data1=123,
                data2="test000"
            ))

        self.event_mgr.subscribe("123", "START", callback)

        self.assertEqual(len(self.event_mgr.subscribers), 1)

        self.event_mgr.publish("START", dict(
            data1=123,
            data2="test000"
        ))

        self.assertEqual(len(self.event_mgr.subscribers), 1)

        self.event_mgr.unsubscribe("123", "START")

        self.assertEqual(len(self.event_mgr.subscribers), 0)
