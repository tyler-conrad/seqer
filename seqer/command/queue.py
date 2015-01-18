from seqer.logger import info
from seqer.logger import debug


class CommandQueue(object):
    def __init__(self):
        self.index = -1
        self.queue = []

    def do(self, command):
        debug('Doing command: {command}', command=command)
        command.execute()
        self.queue = self.queue[:self.index + 1]
        self.queue.append(command)
        self.index += 1

    def redo(self):
        try:
            command = self.queue[self.index + 1]
        except IndexError as ie:
            info('No commands available for redo')
            return
        debug('Redoing command: {command}', command=command)
        command.execute()
        self.index += 1

    def undo(self):
        while True:
            if self.index < 0:
                info('All commands have been undone')
                return

            try:
                command = self.queue[self.index]
            except IndexError as ie:
                info('No commands available for undo')
                return
            self.index -= 1

            try:  # type check instead of try/catch?
                debug('Undoing command: {command}', command=command)
                command.unexecute()
            except AttributeError as ae:
                debug('Undo attempted on non-undoable command')
                continue

            return

command_queue = CommandQueue()

if __name__ == '__main__':
    from seqer.command.base import UndoableCommand
    from seqer.command.base import Command

    class Printer(UndoableCommand):
        def execute(self):
            print 'execute'

        def unexecute(self):
            print 'unexecute'

    class NonUndoableCommand(Command):
        def execute(self):
            print 'nonundoable command'

    cq = CommandQueue()

    cq.redo()
    cq.undo()

    cq.do(Printer())
    cq.do(Printer())
    cq.do(NonUndoableCommand())

    cq.undo()
    cq.redo()
    cq.undo()
    cq.undo()

    cq.undo()

    cq.do(NonUndoableCommand())
    cq.redo()
    cq.undo()
