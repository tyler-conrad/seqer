from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from seqer.uix.config_modal import ConfigModal

Builder.load_string('''
#:import ScaledButton seqer.uix.scaled_button.ScaledButton

<StartModal>:
    size_hint: 0.8, 0.4

    BoxLayout:
        orientation: 'vertical'
        padding: '50dp'

        ScaledButton:
            text: 'Setup'
            on_press: root.setup()

        ScaledButton:
            text: 'Load Script'

''')


class StartModal(ModalView):
    def setup(self):
        ConfigModal().open()
        self.dismiss()

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    config_modal = StartModal()
    Window.add_widget(config_modal)
    config_modal.open()
    runTouchApp()
