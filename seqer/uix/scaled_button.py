from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder

from seqer.uix.scaled_label import FontScaledLabel

Builder.load_string('''
<ScaledButton>:
    state_image: self.background_normal if self.state == 'normal' else self.background_down
    disabled_image: self.background_disabled_normal if self.state == 'normal' else self.background_disabled_down
    canvas.before:
        Color:
            rgba: self.background_color
        BorderImage:
            border: self.border
            pos: self.pos
            size: self.size
            source: self.disabled_image if self.disabled else self.state_image
''')


class ScaledButton(ButtonBehavior, FontScaledLabel):
    background_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    background_normal = StringProperty(
        'atlas://data/images/defaulttheme/button')
    background_down = StringProperty(
        'atlas://data/images/defaulttheme/button_pressed')
    background_disabled_normal = StringProperty(
        'atlas://data/images/defaulttheme/button_disabled')
    background_disabled_down = StringProperty(
        'atlas://data/images/defaulttheme/button_disabled_pressed')
    border = ListProperty([16.0, 16.0, 16.0, 16.0])

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    layout = BoxLayout(orientation='vertical')
    layout.add_widget(ScaledButton(text='Test'))
    layout.add_widget(ScaledButton(text='Test'))
    layout.add_widget(ScaledButton(text='Test'))
    Window.add_widget(layout)
    runTouchApp()
