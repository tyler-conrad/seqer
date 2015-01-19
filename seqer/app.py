from kivy.app import App
from seqer.option import options
from seqer.script import run_script
from seqer.manager import PatternManager
from seqer.sequencer import Sequencer
from seqer.uix.start_modal import StartModal


class SeqerApp(App):
    def on_start(self):
        # sequencer = Sequencer()
        # sequencer.set_pattern_manager(PatternManager())
        # sequencer.record()
        if options.script:
            run_script(options.script)
            return

        StartModal().open()
        # command_queue.do(InitRTPMIDI())
