# adapted from https://github.com/vishnubob/python-midi
from bisect import bisect_left

from seqer.util.misc import print_pipe


class TempoMap(list):
    def __init__(self, stream):
        self.stream = stream

    def add_and_update(self, event):
        self.add(event)
        self.update()

    def add(self, event):
        # get tempo in microseconds per beat
        tempo = event.mpqn
        # convert into milliseconds per beat
        tempo = tempo / 1000.0
        # generate ms per tick
        event.mpt = tempo / self.stream.resolution
        self.append(event)

    def update(self):
        self.sort()
        # adjust running time
        last = None
        for event in self:
            if last:
                event.msdelay = last.msdelay + \
                    int(last.mpt * (event.tick - last.tick))
            else:
                event.msdelay = 0
            last = event

    def get_tempo(self, offset=0):
        last = self[0]
        for tm in self[1:]:
            if tm.tick > offset:
                return last
            last = tm
        return last


# XXX: If multiple tempos occur per window then the first tempo in the window
# is used for calculating the next windowedge.  The remaining tempos in the
# window are skipped and have no effect.
class EventStreamIterator(object):
    def __init__(self, stream, window, start_tick, end_tick):
        self.stream = stream
        self.window_length = window
        self.end_tick = end_tick
        self.lastedge = self.window_edge = start_tick
        # Setup next tempo timepoint
        self.ttp = self.next_ttp(self.window_edge)
        # self.tempomap = iter(self.stream.tempomap)
        self.tempo = self.next_tempo(self.lastedge, offset=-1)
        self.endoftrack = False

    def __iter__(self):
        return self

    def next_tempo(self, lastedge, offset=0):
        tempo_from_tick = dict([(tempo.tick, tempo)
                                for tempo in self.stream.tempomap()])
        tick_list = sorted(tempo_from_tick.keys())
        return tempo_from_tick[tick_list[
            print_pipe(bisect_left(tick_list, lastedge) + offset)]]

    def next_ttp(self, windowedge):
        ttp_list = [tempo.tick for tempo in self.stream.tempomap()]
        ttp_list = ttp_list[:bisect_left(ttp_list, self.end_tick)]
        ttp_list.append(self.end_tick)
        try:
            return ttp_list[bisect_left(ttp_list, windowedge)]
        except IndexError:
            raise StopIteration

    def __next_edge(self):
        if self.endoftrack:
            raise StopIteration
        self.lastedge = self.window_edge
        self.window_edge += int(self.window_length / self.tempo.mpt)
        if self.window_edge > self.ttp:
            # We're past the tempo-marker.
            oldttp = self.ttp
            try:
                self.ttp = self.next_ttp(self.window_edge)
            except StopIteration:
                # End of Track!
                self.window_edge = self.ttp
                self.endoftrack = True
                return
            # Calculate the next window edge, taking into
            # account the tempo change.
            msused = (oldttp - self.lastedge) * self.tempo.mpt
            msleft = self.window_length - msused
            self.tempo = self.next_tempo(self.lastedge)
            ticksleft = msleft / self.tempo.mpt
            self.window_edge = ticksleft + self.tempo.tick

    def next(self):
        self.__next_edge()
        return self.stream[self.lastedge:self.window_edge]
