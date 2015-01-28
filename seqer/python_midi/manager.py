from itertools import chain
from itertools import groupby

from midi import EndOfTrackEvent
from midi import SetTempoEvent
from midi import TimeSignatureEvent

from seqer.logger import warn


def filter_by_event_type(event_list, event_type):
    return [event for event in event_list if isinstance(event, event_type)]


def verify_pattern(pattern):
    for track_num, track in enumerate(pattern):
        end_of_track_event_list = filter_by_event_type(track, EndOfTrackEvent)
        if len(end_of_track_event_list) == 0:
            warn('No End Of Track event found for track: {track_num}',
                 track_num=track_num)

        if len(end_of_track_event_list) > 1:
            warn('More than one End of Track event found for track: '
                 + '{track_num}', track_num=track_num)

        try:
            if sorted(track)[-1] != end_of_track_event_list[0]:
                warn('The found End of Track event is not the last event for '
                     + 'track: {track_num}', track_num=track_num)
        except IndexError:
            pass

    time_signature_event_list = filter_by_event_type(
        chain.from_iterable(pattern), TimeSignatureEvent)

    if len(time_signature_event_list) == 0:
        warn('No Time Signature Event found.', track_num=track_num)

    if len(time_signature_event_list) > 1:
        warn('More than one Time Signature Event found.')

    try:
        if time_signature_event_list[0].tick != 0:
            warn('The Time Signature Event does not have a tick value of 0.')
    except IndexError:
        pass

    set_tempo_event_list = filter_by_event_type(
        chain.from_iterable(pattern), SetTempoEvent)

    set_tempo_event_tick_list = [event.tick for event in set_tempo_event_list]
    if not all([len(list(tick_group)) == 1
                for tick, tick_group
                in groupby(sorted(set_tempo_event_tick_list))]):
        warn('More than one Set Tempo Event exists with the same tick value.')

    start_of_track_set_tempo_event_list = [
        event for event in set_tempo_event_list
        if event.tick == 0]

    if not len(start_of_track_set_tempo_event_list) > 0:
        warn('No Set Tempo Events found with a tick value of 0.')

