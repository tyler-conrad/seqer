from kivy.clock import Clock


def debounce(func, wait=1.0):
    def on_call(*args, **kwargs):
        def call_func(dt):
            func(*args, **kwargs)

        Clock.unschedule(debounce.scheduled_func_call)
        debounce.scheduled_func_call = call_func
        Clock.schedule_once(debounce.scheduled_func_call, wait)
    return on_call
debounce.scheduled_func_call = None

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    from kivy.uix.button import Button
    from kivy.clock import Clock

    def update_text(button):
        button.text = str(Clock.get_time())

    Window.add_widget(Button(on_press=debounce(update_text)))
    runTouchApp()
