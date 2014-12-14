"""An implementation of the Command Pattern."""

from abc import ABCMeta
from abc import abstractmethod
from collections import MutableSequence

from seqer.logger import warn

class Command(object):
    """Abstract base class for all command objects."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        """Execute the command."""


class UndoableCommand(Command):
    """Abstract base class for command support undo functionality."""
    @abstractmethod
    def unexecute(self):
        """Reverses the effects of execute."""


class MacroCommand(Command, MutableSequence):
    """A command that aggregates other commands."""
    def __init__(self, command_list=None):
        self.command_list = []
        if command_list:
            self.command_list.extend(command_list)

    def __len__(self):
        return len(self.command_list)

    def __getitem__(self, index):
        return self.command_list[index]

    def __setitem__(self, index, value):
        self.command_list[index] = value

    def __delitem__(self, index):
        del self.command_list[index]

    def insert(self, index, value):
        self.command_list.insert(index, value)

    def execute(self):
        for command in self.command_list:
            command.execute()


class UndoableMacroCommand(UndoableCommand, MacroCommand):
    """A command that aggregates other commands that support undo
    functionality.
    """
    def unexecute(self):
        for command in reversed(self.command_list):
            command.unexecute()


class RecoverableException(Exception):
    """Exception raised by commands when a recoverable error has occured.

    Can be used to wrap an existing exception object.
    """
    def __init__(self, msg, exception=None):
        self.msg = msg
        self.exception = exception

    def __str__(self):
        msg = self.msg
        if self.exception:
            msg += '\n\t' + self.exception.msg
        return msg


class RollbackMacroCommand(UndoableMacroCommand):
    """A MacroCommand whose execute and unexecute operations must complete
    without raising a RecoverableException or be rolled back.
    """
    def run(self, command_list, do, undo):
        completed_command_list = []
        for command in command_list:
            try:
                if hasattr(command, do):
                    getattr(command, do)()
                else:
                    assert hasattr(command, 'execute')
                    warn('Non-undoable command: {command}', command=command)
            except RecoverableException as e:
                warn('Rolling back macro command: {command} due to exception:' +
                     ' {exception}', command=self, exception=e)
                for completed_command in reversed(completed_command_list):
                    if hasattr(command, undo):
                        getattr(completed_command, undo)
                break
            completed_command_list.append(command)

    def execute(self):
        self.run(
            command_list=self.command_list,
            do='execute',
            undo='unexecute')

    def unexecute(self):
        self.run(
            command_list=reversed(self.command_list),
            do='unexecute',
            undo='execute')

if __name__ == '__main__':
    class Printer(UndoableCommand):
        def execute(self):
            print 'execute'

        def unexecute(self):
            print 'unexecute'

    printer_macro = UndoableMacroCommand(
        command_list=[
            Printer(),
            Printer(),
            Printer()])

    printer_macro.execute()
    printer_macro.unexecute()

    print '-' * 80

    class NonUndoableCommand(Command):
        def execute(self):
            print 'nonundoable command'

    class Raiser(Command):
        def execute(self):
            print 'exeception'
            raise RecoverableException('exception occured', None)

    rollback_macro_command = RollbackMacroCommand(
        command_list=[
            Printer(),
            NonUndoableCommand(),
            Printer(),
            Raiser()])

    rollback_macro_command.execute()
    rollback_macro_command.unexecute()
