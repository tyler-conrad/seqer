import sys
from signal import signal
from signal import SIGINT

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)

from kivy.support import _twisted_reactor_stopper
from kivy.base import EventLoop
from kivy.base import stopTouchApp
from kivy.app import App
from kivy.uix.button import Button

from seqer.seq import pypm_proxy
sys.modules['pypm'] = pypm_proxy

from seqer.rtpmidi.runner import run
from rtpmidi.runner import before_shutdown

class SeqerApp(App):
    def build(self):
        return Button()

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

    run(version='')
    SeqerApp().run()


if __name__ == '__main__':
    main()
