from bisect import insort
from collections import Sized

from midi.containers import Pattern
from midi.containers import Track


class PatternManager(Sized):
    def __init__(self, pattern=None):
        if not pattern:
            pattern = Pattern(tick_relative=False)
        self.pattern = pattern
        self.selected_track_list = []

    def select_track(self, track):
        if track not in self.selected_track_list:
            self.selected_track_list.append(track)

    def deselect_track(self, track):
        if track in self.selected_track_list:
            self.selected_track_list.remove(track)

    def record_event(self, event):
        print 'pm record event'
        for track in self.selected_track_list:
            insort(track, event)

    def new_track(self):
        track = Track(tick_relative=False)
        self.pattern.append(track)
        self.select_track(track)

    def __len__(self):
        return len(self.pattern)
