from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout


Builder.load_string('''
#:import FontScaledLabel seqer.uix.scaled_label.FontScaledLabel
#:import dp kivy.metrics.dp

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
        padding: dp(root.left_padding), 0.0, 0.0, 0.0
        foreground_color: root.input_text_color
        write_tab: False
        input_filter: root.input_filter
        text: root.text

    FloatLabel:
        id: label
        size_hint: None, None
        color: root.hint_text_color
        text: root.hint_text
        horz_align: 'left'
        vert_align: 'top'
        widget_padding: dp(root.left_padding), 0.0, 0.0, 0.0
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
    input_text_color = ListProperty([0.6, 0.6, 0.6, 1.0])
    background_color = ListProperty([0.0, 0.0, 0.0, 0.0])
    minimized_hint_text_color = ListProperty([0.4, 0.4, 0.4, 1.0])
    hint_text_color = ListProperty([0.2, 0.2, 0.2, 1.0])
    left_padding = NumericProperty(20.0)
    input_filter = ObjectProperty(None, allownone=True)
    focus = BooleanProperty(False)
    minimized_label_scale = NumericProperty(0.15)
    minimized_pad = NumericProperty(6.0)
    text = StringProperty('')
    hint_text = StringProperty('')

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.minimized = False
        self.label_anim = None
        Clock.schedule_once(self.init, -1)

    def init(self, dt):
        self.__dict__.update(self.ids)
        self.input.bind(focus=self.setter('focus'))
        self.input.bind(pos=self.update_label)
        self.input.bind(size=self.update_label)
        self.input.bind(font_size=self.update_label_font_size)

        def init_focus(dt):
            self.on_focus(self.input, True)
        Clock.create_trigger(init_focus, 0)()

    def label_minimized_attrs(self):
        return {
            'top': self.top - self.minimized_pad,
            'x': self.x + self.minimized_pad}

    def label_maximized_attrs(self):
        return {
            'x': self.x,
            'y': self.input.y,
            'size': self.input.size}  # set height only?

    def update_label(self, input=None, pos=None):
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

    def on_input_text(self, float_input, text):
        print 'on input text'
        self.on_focus(float_input, True)

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
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    layout = BoxLayout(orientation='vertical')
    sublayout = BoxLayout(orientation='horizontal')
    sublayout.add_widget(Button())
    sublayout.add_widget(FloatInput(hint_text='Float Input'))
    layout.add_widget(sublayout)
    layout.add_widget(Button())
    layout.add_widget(Button())
    layout.add_widget(Button())
    Window.add_widget(layout)
    runTouchApp()
