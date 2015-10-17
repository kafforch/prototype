import unittest

from util import pubsub


class EventManagerTests(unittest.TestCase):
    def test_pubsub(self):
        # initially there are 0 subscribers
        self.assertEqual(pubsub.get_num_of_subscribers("START"), 0)

        # callback with correct invocation checks
        def callback(event, data):
            # print "Invoked callback for id=%s" % id
            self.assertEqual(event, "START")
            self.assertDictEqual(data, dict(
                data1=123,
                data2="test000"
            ))

        # Subscribe twice, but ensure only one is registered
        pubsub.subscribe("START", callback)
        pubsub.subscribe("START", callback)

        self.assertEqual(pubsub.get_num_of_subscribers("START"), 1)

        # publish the event and ensure the number of subscribers is still 2
        pubsub.publish(event="START", data=dict(
            data1=123,
            data2="test000"
        ))

        self.assertEqual(pubsub.get_num_of_subscribers("START"), 1)

        # Unsubscribe the same id twice. Should only be unsubscribed once
        pubsub.unsubscribe("START", callback)
        pubsub.unsubscribe("START", callback)

        self.assertEqual(pubsub.get_num_of_subscribers("START"), 0)

        # Unsubscribe the last one and check there is no subscribers
        pubsub.unsubscribe("START", callback)

        self.assertEqual(pubsub.get_num_of_subscribers("START"), 0)
