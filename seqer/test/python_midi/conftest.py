import pytest

from midi import TimeSignatureEvent
from midi import KeySignatureEvent
from midi import EndOfTrackEvent
from midi import ControlChangeEvent
from midi import ProgramChangeEvent
from midi import NoteOnEvent
from midi import SetTempoEvent

from seqer.python_midi.containers import EventStream
from seqer.python_midi.containers import Pattern
from seqer.python_midi.containers import Track


@pytest.fixture
def mary_track_one_event_list():
    return [
        TimeSignatureEvent(tick=0, data=[4, 2, 24, 8]),
        KeySignatureEvent(tick=0, data=[0, 0]),
        SetTempoEvent(tick=0, data=[9, 39, 192]),
        SetTempoEvent(tick=500, data=[9, 16, 139]),
        SetTempoEvent(tick=2000, data=[8, 249, 203]),
        SetTempoEvent(tick=3000, data=[8, 227, 124]),
        EndOfTrackEvent(tick=1, data=[])]

@pytest.fixture
def mary_track_two_event_list():
    return [
        ControlChangeEvent(tick=0, channel=0, data=[91, 58]),
        ControlChangeEvent(tick=0, channel=0, data=[10, 69]),
        ControlChangeEvent(tick=0, channel=0, data=[0, 0]),
        ControlChangeEvent(tick=0, channel=0, data=[32, 0]),
        ProgramChangeEvent(tick=0, channel=0, data=[24]),
        NoteOnEvent(tick=0, channel=0, data=[64, 72]),
        NoteOnEvent(tick=0, channel=0, data=[55, 70]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 72]),
        NoteOnEvent(tick=231, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[60, 71]),
        NoteOnEvent(tick=231, channel=0, data=[60, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 79]),
        NoteOnEvent(tick=206, channel=0, data=[55, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 85]),
        NoteOnEvent(tick=0, channel=0, data=[55, 79]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 78]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 74]),
        NoteOnEvent(tick=462, channel=0, data=[55, 0]),
        NoteOnEvent(tick=0, channel=0, data=[64, 0]),
        NoteOnEvent(tick=50, channel=0, data=[62, 75]),
        NoteOnEvent(tick=0, channel=0, data=[55, 77]),
        NoteOnEvent(tick=231, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 77]),
        NoteOnEvent(tick=231, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 75]),
        NoteOnEvent(tick=462, channel=0, data=[55, 0]),
        NoteOnEvent(tick=0, channel=0, data=[62, 0]),
        NoteOnEvent(tick=50, channel=0, data=[64, 82]),
        NoteOnEvent(tick=0, channel=0, data=[55, 79]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[67, 84]),
        NoteOnEvent(tick=231, channel=0, data=[67, 0]),
        NoteOnEvent(tick=25, channel=0, data=[67, 75]),
        NoteOnEvent(tick=462, channel=0, data=[55, 0]),
        NoteOnEvent(tick=0, channel=0, data=[67, 0]),
        NoteOnEvent(tick=50, channel=0, data=[64, 73]),
        NoteOnEvent(tick=0, channel=0, data=[55, 78]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 69]),
        NoteOnEvent(tick=231, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[60, 71]),
        NoteOnEvent(tick=231, channel=0, data=[60, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 80]),
        NoteOnEvent(tick=206, channel=0, data=[55, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 84]),
        NoteOnEvent(tick=0, channel=0, data=[55, 79]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 76]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 74]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 77]),
        NoteOnEvent(tick=206, channel=0, data=[55, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 75]),
        NoteOnEvent(tick=0, channel=0, data=[55, 78]),
        NoteOnEvent(tick=231, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 74]),
        NoteOnEvent(tick=231, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[64, 81]),
        NoteOnEvent(tick=231, channel=0, data=[64, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 70]),
        NoteOnEvent(tick=206, channel=0, data=[55, 0]),
        NoteOnEvent(tick=25, channel=0, data=[62, 0]),
        NoteOnEvent(tick=25, channel=0, data=[60, 73]),
        NoteOnEvent(tick=0, channel=0, data=[52, 72]),
        NoteOnEvent(tick=974, channel=0, data=[60, 0]),
        NoteOnEvent(tick=0, channel=0, data=[52, 0]),
        EndOfTrackEvent(tick=1, data=[])]


@pytest.fixture
def mary_track_one(mary_track_one_event_list):
    return Track(events=mary_track_one_event_list)


@pytest.fixture
def mary_track_two(mary_track_two_event_list):
    return Track(events=mary_track_two_event_list)


@pytest.fixture
def mary_pattern(mary_track_one, mary_track_two):
    pattern = Pattern(tracks=[mary_track_one, mary_track_two])
    pattern.make_ticks_abs()
    return pattern


@pytest.fixture
def mary_event_stream(mary_pattern):
    return EventStream(mary_pattern)
