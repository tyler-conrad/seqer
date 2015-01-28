from midi import SetTempoEvent

from seqer.test.util import window


def test_track_make_ticks_absolute_relative(mary_track_two):
    old_relative_ticks = [event.tick for event in mary_track_two]
    mary_track_two.make_ticks_abs()
    mary_track_two.make_ticks_rel()
    new_relative_ticks = [event.tick for event in mary_track_two]
    assert old_relative_ticks == new_relative_ticks


def test_track_make_ticks_absolute(mary_track_two):
    mary_track_two.make_ticks_abs()
    all(left <= right for left, right in window(mary_track_two, 2))


def test_track_get_single_item(mary_track_two, mary_track_two_event_list):
    assert mary_track_two[20] == mary_track_two_event_list[20]


def test_track_get_slice(mary_track_two, mary_track_two_event_list):
    assert mary_track_two[20:30].events == mary_track_two_event_list[20:30]


def test_pattern_get_slice(mary_pattern):
    assert mary_pattern[:1].tracks == [mary_pattern.tracks[0]]


def test_event_stream_tempomap(
        mary_event_stream,
        mary_pattern,
        mary_track_one,
        mary_track_two):
    mary_pattern.make_ticks_abs()

    mary_track_one.make_ticks_abs()
    mary_track_two.make_ticks_abs()

    new_tempomap = [event for event in
                    filter(lambda event: isinstance(event, SetTempoEvent),
                           sorted(list(mary_track_one) + list(mary_track_two)))]

    assert mary_event_stream.tempomap()[:] == new_tempomap


def test_event_stream_slice(mary_event_stream):
    event_list = sorted(list(mary_event_stream.merged()))
    beg = event_list[10]
    end = event_list[15]
    assert mary_event_stream[beg.tick:end.tick] == event_list[10:15]
    assert mary_event_stream[beg.tick:end.tick + 1] == event_list[10:16]
    assert mary_event_stream[beg.tick + 1:end.tick] == event_list[11:15]

    # todo more tests for patterns with runs of events with the same tick value

