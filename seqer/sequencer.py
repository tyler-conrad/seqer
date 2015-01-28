from Queue import Empty

from kivy.clock import Clock

from seqer.pypm_proxy import Time
from seqer.pypm_proxy import record_buffer
from seqer.state import is_recording_lock
from seqer import state

# rtpmidi/rtpmidi/engines/midi/midi_in.py
POLL_INTERVAL = 0.015


class Sequencer(object):
    def set_pattern_manager(self, pattern_manager):
        # todo: handle pattern manager swap
        self.pattern_manager = pattern_manager

    def record(self):
        self.start_time = Time()

        with is_recording_lock:
            state.is_recording = True

        if not self.pattern_manager:
            self.pattern_manager.new_track()

        self.record_poller = Clock.schedule_interval(
            self.record_event, POLL_INTERVAL)

    def record_event(self, dt):
        new_event_list = []
        while True:
            try:
                event = record_buffer.get_nowait()
            except Empty:
                break

            new_event_list.append(event)

        for event in new_event_list:
            self.pattern_manager.record_event(self.make_absolute(event))

    def play(self):
        pass

    def pause(self):
        with is_recording_lock:
            state.is_recording = False

    def stop(self):
        with is_recording_lock:
            state.is_recording = False
        Clock.unschedule(self.record_poller)

    def fast_forward(self):
        pass

    def rewind(self):
        pass

    def make_absolute(self, event):
        event.tick -= self.start_time
        return event
