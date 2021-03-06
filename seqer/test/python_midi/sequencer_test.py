from itertools import chain

import pytest

from midi import SetTempoEvent
from midi import MetaEvent

from seqer.python_midi.containers import Pattern
from seqer.python_midi.containers import Track
from seqer.python_midi.containers import EventStream
from seqer.python_midi.sequencer import EventStreamIterator
from seqer.test.util import window

@pytest.fixture
def tempo_event_list():
    tempo_event_list = [SetTempoEvent() for i in range(10)]
    for i, event in enumerate(tempo_event_list):
        event.tick = i * 1000
        event.bpm = i + 100
    return tempo_event_list


def test_tempomap(tempo_event_list):
    pattern = Pattern([Track(tempo_event_list)])
    pattern.make_ticks_abs()
    tempomap = EventStream(pattern).tempomap()
    assert all([left.msdelay < right.msdelay
               for left, right in window(tempomap[1:], 2)])


@pytest.fixture
def event_list(mary_event_stream):
    return sorted([
        event for event in list(mary_event_stream.merged())
        if not isinstance(event, MetaEvent)])


def test_event_stream_iterator_normal_usage(mary_event_stream, event_list):
    esi = EventStreamIterator(
        stream=mary_event_stream,
        window=20,
        start_tick=0,
        end_tick=event_list[-1].tick + 1)
    assert list(chain.from_iterable(esi)) == event_list


def test_event_stream_iterator_small_window(mary_event_stream, event_list):
    esi = EventStreamIterator(
        stream=mary_event_stream,
        window=3,
        start_tick=0,
        end_tick=event_list[-1].tick + 1)
    assert list(chain.from_iterable(esi)) == event_list


def test_event_stream_iterator_start_end_tick_0(mary_event_stream):
    esi = EventStreamIterator(
        stream=mary_event_stream,
        window=20,
        start_tick=0,
        end_tick=0)
    assert list(chain.from_iterable(esi)) == []


def test_event_stream_iterator_large_window(mary_event_stream, event_list):
    esi = EventStreamIterator(
        stream=mary_event_stream,
        window=20000,
        start_tick=0,
        end_tick=event_list[-1].tick + 1)
    assert list(chain.from_iterable(esi)) == event_list
