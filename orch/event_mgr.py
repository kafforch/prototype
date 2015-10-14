class EventManager:

    def __init__(self):

        # List of dicts. Every element is {
        #                                   "id": UNIQUEID,
        #                                   "event": EVENTNAME,
        #                                   "func": FUNCTION,
        #                                 }
        self.subscribers = []

    def publish(self, event, data):
        for subscriber in self.subscribers:
            if subscriber["event"] == event:
                subscriber["func"](subscriber["id"], event, data)


    def subscribe(self, id, event, func):
        subscription = dict(
            id=id,
            event=event,
            func=func
        )
        for subscriber in self.subscribers:
            if subscriber["id"] == id:
                return

        self.subscribers.append(subscription)


    def unsubscribe(self, id, event):
        i = 0
        for subscriber in self.subscribers:
            if subscriber["id"] == id and subscriber["event"] == event:
                self.subscribers.pop(i)
            i += 1
