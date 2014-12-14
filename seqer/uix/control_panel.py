from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.resources import resource_find
from kivy.graphics.svg import Svg
from kivy.graphics.context_instructions import Translate
from kivy.graphics.context_instructions import PushMatrix
from kivy.graphics.context_instructions import PopMatrix
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton


Builder.load_string('''
<ControlPanel>:
    ControlButton:
        filename: 'rewind.svg'
    ControlButton:
        filename: 'stop.svg'
    ControlButton:
        filename: 'pause.svg'
    ControlButton:
        filename: 'play.svg'
    ControlButton:
        filename: 'record.svg'
    ControlButton:
        filename: 'fast_forward.svg'
''')


class ControlButton(ToggleButton):
    filename = StringProperty()

    def __init__(self, **kwargs):
        super(ControlButton, self).__init__(**kwargs)
        self.trigger_update = Clock.create_trigger(self.update, -1)


    def on_filename(self, instance, filename):
        if hasattr(self, 'svg'):
            self.canvas.clear()

        self.svg = Svg(filename=resource_find(filename))
        print self.svg.width
        print self.svg.height
        self.translate = Translate(
            self.center_x - self.svg.width / 2.0,
            self.center_y - self.svg.height / 2.0)

        instruction_list = [
            PushMatrix(),
            self.translate,
            self.svg,
            PopMatrix()]

        for instruction in instruction_list:
            self.canvas.add(instruction)

    def on_pos(self, instance, pos):
        self.trigger_update()

    def on_size(self, instance, size):
        self.trigger_update()

    def update(self, dt):
        if not hasattr(self, 'translate'):
            return

        self.translate.x = self.center_x - self.svg.width / 2.0
        self.translate.y = self.center_y - self.svg.height / 2.0


class ControlPanel(BoxLayout):
    pass
