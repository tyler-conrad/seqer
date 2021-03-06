__version__ = "0.0.0"

import sys

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from kivy.support import _twisted_reactor_stopper

from twisted.python import log
log.addObserver(log.PythonLoggingObserver('kivy').emit)

from seqer import pypm_proxy
sys.modules['pypm'] = pypm_proxy

import rtpmidi.protocols.rtp.rtp_session as rtp_session


def get_name():
    return 'seqer'
rtp_session.get_name = get_name


def get_fqdn():
    return get_name() + '@localhost'
rtp_session.get_fqdn = get_fqdn

from os.path import abspath
from os.path import dirname
from signal import signal
from signal import SIGINT

from kivy.base import EventLoop
from kivy.base import stopTouchApp
from kivy.interactive import InteractiveLauncher
from kivy.resources import resource_add_path

from rtpmidi.runner import before_shutdown

from seqer.option import options
from seqer.app import SeqerApp


def on_stop(event_loop):
    before_shutdown()
    _twisted_reactor_stopper()


def sigint_handler(signal, frame):
    EventLoop.ensure_window()
    window = EventLoop.window
    if not window.dispatch('on_request_close', source='keyboard'):
        stopTouchApp()
        window.close()


def main():
    signal(SIGINT, sigint_handler)

    EventLoop.unbind(on_stop=_twisted_reactor_stopper)
    EventLoop.bind(on_stop=on_stop)

    resource_add_path(dirname(abspath(__file__)) + '/data')

    seqer_app = SeqerApp()
    if options.interactive:
        InteractiveLauncher(seqer_app).run()
    else:
        seqer_app.run()

if __name__ == '__main__':
    main()
