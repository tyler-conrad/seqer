from kivy.app import App
from kivy.graphics import Color
from kivy.graphics import Ellipse
from kivy.interactive import InteractiveLauncher
from kivy.uix.widget import Widget


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))


class TestApp(App):
    def build(self):
        return Widget()

InteractiveLauncher(TestApp()).run()
