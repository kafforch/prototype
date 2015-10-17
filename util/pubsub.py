from pydispatch import dispatcher


def publish(event, data):
    dispatcher.send(signal=event, sender=dispatcher.Anonymous, event=event, data=data)


def subscribe(event, receiver):
    dispatcher.connect(receiver, signal=event, sender=dispatcher.Any)


def unsubscribe(sender, event):
    try:
        dispatcher.disconnect(sender, signal=event)
    except KeyError:
        # Shush, just work
        True


def get_num_of_subscribers(signal):
    i = 0
    _list = dispatcher.getAllReceivers(sender=dispatcher.Any, signal=signal)
    for _item in _list:
        i+=1

    return i
