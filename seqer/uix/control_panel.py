from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.graphics.instructions import InstructionGroup
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
    # ControlButton:
    #     filename: 'stop.svg'
    # ControlButton:
    #     filename: 'pause.svg'
    # ControlButton:
    #     filename: 'play.svg'
    # ControlButton:
    #     filename: 'record.svg'
    # ControlButton:
    #     filename: 'fast_forward.svg'
''')


class ControlButton(ToggleButton):
    filename = StringProperty()
    placeholder = Svg(filename=resource_find('placeholder.svg'))

    def __init__(self, **kwargs):
        super(ControlButton, self).__init__(**kwargs)
        self.translate = Translate(0, 0)
        self.instruction_group = self._build_group()
        self.canvas.after.add(self.instruction_group)

        self.trigger_update = Clock.create_trigger(self.update, -1)
        self.svg = ControlButton.placeholder
        self._set_svg(self.svg)

    def _build_group(self):
        group = InstructionGroup()
        for instruction in [
                PushMatrix(),
                self.translate,
                PopMatrix()]:
            group.add(instruction)
        return group

    def _set_svg(self, svg):
        self.instruction_group.remove(self.svg)
        self.svg = svg
        self.instruction_group.insert(2, self.svg)
        self.trigger_update()

    def on_filename(self, instance, filename):
        self._set_svg(Svg(filename=resource_find(self.filename)))

    def on_pos(self, instance, pos):
        self.trigger_update()

    def on_size(self, instance, size):
        self.trigger_update()

    def update(self, dt):
        self.translate.x = self.center_x - self.svg.width / 2.0
        self.translate.y = self.center_y - self.svg.height / 2.0

class ControlPanel(BoxLayout):
    pass
