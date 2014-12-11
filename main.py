from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)

from kivy.support import _twisted_reactor_stopper
from kivy.base import EventLoop
from kivy.app import App
from kivy.uix.button import Button

from rtpmidi import runner

class SeqerApp(App):
    def build(self):
        return Button()

def on_stop(event_loop):
    runner.before_shutdown()
    _twisted_reactor_stopper()

def main():
    EventLoop.unbind(on_stop=_twisted_reactor_stopper)
    EventLoop.bind(on_stop=on_stop)

    runner.run(version='')
    SeqerApp().run()

if __name__ == '__main__':
    main()
