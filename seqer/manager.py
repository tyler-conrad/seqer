from bisect import insort
from collections import Sized

from python_midi.containers import Pattern as PythonMidiPattern
from python_midi.containers import Track as PythonMidiTrack


class PatternManager(Sized):
    def __init__(self, pattern=None):
        if not pattern:
            pattern = PythonMidiPattern(tick_relative=False)
        self.pattern = pattern
        self.selected_track_list = []

    def select_track(self, track):
        if track not in self.selected_track_list:
            self.selected_track_list.append(track)

    def deselect_track(self, track):
        if track in self.selected_track_list:
            self.selected_track_list.remove(track)

    def record_event(self, event):
        for track in self.selected_track_list:
            insort(track, event)

    def new_track(self):
        track = PythonMidiTrack(tick_relative=False)
        self.pattern.append(track)
        self.select_track(track)

    def __len__(self):
        return len(self.pattern)
