import pytest

from kivy.event import EventDispatcher

from seqer.properties import MutableListProperty
from seqer.properties import mute

@pytest.fixture
def event_dispatcher():
    class Dispatcher(EventDispatcher):
        mutable_list_property = MutableListProperty([1, 2, 3])
    return Dispatcher()


called = False
def test_mutable_list_property(event_dispatcher):
    def callback(event_dispatcher, mutable_list_property):
        global called
        called = True
    event_dispatcher.bind(mutable_list_property=callback)

    event_dispatcher.mutable_list_property[0] = 0
    assert called

    global called
    called = False

    with mute(event_dispatcher,
              event_dispatcher.properties()['mutable_list_property']):
        event_dispatcher.mutable_list_property[1] = 1
    assert not called

    event_dispatcher.mutable_list_property[2] = 2
    assert called
