from sys import argv
from textwrap import dedent
from os import linesep
from os.path import basename
from sys import exit

from twisted.python.usage import Options
from twisted.python.usage import UsageError

from seqer.utils import QueryDict


class Parser(Options):
    optFlags = [
        ['disable-recovery-journal', 'j', 'DISABLE recovery journal (journal provide note recovery when a packet is lost, so at your own risks!)'],
        ['follow-standard', 'f', 'Take care of MIDI standard (ex: omni on) in recovery journal (experimental)'],
        ['interactive', 'i', 'Launch program in interactive mode'],
        ['show-config', 'c', True, 'Show the config popup on start']
        ['verbose', 'v', 'Enables verbose output']
    ]

    optParameters = [
        ['address', 'a', 'localhost', 'Specify the address of the peer (mandatory)'],
        ['send-port', 's', 44000, 'Select the sending port.', int],
        ['receive-port', 'r', 44000, 'Select the listening port', int],
        ['latency', 'l', 20, 'Specify the latency (in ms) of the midi out device', int],
        ['jitter-buffer', 'b', 10, 'Specify the jitter buffer size in ms', int]
    ]

parser = Parser()
try:
    parser.parseOptions(argv[2:])
except UsageError as ue:
    print linesep.join(dedent('''
        {prog_name}: {usage_error}
        {prog_name}: Try --help for usage details.
    '''.format(
        prog_name=basename(argv[0]),
        usage_error=ue
    )).split('\n'))
    exit(1)
options = QueryDict((k, v.replace('-', '_')) for (k, v) in parser.items())

