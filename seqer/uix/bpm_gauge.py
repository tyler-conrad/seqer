from kivy.lang import Builder
from kivy.uix.slider import Slider


Builder.load_string('''
#:import dp kivy.metrics.dp


<-BPMGauge>:
    orientation: 'horizontal'
    padding: 0.0
    range: 0.0, 240.0
    step: 1.0

    canvas:
        Color:
            rgb: 1.0, 1.0, 1.0

        BorderImage:
            pos: self.pos
            size: self.size
            border: [dp(16.0)] * 4
            source: 'atlas://data/images/defaulttheme/button'

        Color:
            rgba: 0.2, 0.2, 0.8, 0.4

        Rectangle:
            pos: self.pos
            size: self.value_normalized * self.width, self.height

    Label:
        pos: root.pos
        size: root.size
        color: 0.8, 0.8, 0.8, 1.0
        text: str(root.value)
        font_size: 0.8 * root.height
''')


class BPMGauge(Slider):
    pass
