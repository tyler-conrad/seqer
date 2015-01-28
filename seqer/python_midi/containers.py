from bisect import bisect_left
from pprint import pformat
from itertools import chain

from midi import SetTempoEvent
from midi import Event
from midi import MetaEvent

from kivy.event import EventDispatcher
from kivy.properties import ListProperty

from seqer.python_midi.sequencer import TempoMap
from seqer.collections import MutableSequence

DEFAULT_RESOLUTION = 220


class EventStream(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.resolution = pattern.resolution

    def tempomap(self):
        tempomap = TempoMap(self)
        for event in self.merged():
            if isinstance(event, SetTempoEvent):
                tempomap.add(event)
        tempomap.update()
        return tempomap

    def merged(self):
        return chain.from_iterable(self.pattern)

    def __getitem__(self, index_or_slice):
        if not isinstance(index_or_slice, slice):
            raise NotImplementedError(
                'EventStream only supports slice operations')

        event_list = sorted([
            event for event in self.merged()
            if not isinstance(event, MetaEvent)])

        left = bisect_left(event_list, Event(tick=index_or_slice.start))
        right = bisect_left(event_list, Event(tick=index_or_slice.stop))
        return event_list[left:right]

    def __len__(self):
        return len(self.merged())


class Pattern(MutableSequence, EventDispatcher):
    tracks = ListProperty([])

    def __init__(self, tracks=[], resolution=DEFAULT_RESOLUTION, format=1, tick_relative=True):
        self.format = format
        self.resolution = resolution
        self.tick_relative = tick_relative
        self.tracks[:] = tracks

    def __repr__(self):
        return "midi.Pattern(format=%r, resolution=%r, tracks=\\\n%s)" % \
            (self.format, self.resolution, pformat(list(self)))

    def make_ticks_abs(self):
        self.tick_relative = False
        for track in self:
            track.make_ticks_abs()

    def make_ticks_rel(self):
        self.tick_relative = True
        for track in self:
            track.make_ticks_rel()

    def __getitem__(self, index_or_slice):
        if isinstance(index_or_slice, slice):
            return Pattern(resolution=self.resolution, format=self.format,
                            tracks=self.tracks[index_or_slice])
        return self.tracks[index_or_slice]

    def __setitem__(self, index_or_slice, value):
        self.tracks[index_or_slice] = value

    def __delitem__(self, index_or_slice):
        del self.tracks[index_or_slice]

    def insert(self, index, value):
        self.tracks.insert(index, value)

    def __len__(self):
        return len(self.tracks)


class Track(MutableSequence, EventDispatcher):
    events = ListProperty([])

    def __init__(self, events=[], tick_relative=True):
        self.tick_relative = tick_relative
        self.events[:] = events

    def __repr__(self):
        return "midi.Track(\\\n  %s)" % (pformat(list(self)).replace('\n', '\n  '), )

    def make_ticks_abs(self):
        if (self.tick_relative):
            self.tick_relative = False
            running_tick = 0
            for event in self:
                event.tick += running_tick
                running_tick = event.tick

    def make_ticks_rel(self):
        if (not self.tick_relative):
            self.tick_relative = True
            running_tick = 0
            for event in self:
                event.tick -= running_tick
                running_tick += event.tick

    def __getitem__(self, index_or_slice):
        if isinstance(index_or_slice, slice):
            return Track(events=self.events[index_or_slice],
                         tick_relative=self.tick_relative)
        return self.events[index_or_slice]

    def __setitem__(self, index_or_slice, value):
        self.events[index_or_slice] = value

    def __delitem__(self, index_or_slice):
        del self.events[index_or_slice]

    def insert(self, index, value):
        self.events.insert(index, value)

    def __len__(self):
        return len(self.tracks)


