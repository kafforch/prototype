class EventManager:

    def publish(self, **kwargs):
        message = dict(kwargs)
        event = kwargs['event']
        del message['event']