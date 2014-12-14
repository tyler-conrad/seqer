from kivy.lang import Builder
from kivy.uix.slider import Slider


Builder.load_string('''
#:import dp seqer.utils.map_dp

<-BPMGauge>:
    range: 0.0, 240.0
    step: 1.0
    padding: 0.0

    canvas:
        BorderImage:
            border: dp([16.0] * 4)
            pos: dp(self.pos)
            size: dp(self.size)
            source: 'atlas://data/images/defaulttheme/button'

        Color:
            rgba: 0.2, 0.2, 0.8, 0.5

        Rectangle:
            pos: dp(self.pos)
            size: dp([self.value_normalized * self.width, self.height])

    Label:
        color: 0.0, 0.0, 0.0, 0.5
        text: str(root.value)
        font_size: str(dp([0.8 * root.height])[0]) + 'dp'
        pos: dp(root.pos)
        size: dp(root.size)
''')


class BPMGauge(Slider):
    pass
