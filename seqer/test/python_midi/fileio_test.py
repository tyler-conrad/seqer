from os import remove

from seqer.python_midi.fileio import write_midifile
from seqer.python_midi.fileio import read_midifile


def test_fileio(mary_pattern):
    write_midifile("mary.mid", mary_pattern)
    pattern1 = read_midifile("mary.mid")
    write_midifile("mary.mid", pattern1)
    pattern2 = read_midifile("mary.mid")
    assert len(pattern1) == len(pattern2)
    for track_idx in range(len(pattern1)):
        assert len(pattern1[track_idx]) == len(pattern2[track_idx])
        for event_idx in range(len(pattern1[track_idx])):
            event1 = pattern1[track_idx][event_idx]
            event2 = pattern2[track_idx][event_idx]
            assert event1.tick == event2.tick
            assert event1.data == event2.data
    remove('mary.mid')
