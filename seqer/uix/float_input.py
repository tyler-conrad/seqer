from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout


Builder.load_string('''
#:import FontScaledLabel seqer.uix.scaled_label.FontScaledLabel

<FloatLabel@FontScaledLabel>:

<FloatTextInput@TextInput>:

<FloatTextInput>:
    canvas.before:
        Clear
        Color:
            rgba: (self.cursor_color if self.focus and not self.cursor_blink else (0, 0, 0, 0))
        Rectangle:
            pos: [int(x) for x in self.cursor_pos]
            size: 1, -self.line_height
        Color:
            rgba: self.disabled_foreground_color if self.disabled else (self.hint_text_color if not self.text and not self.focus else self.foreground_color)

<FloatInput>:
    orientation: 'vertical'

    canvas.before:
        Color:
            rgba: self.background_color
        BorderImage:
            border: self.border
            pos: self.pos
            size: self.size
            source: (self.background_disabled_active if self.disabled else self.background_active) if self.focus else (self.background_disabled_normal if self.disabled else self.background_normal)

    FloatTextInput:
        id: input
        pos_hint: {'x': 0.0, 'y': 0.0}
        size_hint: 1.0, 0.9
        font_size: self.height - self.height * 0.20501139
        multiline: False
        padding: 0.0, 0.0, 0.0, 0.0

    FloatLabel:
        id: label
        size_hint: None, None
        color: root.hint_text_color
        text: root.hint_text
        horz_align: 'left'
        vert_align: 'top'
''')


class FloatInput(FloatLayout):
    border = ListProperty([4.0, 4.0, 4.0, 4.0])
    background_normal = StringProperty(
        'atlas://data/images/defaulttheme/textinput')
    background_disabled_normal = StringProperty(
        'atlas://data/images/defaulttheme/textinput_disabled')
    background_active = StringProperty(
        'atlas://data/images/defaulttheme/textinput_active')
    background_disabled_active = StringProperty(
        'atlas://data/images/defaulttheme/textinput_disabled_active')
    background_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    minimized_hint_text_color = ListProperty([0.4, 0.4, 0.4, 1.0])
    hint_text_color = ListProperty([0.8, 0.8, 0.8, 1.0])
    focus = BooleanProperty(False)
    minimized_label_scale = NumericProperty(0.15)
    minimized_pad = NumericProperty(6.0)
    hint_text = StringProperty()

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.__dict__.update(self.ids)
        self.minimized = False
        self.label_anim = None
        self.input.bind(focus=self.setter('focus'))
        self.input.bind(pos=self.update_label)
        self.input.bind(size=self.update_label)
        self.input.bind(font_size=self.update_label_font_size)

    def label_minimized_attrs(self):
        return {
            'top': self.top - self.minimized_pad,
            'x': self.x + self.minimized_pad}

    def label_maximized_attrs(self):
        return {
            'y': self.input.y,
            'size': self.input.size}  # set height only?

    def update_label(self, input, pos):
        if self.minimized:
            attr_dict = self.label_minimized_attrs()
        else:
            attr_dict = self.label_maximized_attrs()

        for attr, val in attr_dict.items():
            setattr(self.label, attr, val)

    def update_label_font_size(self, input, font_size):
        if self.minimized:
            font_size = self.label.height
        else:
            font_size = input.font_size
        self.label.font_size = font_size

    def on_anim_complete(self, anim, label):
        self.update_label_font_size(self.input, self.input.font_size)
        if self.minimized:
            for attr, val in self.label_minimized_attrs().items():
                setattr(self.label, attr, val)

    def on_focus(self, float_input, focus):
        if (not self.minimized) and focus:
            self.minimized = True
            anim_kwargs = {
                # 'top': self.top - self.minimized_pad,
                # 'width': self.width * self.minimized_label_scale,
                'height': self.input.height * self.minimized_label_scale,
                'color': self.minimized_hint_text_color}
            anim_kwargs.update(**self.label_minimized_attrs())
        elif self.minimized and not self.input.text and not focus:
            self.minimized = False
            anim_kwargs = {
                # 'y': self.y,
                # 'size': self.size,
                'color': self.hint_text_color}
            anim_kwargs.update(**self.label_maximized_attrs())
        else:
            return

        if self.label_anim:
            self.label_anim.cancel(self.label)

        self.label_anim = Animation(duration=0.1, **anim_kwargs)
        if not self.minimized:
            self.label.font_size = self.input.font_size
        self.label_anim.bind(on_complete=self.on_anim_complete)
        self.label_anim.start(self.label)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    from kivy.uix.button import Button
    layout = BoxLayout(orientation='vertical')
    layout.add_widget(FloatInput(hint_text='Float Input'))
    layout.add_widget(Button())
    layout.add_widget(Button())
    layout.add_widget(Button())
    Window.add_widget(layout)
    runTouchApp()
