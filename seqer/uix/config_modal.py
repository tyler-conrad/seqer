from socket import gaierror

from rtpmidi.utils import check_port

from kivy.lang import Builder
from kivy.uix.modalview import ModalView

from seqer.util.network import ip_from_host_or_ip

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
            validator: root.validate_address

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
                validator: root.validate_port

            FieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: 1.0, 0.0

            FloatInput:
                hint_text: 'Receive Port'
                input_filter: 'int'
                text: str(options['receive_port'])
                validator: root.validate_port

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
                validator: root.validate_latency

            FieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: 1.0, 0.0

            FloatInput:
                hint_text: 'Jitter Buffer Size'
                input_filter: 'int'
                text: str(options['jitter_buffer'])
                validator: root.validate_jitter_buffer_size

        BoxLayout:
            padding: 0.0, '50dp', 0.0, 0.0

            Button:
                text: 'OK'
''')


class ConfigModal(ModalView):
    def validate_address(self, address):
        try:
            ip_from_host_or_ip(address)
        except gaierror as e:
            return False
        return True

    def validate_port(self, port):
        try:
            port_num = int(port)
        except ValueError as ve:
            return False
        return check_port(port_num)

    def validate_latency(self, latency):
        try:
            latency = int(latency)
        except ValueError as ve:
            return False
        return 0 <= latency < 1000

    def validate_jitter_buffer_size(self, jitter_buffer_size):
        try:
            size = int(jitter_buffer_size)
        except ValueError as ve:
            return False
        return 0 <= size < 10000


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    config_modal = ConfigModal()
    Window.add_widget(config_modal)
    config_modal.open()
    runTouchApp()
