class PubSub:
    def __init__(self):

        # List of dicts. Every element is {
        #                                   "id": UNIQUEID,
        #                                   "event": EVENTNAME,
        #                                   "func": FUNCTION,
        #                                 }
        self.__subscribers = []

    def publish(self, event, data):
        for subscriber in self.__subscribers:
            if subscriber["event"] == event:
                subscriber["func"](subscriber["id"], event, data)

    def subscribe(self, sub_id, event, func):
        subscription = dict(
            id=sub_id,
            event=event,
            func=func
        )
        for subscriber in self.__subscribers:
            if subscriber["id"] == sub_id and subscriber["event"] == event:
                return

        self.__subscribers.append(subscription)

    def unsubscribe(self, subs_id, event):
        i = 0
        for subscriber in self.__subscribers:
            if subscriber["id"] == subs_id and subscriber["event"] == event:
                self.__subscribers.pop(i)
            i += 1

    def get_subscribers(self):
        return self.__subscribers
