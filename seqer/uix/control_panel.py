from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.resources import resource_find
from kivy.graphics.svg import Svg
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Translate
from kivy.graphics.context_instructions import PushMatrix
from kivy.graphics.context_instructions import PopMatrix
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import Button

from seqer.utils import QueryDict

Builder.load_string('''
<ControlPanel>:
    ControlButton:
        id: rewind
        normal_filename: 'rewind.svg'
    ControlButton:
        id: stop
        normal_filename: 'stop.svg'
    PlayPauseButton:
        id: play_pause
        normal_filename: 'play.svg'
        down_filename: 'pause.svg'
    ControlToggleButton:
        id: record
        normal_filename: 'record.svg'
    ControlButton:
        id: fast_forward
        normal_filename: 'fast_forward.svg'
''')


class ControlButton(Button):
    normal_filename = StringProperty()
    placeholder = Svg(filename=resource_find('placeholder.svg'))

    def __init__(self, **kwargs):
        super(ControlButton, self).__init__(**kwargs)
        self.translate = Translate(0, 0)
        self.instruction_group = self._build_group()
        self.canvas.after.add(self.instruction_group)

        self.trigger_update = Clock.create_trigger(self.update, -1)
        self.normal_svg = self.svg = ControlButton.placeholder
        self._set_svg(self.normal_svg)

    def _build_group(self):
        group = InstructionGroup()
        for instruction in [
                PushMatrix(),
                self.translate,
                PopMatrix()]:
            group.add(instruction)
        return group

    def _set_svg(self, svg):
        if self.svg in self.instruction_group.children:
            self.instruction_group.remove(self.svg)
        self.svg = svg
        self.instruction_group.insert(2, self.svg)
        self.trigger_update()

    def on_normal_filename(self, instance, filename):
        self.normal_svg = Svg(filename=resource_find(filename))
        self._set_svg(self.normal_svg)

    def on_pos(self, instance, pos):
        self.trigger_update()

    def on_size(self, instance, size):
        self.trigger_update()

    def update(self, dt):
        self.translate.x = self.center_x - self.svg.width / 2.0
        self.translate.y = self.center_y - self.svg.height / 2.0


class ControlToggleButton(ToggleButtonBehavior, ControlButton):
    pass


class PlayPauseButton(ControlToggleButton):
    down_filename = StringProperty()

    def __init__(self, **kwargs):
        super(PlayPauseButton, self).__init__(**kwargs)
        self.down_svg = ControlButton.placeholder
        self._set_down_svg(self.down_svg)

    def _set_down_svg(self, svg):
        if self.state == 'down':
            self._set_svg(self.down_svg)

    def on_down_filename(self, instance, filename):
        self.down_svg = Svg(filename=resource_find(filename))
        self._set_down_svg(self.down_svg)

    def on_state(self, instance, state):
        if state == 'down':
            self._set_svg(self.down_svg)
        else:
            self._set_svg(self.normal_svg)


class ControlPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.init, -1)

    def init(self, dt):
        self.is_stopped = True
        self.control = QueryDict(self.ids)
        self.control.record.bind(state=self.on_record)
        self.control.stop.bind(on_press=self.on_stop_press)
        self.control.play_pause.bind(state=self.on_play_pause)

    def disable_scrubbing(self, is_disabled):
        self.control.rewind.disabled = is_disabled
        self.control.fast_forward.disabled = is_disabled

    def on_record(self, record_button, state):
        if state == 'down':
            self.is_stopped = False
            self.disable_scrubbing(True)
        else:
            self.disable_scrubbing(False)

    def on_stop_press(self, stop_button):
        self.control.record.state = 'normal'
        self.control.play_pause.state = 'normal'
        if self.is_stopped:
            pass
            # todo: move cursor to start of pattern

    def on_play_pause(self, play_pause_button, state):
        self.is_stopped = False
