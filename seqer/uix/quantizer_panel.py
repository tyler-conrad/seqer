from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

Builder.load_string('''
<QuantizerPanel>:
    orientation: 'horizontal'

    QuantizerButton:
        id: default_pressed
        text: '1/2'
    QuantizerButton:
        text: '1/4'
    QuantizerButton:
        text: '1/8'
    QuantizerButton:
        text: '1/16'
    QuantizerButton:
        text: '1/32'
    QuantizerButton:
        text: '1/64'
''')

class QuantizerButton(ToggleButton):
    def __init__(self, **kwargs):
        kwargs['group'] = 'quantizer'
        super(QuantizerButton, self).__init__(**kwargs)

class QuantizerPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(QuantizerPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.init, -1)

    def init(self, dt):
        self.ids['default_pressed'].state = 'down'
