from pprint import pformat
from itertools import chain

from midi import SetTempoEvent

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

from seqer.
from seqer.collections import MutableSequence


class EventStream(EventDispatcher):
    # in units of ticks
    cursor = NumericProperty(0)
    start_of_track = NumericProperty(0)
    end_of_track = NumericProperty(0)

    def __init__(self, pattern): # set end_of_track
        self.pattern = pattern
        self.resolution = pattern.resolution
        self.tempomap = TempoMap(self)
        self.refresh_tempomap()

        for track in pattern:
            track.bind(events=self.on_events)
        pattern.bind(tracks=self.on_tracks)

    def refresh_tempomap(self):
        self.tempomap[:] = []
        for event in sorted(event
                            for event in self.merged()
                            if isinstance(event, SetTempoEvent)):
            self.tempomap.add(event)
        self.tempomap.update()

    def merged(self):
        return chain.from_iterable(self.pattern)

    def iterevents(self):
        pass

    def on_events(self, track, events):
        self.refresh_tempomap()

    def on_tracks(self, pattern, tracks):
        self.refresh_tempomap()

    def on_cursor(self, eventstream, cursor):
        if cursor < self.start_of_track:
            self.cursor = self.start_of_track

        if cursor > self.end_of_track:
            self.cursor = self.end_of_track

    def on_start_of_track(self, eventstream, start_of_track):
        if start_of_track > self.cursor:
            self.cursor = start_of_track

        if start_of_track > self.end_of_track:
            self.start_of_track = self.end_of_track

    def on_end_of_track(self, eventstream, end_of_track):
        if end_of_track < self.cursor:
            self.cursor = end_of_track

        if end_of_track < self.start_of_track:
            self.end_of_track = self.start_of_track



class Pattern(MutableSequence, EventDispatcher):
    tracks = ListProperty([])

    def __init__(self, tracks=[], resolution=220, format=1, tick_relative=True):
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
