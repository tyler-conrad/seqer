from kivy.properties import OptionProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label


Builder.load_string('''
<AlignedLabel>:
    _build_canvas: True
''')


class AlignedLabel(Label):
    widget_padding = ListProperty([0.0, 0.0, 0.0, 0.0])
    horz_align = OptionProperty(
        'center',
        options=['left', 'center', 'right'])
    vert_align = OptionProperty(
        'center',
        options=['bottom', 'center', 'top'])
    align = ReferenceListProperty(horz_align, vert_align)
    _build_canvas = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.rect = Rectangle()
        self.text_color = Color()
        super(AlignedLabel, self).__init__(**kwargs)

        self.trigger_update = Clock.create_trigger(self.update, -1)
        self.bind(
            pos=self.trigger_update,
            size=self.trigger_update,
            widget_padding=self.trigger_update)

    def on_color(self, label, color):
        self.text_color.rgba = (self.disabled_color
            if self.disabled
            else (self.color if not self.markup else (1, 1, 1, 1)))

    def on__build_canvas(self, label, build_canvas):
        canvas = self.canvas
        canvas.clear()
        canvas.add(self.text_color)
        canvas.add(self.rect)

    def on_texture(self, dispatcher, texture):
        if not self.texture:
            return

        self.rect.texture = self.texture
        self.rect.size = self.texture.size
        self.trigger_update()

    def calc_rect_pos(self, width, height):
        padding = self.widget_padding
        x = {
            'left': padding[0] + self.x,
            'center': self.center_x - width * 0.5,
            'right': self.right - (width + padding[2])
        }[self.horz_align]

        y = {
            'bottom': padding[3] + self.y,
            'center': self.center_y - height * 0.5,
            'top': self.top - (height + padding[1]),
        }[self.vert_align]

        return x, y

    def update(self, dt=None):
        if not self.texture:
            return

        self.rect.pos = self.calc_rect_pos(*self.texture.size)


if __name__ == '__main__':
    from textwrap import dedent

    from kivy.core.window import Window
    from kivy.base import runTouchApp
    from kivy.lang import Builder

    Window.add_widget(Builder.load_string(dedent('''
        <AlignedLabel>:
            color: 1.0, 1.0, 1.0, 1.0
            text: 'aligned label'

        BoxLayout:
            orientation: 'horizontal'
            AlignedLabel:
                horz_align: 'left'
            AlignedLabel:
                horz_align: 'right'
            AlignedLabel:
                align: 'left', 'bottom'
    ''')))
    runTouchApp()
