from time import time
from Queue import Queue
from Queue import Empty

from midi.fileio import FileReader, FileWriter
from midi.util import write_varlen, read_varlen


def CountDevices():
    """Return number of available MIDI (input and output) devices."""
    return 2


def GetDeviceInfo(device_no):
    """Return device info tuple for MIDI device given by device_no.

    The returned tuple has the following five items:

    * underlying MIDI API (string)
    * device name (string)
    * whether device can be opened as input (1) or not (0)
    * whether device can be opened as output (1) or not (0)
    * whether device is currently opened (1) or not (0)

    """
    return [
        ('seqer', 'output', 0, 1, 0),
        ('seqer', 'input', 1, 0, 0)
    ][device_no]


def get_time():
    return int(time() * 1000)
init_time = get_time()


def Time():
    """Return the current time in ms of the PortMidi timer."""
    return get_time() - init_time

io_buffer = Queue()
file_reader = FileReader()
file_writer = FileWriter()


class Output:
    """Represents an output MIDI stream device.

    Takes the form::

        output = pypm.Output(output_device, latency)

    latency is in ms. If latency == 0 then timestamps for output are ignored.

    """

    def __init__(self, output_device, latency=0):
        """Instantiate MIDI output stream object."""


    def Write(self, data):
        """Output a series of MIDI events given by data list n this device.

        Usage::

            Write([
                [[status, data1, data2, data3], timestamp],
                [[status, data1, data2, data3], timestamp],
                ...
            ])

        The data1/2/3 items in each event are optional::

           Write([[[0xc0, 0, 0], 20000]])

        is equivalent to::

           Write([[[0xc0], 20000]])

        Example:

        Send program change 1 at time 20000 and send note 65 with velocity 100
        at 500 ms later::

             Write([[[0xc0, 0, 0], 20000], [[0x90, 60, 100], 20500]])

        .. notes::
            1. Timestamps will be ignored if latency == 0.

            2. To get a note to play immediately, send the note on event with
               the result from the Time() function as the timestamp.

        """
        if not data:
            return

        for event in data:
            io_buffer.put_nowait(file_reader.parse_midi_event(iter(
                write_varlen(event[1]) + ''.join(
                    chr(num) for num in event[0]))))


class Input:
    """Represents an input MIDI stream device.

    Takes the form::

        input = pypm.Input(input_device)

    """

    def __init__(self, input_device, buffersize=4096):
        """Instantiate MIDI input stream object."""

    def Poll(self):
        """Test whether input is available.

        Returns TRUE if input can be read, FALSE otherwise, or an error value.

        """
        return not io_buffer.empty()

    def Read(self, max_events):
        """Read and return up to max_events events from input.

        Reads up to max_events midi events stored in the input buffer and
        returns them as a list in the following form::

            [
                [[status, data1, data2, data3], timestamp],
                [[status, data1, data2, data3], timestamp],
                ...
            ]

        """
        if not self.Poll():
            return []

        event_list = []
        for i in range(max_events):
            file_writer.RunningStatus = None
            try:
                encoded = file_writer.encode_midi_event(
                    io_buffer.get(block=True, timeout=0))
            except Empty:
                break

            timestamp = read_varlen(iter(encoded))
            event_list.append([[ord(num) for num in encoded], timestamp])

        return event_list
