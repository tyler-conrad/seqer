from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string('''
<FieldSeparator>:
    canvas:
        Color:
            rgba: self.color
        Line:
            points: [self.x, self.center_y, self.right, self.center_y] if self.orientation == 'horizontal' else [self.center_x, self.y, self.center_x, self.top]
            width: 1.0
''')


class FieldSeparator(Widget):
    orientation = StringProperty('horizontal')
    color = ListProperty([1.0, 1.0, 1.0, 1.0])

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    layout = BoxLayout(orientation='vertical')
    layout.add_widget(FieldSeparator(orientation='horizontal'))
    layout.add_widget(FieldSeparator(orientation='vertical'))
    Window.add_widget(layout)
    runTouchApp()
