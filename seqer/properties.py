from kivy.properties import ListProperty


class MutableListProperty(ListProperty):
    def link(self, event_dispatcher, name):
        super(MutableListProperty, self).link(event_dispatcher, name)

        if not hasattr(event_dispatcher, '_muted'):
            event_dispatcher._muted = {}
        event_dispatcher._muted[name] = False

    def dispatch(self, event_dispatcher):
        if event_dispatcher._muted[self.name]:
            return
        super(MutableListProperty, self).dispatch(event_dispatcher)


class MutablePropertyContextManager(object):
    def __init__(self, event_dispatcher, mutable_property_name):
        self.event_dispatcher = event_dispatcher
        self.mutable_property = (
            event_dispatcher.properties()[mutable_property_name])

    def set_muted(self, is_muted):
        self.event_dispatcher._muted[self.mutable_property.name] = is_muted

    def __enter__(self):
        self.set_muted(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_muted(False)


def mute(event_dispatcher, mutable_property_name):
    return MutablePropertyContextManager(event_dispatcher, mutable_property_name)
