import unittest

from util import pubsub


class EventManagerTestsBase(unittest.TestCase):
    def setUp(self):
        self.event_mgr = pubsub.PubSub()


class EventManagerTests(EventManagerTestsBase):

    def test_pubsub(self):

        # initially there are 0 subscribers
        self.assertEqual(len(self.event_mgr.subscribers), 0)

        # callback with correct invocation checks
        def callback(id, event, data):
            #print "Invoked callback for id=%s" % id
            self.assertEqual(event, "START")
            self.assertDictEqual(data, dict(
                data1=123,
                data2="test000"
            ))

        # Subscribe twice, but ensure only one is registered
        self.event_mgr.subscribe("123", "START", callback)
        self.event_mgr.subscribe("123", "START", callback)

        self.assertEqual(len(self.event_mgr.subscribers), 1)

        # Subscribe with another id and check it has been added
        self.event_mgr.subscribe("1234", "START", callback)

        self.assertEqual(len(self.event_mgr.subscribers), 2)

        # publish the event and ensure the number of subscribers is still 2
        self.event_mgr.publish("START", dict(
            data1=123,
            data2="test000"
        ))

        self.assertEqual(len(self.event_mgr.subscribers), 2)

        # Unsubscribe the same id twice. Should only be unsubscribed once
        self.event_mgr.unsubscribe("123", "START")
        self.event_mgr.unsubscribe("123", "START")

        self.assertEqual(len(self.event_mgr.subscribers), 1)

        # Unsubscribe the last one and check there is no subscribers
        self.event_mgr.unsubscribe("1234", "START")

        self.assertEqual(len(self.event_mgr.subscribers), 0)
