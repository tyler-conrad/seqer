from kivy.lang import Builder
from kivy.uix.modalview import ModalView

Builder.load_string('''
#:import PadLayout seqer.uix.pad_layout.PadLayout
#:import FloatInput seqer.uix.float_input.FloatInput
#:import FieldSeparator seqer.uix.field_separator.FieldSeparator

<ConfigFloatInput@FloatInput>:
    input_text_color: 0.6, 0.6, 0.6, 1.0
    background_color: 0.0, 0.0, 0.0, 0.0
    hint_text_color: 0.2, 0.2, 0.2, 1.0
    minimized_hint_text_color: 0.4, 0.4, 0.4, 1.0

<ConfigFieldSeparator@FieldSeparator>:
    color: 0.4, 0.4, 0.4, 1.0

<ConfigModal>:
    size_hint: 0.8, 0.4
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        padding: '50dp'

        BoxLayout:
            orientation: 'vertical'

            ConfigFloatInput:
                hint_text: 'Peer Address'

            ConfigFieldSeparator:
                orientation: 'horizontal'
                size_hint: 1.0, None
                size: 0.0, 1.0

        BoxLayout:
            orientation: 'horizontal'

            ConfigFloatInput:
                hint_text: 'Send Port'

            ConfigFieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: '50dp', 0.0

            ConfigFloatInput:
                hint_text: 'Receive Port'

        BoxLayout:
            padding: 0.0, '50dp', 0.0, 0.0

            Button:
                text: 'OK'
''')


class ConfigModal(ModalView):
    pass


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    config_modal = ConfigModal()
    Window.add_widget(config_modal)
    config_modal.open()
    runTouchApp()
