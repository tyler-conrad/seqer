from kivy.uix.widget import Widget


class Wrapper(Widget):
    def on_pos(self, wrapper, pos):
        for child in self.children:
            child.pos = self.pos

    def on_size(self, wrapper, size):
        for child in self.children:
            child.size = self.size


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    from kivy.uix.button import Button

    wrapper = Wrapper()
    wrapper.add_widget(Button())
    Window.add_widget(wrapper)
    runTouchApp()
