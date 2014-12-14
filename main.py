import sys

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from kivy.support import _twisted_reactor_stopper

from twisted.python import log
log.addObserver(log.PythonLoggingObserver('kivy').emit)

from seqer import pypm_proxy
sys.modules['pypm'] = pypm_proxy

from os.path import dirname
from sys import argv
from signal import signal
from signal import SIGINT

from kivy.config import Config
from kivy.base import EventLoop
from kivy.base import stopTouchApp
from kivy.interactive import InteractiveLauncher
from kivy.app import App
from kivy.resources import resource_add_path

from rtpmidi.runner import before_shutdown

from seqer.rtpmidi.runner import run
from seqer.manager import PatternManager
from seqer.sequencer import Sequencer


class SeqerApp(App):
    def on_start(self):
        sequencer = Sequencer()
        sequencer.set_pattern_manager(PatternManager())
        sequencer.record()


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

    Config.set('graphics', 'fullscreen', 0)

    resource_add_path(dirname(argv[0]) + '/assets')

    run(version='')
    InteractiveLauncher(SeqerApp()).run()


if __name__ == '__main__':
    main()
