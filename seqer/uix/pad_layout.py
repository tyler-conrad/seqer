from kivy.properties import VariableListProperty
from kivy.uix.layout import Layout


class PadLayout(Layout):
    padding = VariableListProperty([0.0, 0.0, 0.0, 0.0])

    def __init__(self, **kwargs):
        super(PadLayout, self).__init__(**kwargs)
        self.bind(
            children=self._trigger_layout,
            parent=self._trigger_layout,
            padding=self._trigger_layout,
            size=self._trigger_layout,
            pos=self._trigger_layout)

    def do_layout(self, *largs):
        padding_left = self.padding[0] * self.width
        padding_top = self.padding[1] * self.height
        padding_right = self.padding[2] * self.width
        padding_bottom = self.padding[3] * self.height

        for c in self.children:
            c.x = self.x + padding_left
            c.y = self.y + padding_bottom
            c.width = self.width - (padding_left + padding_right)
            c.height = self.height - (padding_top + padding_bottom)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    from kivy.uix.button import Button
    layout = PadLayout(padding=[0.1, 0.2, 0.3, 0.4])
    layout.add_widget(Button())
    Window.add_widget(layout)
    runTouchApp()
