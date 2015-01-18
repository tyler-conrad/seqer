import socket

from rtpmidi.utils import check_ip

from seqer.command.base import Command
from seqer.rtpmidi.runner import run
from seqer.logger import warn


def ip_from_host_or_ip(host_or_ip):
    if check_ip(host_or_ip):
        return host_or_ip
    try:
        ip = socket.gethostbyname(host_or_ip)
    except socket.gaierror as e:
        warn('Invalid host or ip address: {host_or_ip}', host_or_ip=host_or_ip)
        raise e
    return ip


class InitRTPMIDI(Command):
    def __init__(
            self,
            peer_address='192.168.0.1',
            sending_port=44000,
            receiving_port=44000,
            latency=20,
            jitter_buffer_size=10,
            safe_keyboard=False,
            disable_recovery_journal=False,
            follow_standard=False,
            verbose=True):

        self.peer_address = peer_address
        self.sending_port = sending_port
        self.receiving_port = receiving_port
        self.latency = latency
        self.jitter_buffer_size = jitter_buffer_size
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
