from socket import gaierror

from rtpmidi.utils import check_port

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView

from seqer.util.network import ip_from_host_or_ip
from seqer.util.query import select_by_type
from seqer.uix.float_input import FloatInput
from seqer.command.queue import command_queue
from seqer.command.init_rtpmidi import InitRTPMIDI

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
            id: address
            hint_text: 'Address'
            text: options['address']
            validator: root.validate_address

        FieldSeparator:
            orientation: 'horizontal'
            size_hint: 1.0, None
            size: 0.0, 1.0

        BoxLayout:
            orientation: 'horizontal'

            FloatInput:
                id: send_port
                hint_text: 'Send Port'
                input_filter: 'int'
                text: str(options['send_port'])
                validator: root.validate_port

            FieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: 1.0, 0.0

            FloatInput:
                id: receive_port
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
                id: latency
                hint_text: 'Latency'
                input_filter: 'int'
                text: str(options['latency'])
                validator: root.validate_latency

            FieldSeparator:
                orientation: 'vertical'
                size_hint: None, 1.0
                size: 1.0, 0.0

            FloatInput:
                id: jitter_buffer_size
                hint_text: 'Jitter Buffer Size'
                input_filter: 'int'
                text: str(options['jitter_buffer'])
                validator: root.validate_jitter_buffer_size

        BoxLayout:
            padding: 0.0, '50dp', 0.0, 0.0

            Button:
                text: 'OK'
                on_press: root.on_ok()
''')


class ConfigModal(ModalView):
    @staticmethod
    def validate_address(address):
        try:
            ip_from_host_or_ip(address)
        except gaierror as e:
            return False
        return True

    @staticmethod
    def validate_port(port):
        try:
            port_num = int(port)
        except ValueError as ve:
            return False
        return check_port(port_num)

    @staticmethod
    def validate_latency(latency):
        try:
            latency = int(latency)
        except ValueError as ve:
            return False
        return 0 <= latency < 1000

    @staticmethod
    def validate_jitter_buffer_size(jitter_buffer_size):
        try:
            size = int(jitter_buffer_size)
        except ValueError as ve:
            return False
        return 0 <= size < 10000

    def __init__(self, **kwargs):
        super(ConfigModal, self).__init__(**kwargs)
        Clock.schedule_once(self.init, -1)

    def init(self, dt):
        self.__dict__.update(self.ids)

    def on_ok(self):
        float_input_list = list(select_by_type(self, FloatInput))
        for float_input in float_input_list:
            float_input.validate()

        if not all([float_input.is_valid for float_input in float_input_list]):
            return

        command_queue.do(InitRTPMIDI(
            peer_address=self.address.text,
            sending_port=self.send_port.text,
            receiving_port=self.receive_port.text,
            latency=self.latency.text,
            jitter_buffer_size=self.jitter_buffer_size.text))
        self.dismiss()

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    config_modal = ConfigModal()
    Window.add_widget(config_modal)
    config_modal.open()
    runTouchApp()
