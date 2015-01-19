from kivy.lang import Builder
from kivy.uix.modalview import ModalView

Builder.load_string('''
#:import options seqer.option.options
#:import PadLayout seqer.uix.pad_layout.PadLayout
#:import FloatInput seqer.uix.float_input.FloatInput
#:import FieldSeparator seqer.uix.field_separator.FieldSeparator

<ConfigModal>:
    size_hint: 0.8, 0.6
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        padding: '50dp'

        FloatInput:
            hint_text: 'Peer Address'
            text: options['address']

        FieldSeparator:
            orientation: 'horizontal'
            size_hint: 1.0, None
            size: 0.0, 1.0

        BoxLayout:
            orientation: 'horizontal'

            FloatInput:
                hint_text: 'Send Port'
                input_filter: 'int'
                text: str(options['send_port'])

            FieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: 1.0, 0.0

            FloatInput:
                hint_text: 'Receive Port'
                input_filter: 'int'
                text: str(options['receive_port'])

        FieldSeparator:
            orientation: 'horizontal'
            size_hint: 1.0, None
            size: 0.0, 1.0

        BoxLayout:
            orientation: 'horizontal'

            FloatInput:
                hint_text: 'Latency'
                input_filter: 'int'
                text: str(options['latency'])

            FieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: 1.0, 0.0

            FloatInput:
                hint_text: 'Jitter Buffer Size'
                input_filter: 'int'
                text: str(options['jitter_buffer'])

        BoxLayout:
            padding: 0.0, '50dp', 0.0, 0.0

            Button:
                text: 'OK'
''')


class ConfigModal(ModalView):
    pass
    # def __init__(self, **kwargs):
    #     super(ConfigModal, self).__init__(**kwargs)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    config_modal = ConfigModal()
    Window.add_widget(config_modal)
    config_modal.open()
    runTouchApp()
