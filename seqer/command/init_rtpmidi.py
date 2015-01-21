from seqer.command.base import Command
from seqer.rtpmidi.runner import run
from seqer.util.network import ip_from_host_or_ip


class InitRTPMIDI(Command):
    def __init__(
            self,
            peer_address='localhost',
            sending_port='44000',
            receiving_port='44000',
            latency='20',
            jitter_buffer_size='10',
            safe_keyboard=False,
            disable_recovery_journal=False,
            follow_standard=False,
            verbose=True):

        self.peer_address = ip_from_host_or_ip(peer_address)
        self.sending_port = int(sending_port)
        self.receiving_port = int(receiving_port)
        self.latency = int(latency)
        self.jitter_buffer_size = int(jitter_buffer_size)
        self.safe_keyboard = safe_keyboard
        self.disable_recovery_journal = disable_recovery_journal
        self.follow_standard = follow_standard
        self.verbose = verbose

    def execute(self):
        run(
            peer_address=self.peer_address,
            sending_port=self.sending_port,
            receiving_port=self.receiving_port,
            latency=self.latency,
            jitter_buffer_size=self.jitter_buffer_size,
            safe_keyboard=self.safe_keyboard,
            disable_recovery_journal=self.disable_recovery_journal,
            follow_standard=self.follow_standard,
            verbose=self.verbose)
